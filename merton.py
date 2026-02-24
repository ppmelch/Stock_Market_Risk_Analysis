from libraries import norm, np , pd
from risk_models import RiskModel

class Merton(RiskModel):
    """Merton structural model for default risk estimation."""

    def __init__(self, companies, rf=0.03):
        """Initialize the model with company data and risk-free rate."""
        super().__init__(companies)
        self.rf = rf

    def V(self, ticker):
        """Return firm value proxy as equity value plus total debt."""
        return (
            self.companies.market_equity(ticker)
            + self.companies.total_debt(ticker)
        )

    def D(self, ticker):
        """Return default point proxy based on total debt."""
        return self.companies.total_debt(ticker)

    def vol(self, ticker):
        """Return annualized equity volatility for a ticker."""
        return self.companies.equity_volatility(ticker)

    def distance_to_default(self, ticker, T=1):
        """Compute distance to default over horizon T in years."""

        V = self.V(ticker)
        D = self.D(ticker)
        sigma = self.vol(ticker)

        if D <= 0 or sigma <= 0:
            raise ValueError(f"{ticker}: invalid inputs")

        DD = (
            np.log(V / D)
            + (self.rf + sigma**2 / 2) * T
        ) / (sigma * np.sqrt(T))

        return DD

    def probability_of_default(self, ticker, T=1):
        """Compute default probability in percentage terms."""

        DD = self.distance_to_default(ticker, T)
        return (1 - norm.cdf(DD)) * 100

    def merton_df(self):
        """Return a dataframe with distance to default and PD by ticker."""

        data = []

        for ticker in self.companies.tickers:

            try:
                dd = self.distance_to_default(ticker)
                pd_default = self.probability_of_default(ticker)

                data.append({
                    "Ticker": ticker,
                    "Distance to Default": round(dd, 4),
                    "Probability of Default": pd_default
                })

            except Exception as e:
                print(f"⚠️ {ticker} skipped → {e}")

        if not data:
            return pd.DataFrame(
                columns=[
                    "Distance to Default",
                    "Probability of Default"
                ]
            )

        return pd.DataFrame(data).set_index("Ticker")