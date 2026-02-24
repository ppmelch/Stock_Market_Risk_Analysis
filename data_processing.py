from libraries import pd, yf


def download_prices(tickers, interval):
    """Download adjusted close prices for a ticker list and interval."""

    prices = {}

    for ticker in tickers:

        try:
            stock = yf.Ticker(ticker)

            data = stock.history(
                period=interval,
                auto_adjust=True
            )

            if data is None or data.empty:
                print(f"{ticker} history empty")
                continue

            prices[ticker] = data["Close"]

        except Exception as e:
            print(f"{ticker} failed → {e}")

    if not prices:
        print("Yahoo returned empty dataframe")
        return pd.DataFrame()

    return pd.DataFrame(prices)

