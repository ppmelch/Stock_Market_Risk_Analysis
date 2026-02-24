from libraries import pd, yf


def download_prices(tickers, interval):

    prices = {}

    for ticker in tickers:

        try:
            stock = yf.Ticker(ticker)

            data = stock.history(
                period=interval,
                auto_adjust=True
            )

            if data is None or data.empty:
                print(f"⚠️ {ticker} history empty")
                continue

            prices[ticker] = data["Close"]

        except Exception as e:
            print(f"⚠️ {ticker} failed → {e}")

    # ✅ NEVER CRASH
    if not prices:
        print("⚠️ Yahoo returned empty dataframe")
        return pd.DataFrame()

    return pd.DataFrame(prices)

