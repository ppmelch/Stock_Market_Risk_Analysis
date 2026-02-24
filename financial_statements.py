from libraries import pd, yf , np
from data_processing import download_prices


class Companies:

    def __init__(self, tickers, interval="1y"):

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

    # ===============================
    # PRICES
    # ===============================
    @property
    def prices(self):

        if self._prices is None:

            prices = download_prices(
                self.tickers,
                self.interval
            )

            if prices.empty:
                print("⚠️ No price data available")

            self._prices = prices

        return self._prices

    # ===============================
    # INCOME STATEMENTS
    # ===============================
    @property
    def income_statements(self):

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

    # ===============================
    # BALANCE SHEETS
    # ===============================
    @property
    def balance_sheets(self):

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

    # ===============================
    # MARKET DATA
    # ===============================
    @property
    def market_data(self):

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

    # ===============================
    # INTERNAL HELPERS
    # ===============================
    def _bs(self, ticker):

        bs = self.balance_sheets.get(ticker)

        if bs is None or bs.empty:
            raise ValueError(f"{ticker}: Balance sheet unavailable")

        return bs.iloc[:, 0]

    def _inc(self, ticker):

        inc = self.income_statements.get(ticker)

        if inc is None or inc.empty:
            raise ValueError(f"{ticker}: Income statement unavailable")

        if "TTM" in inc.columns:
            return inc["TTM"]

        return inc.iloc[:, 0]

    # ===============================
    # FINANCIAL VARIABLES
    # ===============================
    def total_assets(self, ticker):
        return self._bs(ticker)["Total Assets"]

    def total_liabilities(self, ticker):
        return self._bs(ticker)[
            "Total Liabilities Net Minority Interest"
        ]

    def working_capital(self, ticker):
        bs = self._bs(ticker)
        return bs["Current Assets"] - bs["Current Liabilities"]

    def retained_earnings(self, ticker):
        return self._bs(ticker)["Retained Earnings"]

    def ebit(self, ticker):
        return self._inc(ticker)["EBIT"]

    def sales(self, ticker):
        return self._inc(ticker)["Total Revenue"]

    def market_equity(self, ticker):
        return self.market_data[ticker]["market_cap"]

    def equity_volatility(self, ticker):

        if ticker not in self.prices:
            raise ValueError(f"{ticker}: No price data")

        prices = self.prices[ticker]

        returns = np.log(
            prices / prices.shift(1)
        ).dropna()

        return returns.std() * np.sqrt(252)