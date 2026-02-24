from altman import Altman
from merton import Merton
from financial_statements import Companies
from libraries import plt, st , pd 
from visualization import plot_altman, plot_merton_dd, plot_pd


@st.cache_resource
def load_companies(tickers, interval):

    companies = Companies(tickers, interval)

    _ = companies.balance_sheets
    _ = companies.income_statements
    _ = companies.market_data
    _ = companies.prices

    return companies


def main():

    st.title("📊 Stock Market Risk Analysis")
    st.markdown("Altman Z-Score & Merton Model")
    st.markdown("José Armando Melchor Soto - 745697")
    st.markdown("---")

    col1, col2, col3 = st.columns([4,2,1])

    with col1:
        raw_tickers = st.text_input(
            "Tickers",
            value="V, MA, BA, F"
        )

    with col2:
        interval = st.selectbox(
            "Interval",
            ["6mo","1y","2y","5y","10y"]
        )

    with col3:
        st.write("")
        st.write("")
        run_analysis = st.button("Run", type="primary")

    if run_analysis:

        tickers = [
            t.strip().upper()
            for t in raw_tickers.split(",")
        ]

        with st.spinner("Downloading data..."):

            companies = load_companies(
                tuple(tickers),
                interval
            )

            if companies.prices.empty:
                st.error("⚠️ Yahoo returned no price data.")
                return

            st.session_state["companies"] = companies

    if "companies" not in st.session_state:
        return

    companies = st.session_state["companies"]

    # ================= ALTAMN =================
    st.header("Altman Z-Score")

    altman = Altman(companies)
    z_df = altman.z_scores_df().dropna()

    if not z_df.empty:
        st.dataframe(z_df)
        plot_altman(z_df)

    # ================= MERTON =================
    st.header("Merton Model")

    merton = Merton(companies)
    merton_df = merton.merton_df().dropna()

    if merton_df.empty:
        st.warning("⚠️ No valid Merton results.")
        return

    st.dataframe(merton_df)

    colA, colB = st.columns(2)

    with colA:
        plot_merton_dd(merton_df)

    with colB:
        plot_pd(merton_df)


if __name__ == "__main__":
    main()