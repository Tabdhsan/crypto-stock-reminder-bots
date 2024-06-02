from config import COIN_GECKO_API_KEY
import requests


class CustomCoinGeckoApi:
    def __init__(self):
        self.COIN_GECKO_API_KEY = COIN_GECKO_API_KEY

        self.HEADERS = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.COIN_GECKO_API_KEY,
        }

        self.CURRENCY = "usd"

    def get_url_for_crypto_list(self, crypto_list):
        unencoded_string = ",".join(crypto_list)
        encoded_string = requests.utils.quote(unencoded_string)
        return f"https://api.coingecko.com/api/v3/simple/price?vs_currencies={self.CURRENCY}&ids={encoded_string}"

    def get_url(self, crypto_id):
        return f"https://api.coingecko.com/api/v3/simple/price?vs_currencies={self.CURRENCY}&ids={crypto_id}"

    def get_all_crypto_prices(self, crypto_list) -> dict:
        url = self.get_url_for_crypto_list(crypto_list)
        response = requests.get(url)
        data = response.json()
        return data
