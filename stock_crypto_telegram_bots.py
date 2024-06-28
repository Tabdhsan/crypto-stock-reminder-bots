from config import CRYPTO_CHAT_ID, STOCK_CHAT_ID
from custom_coin_gecko_api import CustomCoinGeckoApi
from custom_google_sheets_api import CustomGoogleSheetsApi
from datetime import time, datetime as dt

from custom_telegram_api import CustomTelegramApi
from pytz import timezone


class TelegramBots:
    def __init__(self):
        self.json_path = "stock_crypto_creds.json"
        self.sheet_name = "StocksAndCrypto"
        self.STOCK_CHAT_ID = STOCK_CHAT_ID
        self.CRYPTO_CHAT_ID = CRYPTO_CHAT_ID

        self.telegram_wrapper = CustomTelegramApi()
        self.google_sheets_wrapper = CustomGoogleSheetsApi(
            creds_json_file=self.json_path, sheet_name=self.sheet_name
        )
        self.records = self.google_sheets_wrapper.get_all_records()
        self.investment_dict = self.get_investment_dict(self.records)

    # Checks if stock market is open based on daily hours (doesn't acct for edge cases like holidays)
    # This can probably be done via a simple api call but I don't need robust data
    def market_open_checker(given_date_time):
        START_TIME = time(9, 30, 0)
        END_TIME = time(15, 45, 0)
        TIME_NOW = given_date_time.time()

        # Checks if currently the market is open
        # Monday is 1 and Sunday is 7
        if given_date_time.isoweekday() <= 5 and START_TIME <= TIME_NOW <= END_TIME:
            # Market is Open
            return True

        # Market is Closed
        return False

    def get_investment_dict(self, records: dict):
        investment_dict = {}
        for record in records:
            investment_name = record["Investment_Name"]
            if investment_name not in investment_dict:
                investment_dict[investment_name] = []

            condition = {
                "Investment_Type": record["Investment_Type"],
                "Target_Price": record["Target_Price"],
                "Comparison_Type": record["Comparison_Type"],
            }

            investment_dict[investment_name].append(condition)
        return investment_dict

    def get_stock_price(self, investment_name):
        pass

    def get_price_for_all_cryptos(self, crypto_list):
        coin_gecko_api_wrapper = CustomCoinGeckoApi()
        return coin_gecko_api_wrapper.get_all_crypto_prices(crypto_list)

    def is_valid_price(self, current_price, target_price, comparison_type):
        if comparison_type == "lessThan" and current_price < target_price:
            return True
        elif comparison_type == "greaterThan" and current_price > target_price:
            return True
        return False

    def get_dict_by_type(self, investment_type) -> dict:
        filtered_dict = {}
        for key, conditions in self.investment_dict.items():
            filtered_conditions = [
                c for c in conditions if c["Investment_Type"] == investment_type
            ]
            if filtered_conditions:
                filtered_dict[key] = filtered_conditions
        return filtered_dict

    def format_number(self, number):
        if number >= 0.01 or number == 0:
            return f"{number:.4f}"

        # Find the first non-zero digit after the decimal point
        decimal_str = f"{number:.20f}".rstrip("0")
        significant_digits = len(decimal_str) - decimal_str.index(".") - 1
        return f"{number:.{significant_digits}f}"

    def get_dt_string(self):
        time = dt.now(timezone("US/Eastern"))
        return time.strftime("%m/%d/%Y %H:%M")

    def convert_price_to_string(self, price) -> str:

        if price < 0.01:
            return f"{price:.8f}"
        elif price < 1:
            return f"{price:.2f}"
        else:
            return f"{price:.2f}"

    def get_message_text(self, investment_name, price, target_price, comparison_type):
        dt_string = self.get_dt_string()
        price_string = self.format_number(price)
        target_price_string = self.format_number(target_price)
        return f"{dt_string}---${investment_name} IS ${price_string} | Condition: {comparison_type} {target_price_string}"

    def send_crypto_messages(self):
        crypto_dict = self.get_dict_by_type("crypto")

        crypto_list = list(crypto_dict.keys())

        crypto_prices = self.get_price_for_all_cryptos(crypto_list)

        for crypto_name, conditions in crypto_dict.items():
            current_price = crypto_prices[crypto_name.lower()]["usd"]

            for condition in conditions:
                target_price = condition["Target_Price"]
                comparison_type = condition["Comparison_Type"]

                # Do a price comparison
                is_valid_price = self.is_valid_price(
                    current_price,
                    target_price,
                    comparison_type,
                )

                # Send a message
                if is_valid_price is True:
                    message_text = self.get_message_text(
                        crypto_name, current_price, target_price, comparison_type
                    )

                    self.telegram_wrapper.send_message("crypto", message_text)

                    print(f"SENDING CRYPTO MSG NOW for {crypto_name}")
                else:
                    print(f"NO CRYPTO MSG for {crypto_name}")
