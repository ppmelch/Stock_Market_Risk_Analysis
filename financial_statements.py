from libraries import pd, yf, np
from data_processing import download_prices


class Companies:
    """Container that downloads, caches, and serves company financial data."""

    def __init__(self, tickers, interval="1y"):
        """Initialize the data container for the provided ticker symbols."""

        self.tickers = [t.upper() for t in tickers]
        self.interval = interval

        self._prices = None
        self._income_stmt = {}
        self._balance_sheet = {}
        self._market_data = {}

        self._yf = {
            t: yf.Ticker(t)
            for t in self.tickers
        }

    @property
    def prices(self):
        """Return cached adjusted close prices for all configured tickers."""

        if self._prices is None:

            prices = download_prices(
                self.tickers,
                self.interval
            )

            if prices.empty:
                print("⚠️ No price data available")

            self._prices = prices

        return self._prices

    @property
    def income_statements(self):
        """Return cached annual and TTM income statements by ticker."""

        if not self._income_stmt:

            for t in self.tickers:
                try:
                    ticker = self._yf[t]

                    annual = ticker.financials
                    quarterly = ticker.quarterly_financials

                    if annual is None or annual.empty:
                        self._income_stmt[t] = None
                        continue

                    if quarterly is not None and not quarterly.empty:
                        ttm = quarterly.iloc[:, :4].sum(axis=1)
                        ttm = pd.DataFrame(ttm, columns=["TTM"])
                        income = pd.concat([ttm, annual], axis=1)
                    else:
                        income = annual

                    self._income_stmt[t] = income

                except Exception:
                    self._income_stmt[t] = None

        return self._income_stmt

    @property
    def balance_sheets(self):
        """Return cached balance sheets by ticker."""

        if not self._balance_sheet:

            for t in self.tickers:

                try:
                    ticker = self._yf[t]

                    bs = ticker.balance_sheet

                    if bs is None or bs.empty:
                        bs = None

                    self._balance_sheet[t] = bs

                except Exception:
                    self._balance_sheet[t] = None

        return self._balance_sheet

    @property
    def market_data(self):
        """Return cached market metadata needed by risk models."""

        if not self._market_data:

            for t in self.tickers:

                try:
                    info = self._yf[t].info

                    self._market_data[t] = {
                        "market_cap": info.get("marketCap"),
                    }

                except Exception:
                    self._market_data[t] = None

        return self._market_data

    def _bs(self, ticker):
        """Return the latest balance sheet series for a ticker."""

        bs = self.balance_sheets.get(ticker)

        if bs is None or bs.empty:
            raise ValueError(f"{ticker}: Balance sheet unavailable")

        return bs.iloc[:, 0]

    def _inc(self, ticker):
        """Return the income statement series, preferring TTM when available."""

        inc = self.income_statements.get(ticker)

        if inc is None or inc.empty:
            raise ValueError(f"{ticker}: Income statement unavailable")

        if "TTM" in inc.columns:
            return inc["TTM"]

        return inc.iloc[:, 0]

    def total_assets(self, ticker):
        """Return total assets for the given ticker."""
        return self._bs(ticker)["Total Assets"]

    def total_liabilities(self, ticker):
        """Return total liabilities for the given ticker."""
        return self._bs(ticker)[
            "Total Liabilities Net Minority Interest"
        ]

    def working_capital(self, ticker):
        """Return working capital computed from current assets and liabilities."""
        bs = self._bs(ticker)
        return bs["Current Assets"] - bs["Current Liabilities"]

    def retained_earnings(self, ticker):
        """Return retained earnings for the given ticker."""
        return self._bs(ticker)["Retained Earnings"]

    def ebit(self, ticker):
        """Return EBIT for the given ticker."""
        return self._inc(ticker)["EBIT"]

    def sales(self, ticker):
        """Return total revenue (sales) for the given ticker."""
        return self._inc(ticker)["Total Revenue"]

    def market_equity(self, ticker):
        """Return market capitalization used as market equity."""
        return self.market_data[ticker]["market_cap"]

    def equity_volatility(self, ticker):
        """Return annualized equity return volatility from price history."""

        if ticker not in self.prices:
            raise ValueError(f"{ticker}: No price data")

        prices = self.prices[ticker]

        returns = np.log(
            prices / prices.shift(1)
        ).dropna()

        return returns.std() * np.sqrt(252)

    def total_debt(self, ticker):
        """Return total debt, using fallback fields when needed."""

        bs = self._bs(ticker)

        possible_names = [
            "Total Debt",
            "Short Long Term Debt Total",
            "Long Term Debt",
        ]

        for name in possible_names:
            if name in bs.index:
                return bs[name]

        return 0.5 * bs[
            "Total Liabilities Net Minority Interest"
        ]
