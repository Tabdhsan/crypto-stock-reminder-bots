from datetime import datetime as dt
from datetime import time

import gspread
import requests
from bs4 import BeautifulSoup, SoupStrainer
from oauth2client.service_account import ServiceAccountCredentials
from pytz import timezone

from tokens import CRYPTO_BOT_TOKEN, CRYPTO_CHAT_ID, STOCK_BOT_TOKEN, STOCK_CHAT_ID

# TELEGRAM CONSTANTS

CRYPTO_TELEGRAM_URL = f"https://api.telegram.org/bot{CRYPTO_BOT_TOKEN}/sendMessage"

STOCK_TELEGRAM_URL = f"https://api.telegram.org/bot{STOCK_BOT_TOKEN}/sendMessage"


def lambda_handler(event, context):
    # GSheets Initialization
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "stock_crypto_creds.json", scope
    )

    client = gspread.authorize(creds)
    spreadsheet = client.open("StocksAndCrypto").sheet1

    # Gets all rows and columns as a dictionary from google sheets
    data = spreadsheet.get_all_records()

    # Dict containing all stock and crypto options
    investment_dict = {}
    for i in data:
        # Turns the 'Investment_Name' column from gsheets to the key of a new dictionary with the old keys as values
        investment_name = i["Investment_Name"]
        del i["Investment_Name"]
        investment_dict[investment_name] = i

    # Sends message on Telegram
    def telegram_messenger(stock_crypto_name, investment_type, price):
        chat_id = STOCK_CHAT_ID if investment_type == "stock" else CRYPTO_CHAT_ID
        url = STOCK_TELEGRAM_URL if investment_type == "stock" else CRYPTO_TELEGRAM_URL

        # datetime
        time = dt.now(timezone("US/Eastern"))
        dt_string = time.strftime("%m/%d/%Y %H:%M")

        # GET pieces
        MESSAGE = f"{dt_string}---${stock_crypto_name} IS ${price if stock_crypto_name != 'SHIBA_INU' else '{:f}'.format(price)}"
        PARAMS = {"chat_id": chat_id, "text": f"{MESSAGE}"}

        # GET call
        requests.get(url=url, params=PARAMS)

    # Compares current price to target price based on comparison type given and then calls telegram_messenger if conditions met
    def compare_price_and_send_message(
        current_price, target_price, investment_name, comparison_type, investment_type
    ):
        if comparison_type == "lessThan" and current_price < target_price:
            telegram_messenger(investment_name, investment_type, current_price)
        elif comparison_type == "greaterThan" and current_price > target_price:
            telegram_messenger(investment_name, investment_type, current_price)

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

    def get_current_price(investment_type, link):
        html_request = requests.get(link).text
        parse_conditions = SoupStrainer("h2", attrs={"class": "intraday__price "})

        if (
            investment_type == "stock"
            and market_open_checker(dt.now(timezone("US/Eastern"))) == False
        ):
            return None

        soup = BeautifulSoup(html_request, "html.parser", parse_only=parse_conditions)
        current_price = soup.find("bg-quote").text.replace(",", "")
        return float(current_price)

    def price_getter(investment_name, target_price, comparison_type):
        investment_type = investment_dict[investment_name]["Investment_Type"]
        link = investment_dict[f"{investment_name}"]["Link"]

        CURRENT_PRICE = get_current_price(investment_type, link)

        if CURRENT_PRICE != None:
            compare_price_and_send_message(
                CURRENT_PRICE,
                target_price,
                investment_name,
                comparison_type,
                investment_type,
            )

    for key, value in investment_dict.items():
        raw_target_price = value["Target_Price"]
        if type((raw_target_price)) == float:
            target_price = raw_target_price
        elif type((raw_target_price)) == str:
            target_price = float(raw_target_price.replace(",", ""))
        # target_price = float(value["Target_Price"].replace(",",""))
        comparison_type = value["Comparison_Type"]
        price_getter(key, target_price, comparison_type)
