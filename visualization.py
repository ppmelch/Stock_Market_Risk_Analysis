from libraries import px, go, st
from risk_models import RiskModel


class Visualization:
    """
    Visualization layer responsible for formatting model outputs
    and generating interactive Plotly visualizations for the
    financial risk dashboard.

    This class separates presentation logic from financial models,
    ensuring that numerical computations remain independent from
    visualization and display formatting.
    """

    def __init__(self):
        """
        Initializes visualization configuration used
        across all Plotly charts.
        """
        self.template = "plotly_dark"

    @staticmethod
    def format_merton_table(merton_df):
        """
        Formats the Merton model results for visualization.

        Converts numerical outputs into readable financial values:
        - Distance to Default rounded to two decimals.
        - Probability of Default expressed as percentage format.

        Parameters
        ----------
        merton_df : pandas.DataFrame
            Raw output from the Merton model.

        Returns
        -------
        pandas.DataFrame
            Formatted dataframe ready for display.
        """

        df = merton_df.copy()

        df["Distance to Default"] = df[
            "Distance to Default"
        ].map(lambda x: f"{x:.2f}")

        df["Probability of Default"] = df[
            "Probability of Default"
        ].map(
            lambda x: "<0.01%" if x < 0.01 else f"{x:.2f}%"
        )

        return df

    @staticmethod
    def build_credit_table(z_df, merton_df):
        """
        Combines Altman Z-Score and Merton outputs to generate
        a unified credit risk assessment table.

        Applies the credit decision rule defined in RiskModel
        to classify firms into APPROVE, REVIEW, or DENY.

        Parameters
        ----------
        z_df : pandas.DataFrame
            Altman Z-score results.
        merton_df : pandas.DataFrame
            Merton model results.

        Returns
        -------
        pandas.DataFrame
            Combined and formatted credit decision table.
        """

        df = z_df.join(merton_df, how="inner")

        df["Decision"] = df.apply(
            lambda row: RiskModel.credit_decision(
                row["Z-Score"],
                row["Probability of Default"]
            ),
            axis=1
        )

        df["Z-Score"] = df["Z-Score"].map(lambda x: f"{x:.2f}")
        df["Distance to Default"] = df[
            "Distance to Default"
        ].map(lambda x: f"{x:.2f}")
        df["Probability of Default"] = df[
            "Probability of Default"
        ].map(
            lambda x: "<0.01%" if x < 0.01 else f"{x:.2f}%"
        )

        return df.reset_index()

    @staticmethod
    def plot_altman(z_df):
        """
        Creates an interactive bar chart displaying Altman Z-Scores.

        Companies are colored according to financial distress zones:
        Unsafe (<1.8), Grey (1.8–3), and Safe (>3).

        Parameters
        ----------
        z_df : pandas.DataFrame
            Altman Z-score results.
        """

        df = z_df.reset_index()

        def risk_zone(z):
            if z < 1.8:
                return "Unsafe"
            elif z < 3:
                return "Grey"
            return "Safe"

        df["Zone"] = df["Z-Score"].apply(risk_zone)

        color_map = {
            "Unsafe": "#dc2626",
            "Grey": "#9ca3af",
            "Safe": "#16a34a"
        }

        fig = px.bar(
            df,
            x="Ticker",
            y="Z-Score",
            color="Zone",
            color_discrete_map=color_map,
            text="Z-Score",
            title="Altman Z-Score"
        )

        fig.add_hline(y=1.8, line_dash="dash", line_color="red")
        fig.add_hline(y=3, line_dash="dash", line_color="green")

        fig.update_traces(texttemplate="%{text:.2f}")

        fig.update_layout(
            height=450,
            xaxis_title="Company",
            yaxis_title="Z Score"
        )

        st.plotly_chart(fig, use_container_width=True)

    def plot_merton_dd(self, merton_df):
        """
        Displays Distance to Default with risk zones.
        """

        df = merton_df.reset_index()

        def dd_zone(dd):
            if dd <= 1.5:
                return "Unsafe"
            elif dd <= 3:
                return "Grey"
            return "Safe"

        df["Zone"] = df["Distance to Default"].apply(dd_zone)

        color_map = {
            "Unsafe": "#dc2626",
            "Grey": "#9ca3af",
            "Safe": "#16a34a"
        }

        fig = px.bar(
            df,
            x="Ticker",
            y="Distance to Default",
            color="Zone",
            color_discrete_map=color_map,
            text="Distance to Default",
            template=self.template,
            title="Distance to Default"
        )

        fig.add_hline(y=1.5, line_dash="dash", line_color="red")
        fig.add_hline(y=3, line_dash="dash", line_color="green")

        fig.update_traces(texttemplate="%{text:.2f}")

        st.plotly_chart(fig, use_container_width=True)

    def plot_pd(self, merton_df):
        """
        Displays Probability of Default with risk zones.
        """

        df = merton_df.reset_index()

        def pd_zone(pd):
            if pd > 15:
                return "Unsafe"
            elif pd > 5:
                return "Grey"
            return "Safe"

        df["Zone"] = df["Probability of Default"].apply(pd_zone)

        color_map = {
            "Unsafe": "#dc2626",
            "Grey": "#9ca3af",
            "Safe": "#16a34a"
        }

        fig = px.bar(
            df,
            x="Ticker",
            y="Probability of Default",
            color="Zone",
            color_discrete_map=color_map,
            text="Probability of Default",
            template=self.template,
            title="Probability of Default (%)"
        )

        fig.add_hline(y=5, line_dash="dash", line_color="green")
        fig.add_hline(y=15, line_dash="dash", line_color="red")

        fig.update_traces(
            texttemplate="%{text:.2f}",
            hovertemplate="PD: %{y:.2f}%"
        )

        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def plot_credit_table(df):
        """
        Displays the final credit decision table using
        a Plotly interactive table.

        Decision outcomes are color-coded:
        green (APPROVE), orange (REVIEW), red (DENY).

        Parameters
        ----------
        df : pandas.DataFrame
            Credit decision dataframe.
        """

        decision_colors = []

        for d in df["Decision"]:
            if d == "APPROVE":
                decision_colors.append("#16a34a")
            elif d == "DENY":
                decision_colors.append("#dc2626")
            else:
                decision_colors.append("#9ca3af")

        n_cols = len(df.columns)

        cell_colors = [
            ["#0b1220"] * len(df)
            for _ in range(n_cols - 1)
        ] + [decision_colors]

        fig = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=list(df.columns),
                        fill_color="#111827",
                        font=dict(color="white", size=14),
                        align="left"
                    ),
                    cells=dict(
                        values=[df[col] for col in df.columns],
                        fill_color=cell_colors,
                        font=dict(color="white"),
                        align="left"
                    )
                )
            ]
        )

        fig.update_layout(
            template="plotly_dark",
            height=350
        )

        st.plotly_chart(fig, use_container_width=True)