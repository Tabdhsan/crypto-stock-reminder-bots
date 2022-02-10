from bs4 import BeautifulSoup, SoupStrainer
import requests
from datetime import datetime as dt, time
from pytz import timezone
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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

# Gets all rows and columns as a dictionary
data = spreadsheet.get_all_records()

# Dict containing all stock and crypto options
investment_dict = {}
for i in data:
    # Turns the 'Investment_Name' column from gsheets to the key of a new dictionary with the old keys as values
    investment_name = i["Investment_Name"]
    del i["Investment_Name"]
    investment_dict[investment_name] = i

# TELEGRAM CONSTANTS
CRYPTO_BOT_TOKEN = "5087210892:AAGmv8Up5MHuiyt-BVt21lVUh7-KgLvYC54"
CRYPTO_CHAT_ID = "-619492712"
CRYPTO_TELEGRAM_URL = f"https://api.telegram.org/bot{CRYPTO_BOT_TOKEN}/sendMessage"


STOCK_BOT_TOKEN = "5172522415:AAEqnv01yFDyzCN20fXJUUMx1PATlv5sfFs"
STOCK_CHAT_ID = "-646527859"
STOCK_TELEGRAM_URL = f"https://api.telegram.org/bot{STOCK_BOT_TOKEN}/sendMessage"


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
    if (
        given_date_time.isoweekday() <= 5
        and TIME_NOW >= START_TIME
        and TIME_NOW <= END_TIME
    ):
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
    target_price = value["Target_Price"]
    comparison_type = value["Comparison_Type"]
    price_getter(key, target_price, comparison_type)
