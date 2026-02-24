from libraries import pd
from risk_models import RiskModel


class Altman(RiskModel):

    def __init__(self, companies):
        super().__init__(companies)

    # =====================================================
    # COMPUTE FINANCIAL RATIOS
    # =====================================================
    def _compute_ratios(self, ticker):

        fs = self.companies

        X1 = fs.working_capital(ticker) / fs.total_assets(ticker)
        X2 = fs.retained_earnings(ticker) / fs.total_assets(ticker)
        X3 = fs.ebit(ticker) / fs.total_assets(ticker)
        X4 = fs.market_equity(ticker) / fs.total_liabilities(ticker)
        X5 = fs.sales(ticker) / fs.total_assets(ticker)

        return X1, X2, X3, X4, X5

    # =====================================================
    # ALTMAN Z SCORE
    # =====================================================
    def compute(self, ticker):

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

    # =====================================================
    # RATIOS MATRIX
    # =====================================================
    def ratios_matrix(self):

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

    # =====================================================
    # ALL Z SCORES
    # =====================================================
    def compute_all(self):

        return {
            ticker: self.compute(ticker)
            for ticker in self.companies.tickers
        }

    # =====================================================
    # DATAFRAME OUTPUT
    # =====================================================
    def z_scores_df(self):

        results = self.compute_all()

        df = pd.DataFrame({
            "Ticker": results.keys(),
            "Z-Score": results.values()
        })

        return df.set_index("Ticker")