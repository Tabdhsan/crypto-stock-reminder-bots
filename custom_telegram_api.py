from config import CRYPTO_BOT_TOKEN, CRYPTO_CHAT_ID, STOCK_BOT_TOKEN, STOCK_CHAT_ID

import requests


class CustomTelegramApi:
    def __init__(self):
        self.CRYPTO_BOT_TOKEN = CRYPTO_BOT_TOKEN
        self.CRYPTO_CHAT_ID = CRYPTO_CHAT_ID
        self.STOCK_BOT_TOKEN = STOCK_BOT_TOKEN
        self.STOCK_CHAT_ID = STOCK_CHAT_ID

    def get_base_url_by_type(self, type):
        token = self.CRYPTO_BOT_TOKEN if type == "crypto" else self.STOCK_BOT_TOKEN

        return f"https://api.telegram.org/bot{token}/sendMessage"

    def send_message(self, type, text):
        chat_id = self.CRYPTO_CHAT_ID if type == "crypto" else self.STOCK_CHAT_ID

        url = self.get_base_url_by_type(type)
        params = {"chat_id": chat_id, "text": text}

        requests.get(url=url, params=params)
