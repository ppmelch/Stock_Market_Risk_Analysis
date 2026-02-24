import pandas as pd
from risk_models import RiskModel


class Altman(RiskModel):
    """Altman Z-Score model implementation for listed companies."""

    def __init__(self, companies):
        """Initialize the Altman model with a financial data provider."""
        super().__init__(companies)

    def _compute_ratios(self, ticker):
        """Compute the five Altman financial ratios for one ticker."""

        fs = self.companies

        X1 = fs.working_capital(ticker) / fs.total_assets(ticker)
        X2 = fs.retained_earnings(ticker) / fs.total_assets(ticker)
        X3 = fs.ebit(ticker) / fs.total_assets(ticker)
        X4 = fs.market_equity(ticker) / fs.total_liabilities(ticker)
        X5 = fs.sales(ticker) / fs.total_assets(ticker)

        return X1, X2, X3, X4, X5

    def compute(self, ticker):
        """Return the Altman Z-Score for a single ticker."""

        try:
            X1, X2, X3, X4, X5 = self._compute_ratios(ticker)

            z = (
                1.2 * X1 +
                1.4 * X2 +
                3.3 * X3 +
                0.6 * X4 +
                1.0 * X5
            )

            return z

        except Exception as e:
            print(f"⚠️ {ticker} skipped → {e}")
            return None

    def ratios_matrix(self):
        """Build a dataframe with Altman ratio components by ticker."""

        data = []

        for ticker in self.companies.tickers:
            try:
                X1, X2, X3, X4, X5 = self._compute_ratios(ticker)

                data.append({
                    "Ticker": ticker,
                    "X1": X1,
                    "X2": X2,
                    "X3": X3,
                    "X4": X4,
                    "X5": X5
                })

            except Exception as e:
                print(f"⚠️ Skipping {ticker}: {e}")

        return pd.DataFrame(data).set_index("Ticker")

    def compute_all(self):
        """Compute Altman Z-Score values for all configured tickers."""

        return {
            ticker: self.compute(ticker)
            for ticker in self.companies.tickers
        }

    def z_scores_df(self):
        """Return all computed Z-Scores as a ticker-indexed dataframe."""

        results = self.compute_all()

        df = pd.DataFrame({
            "Ticker": results.keys(),
            "Z-Score": results.values()
        })

        return df.set_index("Ticker")