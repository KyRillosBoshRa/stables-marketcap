import requests
import pandas as pd


class StablecoinMarketCap:
    def fetch_market_cap(self):
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=stablecoins"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

        except Exception as e:
            print(f"Error occurred fetching stable coins list: {e}")

        d = []
        for coin in data:
            d.append(
                {
                    "name": coin["name"],
                    "symbol": coin["symbol"],
                    "market_cap": coin["market_cap"],
                    "market_cap_change_24h": coin["market_cap_change_24h"],
                    "market_cap_change_percentage_24h": coin["market_cap_change_percentage_24h"],
                }
            )

        df = pd.DataFrame(d)
        df = df.dropna()
        return df

    def get_market_cap_change(self):
        df = self.fetch_market_cap()

        market_cap_change_usd = df.market_cap_change_24h.sum()
        market_cap_pct = round(market_cap_change_usd / df.market_cap.sum() * 100, 3)

        return market_cap_change_usd, market_cap_pct


def main() -> None:
    stablecoin_marketcap = StablecoinMarketCap()

    df_daily = stablecoin_marketcap.fetch_market_cap()

    print(df_daily)

    market_cap_change_usd, market_cap_pct = stablecoin_marketcap.get_market_cap_change()

    print("total market cap change in usd : " + str(market_cap_change_usd))
    print("total market cap change pct : " + str(market_cap_pct) + "%")


if __name__ == "__main__":
    main()
