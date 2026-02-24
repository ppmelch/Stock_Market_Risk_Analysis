class RiskModel:
    """Base class for risk models used to evaluate company creditworthiness."""

    def __init__(self, companies):
        """Initialize the risk model with a company data mapping.

        Args:
            companies: Dictionary-like object containing company information.
        """
        self.companies = companies
        self._ratio_cache = {}

    def compute(self, ticker):
        """Compute model-specific risk outputs for a given ticker.

        Args:
            ticker: Stock symbol identifying the company to evaluate.

        Raises:
            NotImplementedError: Always, unless implemented in a subclass.
        """
        raise NotImplementedError(
            "Subclasses must implement compute()"
        )

    @staticmethod
    def credit_decision(z_score, pd):
        """Return a credit decision based on Z-Score and probability of default.

        Args:
            z_score: Altman Z-Score value.
            pd: Probability of default expressed as a percentage.

        Returns:
            str: One of "Insufficient Data", "APPROVE", "DENY", or "REVIEW".
        """

        if z_score is None or pd is None:
            return "Insufficient Data"

        if z_score > 3 and pd < 5:
            return "APPROVE"

        if z_score < 1.8 or pd > 20:
            return "DENY"

        return "REVIEW"
