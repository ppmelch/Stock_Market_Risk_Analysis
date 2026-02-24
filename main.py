import streamlit as st
from altman import Altman
from merton import Merton
from financial_statements import Companies
from visualization import Visualization


def main():
    """
    Main entry point of the Stock Market Risk Dashboard.

    This dashboard evaluates corporate credit risk using
    the Altman Z-Score and Merton structural default model.
    Financial data is dynamically downloaded using ticker
    symbols provided by the user.

    The workflow consists of:
        1. Data acquisition and caching.
        2. Risk model computation.
        3. Interactive visualization.
        4. Credit approval decision.
    """

    st.set_page_config(
        page_title="Risk Dashboard",
        layout="wide"
    )

    @st.cache_resource
    def load_companies(tickers, interval):
        """
        Downloads and caches financial information for
        selected companies to avoid repeated API calls.

        Parameters
        ----------
        tickers : tuple
            Company ticker symbols.
        interval : str
            Historical price interval.

        Returns
        -------
        Companies
            Initialized financial data container.
        """
        return Companies(tickers, interval)

    if "companies" not in st.session_state:
        """
        Initializes session storage used to persist
        downloaded financial data across Streamlit reruns.
        """
        st.session_state.companies = None

    st.title("Stock Market Risk Analysis")
    st.markdown("Altman Z-Score & Merton Model")
    st.markdown("José Armando Melchor Soto - 745697")
    st.markdown("---")

    viz = Visualization()

    col1, col2, col3 = st.columns([4, 2, 1])

    with col1:
        raw_tickers = st.text_input(
            "Tickers",
            value="AZO, MA, BA, F"
        )

    with col2:
        interval = st.selectbox(
            "Interval",
            ["6mo", "1y", "2y", "5y", "10y"]
        )

    with col3:
        st.write("")
        st.write("")
        run_analysis = st.button(
            "Run",
            type="primary"
        )

    if run_analysis:
        tickers = [
            t.strip().upper()
            for t in raw_tickers.split(",")
        ]

        with st.spinner("Downloading financial data..."):

            companies = load_companies(
                tuple(tickers),
                interval
            )

            if companies.prices.empty:
                st.error("Yahoo Finance returned no data.")
                return

            st.session_state.companies = companies

    if st.session_state.companies is None:
        st.info("Select tickers and press Run")
        return

    companies = st.session_state.companies

    st.markdown("---")
    st.header("Altman Z-Score")

    altman = Altman(companies)
    z_df = altman.z_scores_df().dropna()

    if not z_df.empty:

        colA, colB = st.columns([1, 2])

        with colA:
            st.markdown("<br><br><br>",
                        unsafe_allow_html=True)
            st.dataframe(
                z_df,
                use_container_width=True
            )

        with colB:
            viz.plot_altman(z_df)

    st.markdown("---")
    st.header("Merton Model")

    merton = Merton(companies)
    merton_df = merton.merton_df().dropna()

    if merton_df.empty:
        st.warning("No valid Merton results.")
        return

    formatted_merton = viz.format_merton_table(
        merton_df
    )

    st.dataframe(
        formatted_merton,
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    with col1:
        viz.plot_merton_dd(merton_df)

    with col2:
        viz.plot_pd(merton_df)

    st.markdown("---")
    st.header("Credit Decision")

    credit_df = viz.build_credit_table(
        z_df,
        merton_df
    )

    viz.plot_credit_table(credit_df)

    st.markdown("---")
    st.header("Bibliography")
    st.markdown(
        """
        - Slay, R. (2023). Altman Z-Score presentation. Instituto Tecnológico y de Estudios Superiores de Occidente (ITESO).
        - Slay, R. (2023). Merton model KMV: An introductory overview of the Merton model. Instituto Tecnológico y de Estudios Superiores de Occidente (ITESO).
        - Altman, E. I. (2000). Predicting financial distress of companies: Revisiting the Z-Score and ZETA® models. Stern School of Business, New York University.
        - Yahoo Finance. (n.d.). Stock market data and financial information. Retrieved February 23, 2026, from https://finance.yahoo.com/
        - OpenAI. (2026). ChatGPT [Large language model]. https://chat.openai.com/chat.
        """)


if __name__ == "__main__":
    main()