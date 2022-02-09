# FIXME: TESTING

from bs4 import BeautifulSoup
import requests
from datetime import datetime as dt, time
from pytz import timezone

# TELEGRAM CONSTANTS
CRYPTO_BOT_TOKEN = "5087210892:AAGmv8Up5MHuiyt-BVt21lVUh7-KgLvYC54"
CRYPTO_CHAT_ID = "-619492712"
CRYPTO_TELEGRAM_URL = f"https://api.telegram.org/bot{CRYPTO_BOT_TOKEN}/sendMessage"


STOCK_BOT_TOKEN = "5172522415:AAEqnv01yFDyzCN20fXJUUMx1PATlv5sfF"
STOCK_CHAT_ID = "-646527859"
STOCK_TELEGRAM_URL = f"https://api.telegram.org/bot{STOCK_BOT_TOKEN}/sendMessage"


# Scraping Link Creators
def create_stock_link(ticker):
    BASE_LINK = f"https://finance.yahoo.com/quote/ticker?p=ticker&.tsrc=fin-srch"
    return BASE_LINK.replace("ticker", ticker)


def create_crypto_link(crypto_name):
    BASE_LINK = f"https://coinmarketcap.com/currencies/crypto_name/"
    return BASE_LINK.replace("crypto_name", crypto_name)


# Dict containing all stock and crypto options
STOCK_AND_CRYPTO_DICT = {
    "BTC": {
        "type": "crypto",
        "link": create_crypto_link("bitcoin"),
    },
    "SHIBA_INU": {
        "type": "crypto",
        "link": create_crypto_link("shiba-inu"),
    },
    "ATOS": {
        "type": "stock",
        "link": create_stock_link("ATOS"),
    },
    # BLACKBERRY
    # ASK STEVEN
    # ASK MEG
}


# Sends message on Telegram
def telegram_messenger(stock_crypto_name, price):
    # datetime
    time = dt.now(timezone("US/Eastern"))
    dt_string = time.strftime("%m/%d/%Y %H:%M")
    print(f"TELEGRAM_MESSENGER : time rn is {dt_string}")

    # GET pieces
    MESSAGE = f"{dt_string}---${stock_crypto_name} IS ${price if stock_crypto_name != 'SHIBA_INU' else '{:f}'.format(price)}"
    PARAMS = {"chat_id": CRYPTO_CHAT_ID, "text": f"{MESSAGE}"}

    # GET call
    requests.get(url=CRYPTO_TELEGRAM_URL, params=PARAMS)


# Compares current price to target price based on comparison type given and then calls telegram_messenger if conditions met
def compare_price_and_send_message(
    current_price, target_price, investment_name, comparison_type
):
    if comparison_type == "lessThan" and current_price < target_price:
        telegram_messenger(investment_name, current_price)
    elif comparison_type == "greaterThan" and current_price > target_price:
        telegram_messenger(investment_name, current_price)


# FIXME WORKS FOR EST, NEED TO SEE IF IT WORKS FOR GMT?
def market_open_checker(given_date_time):
    START_TIME = time(9, 30, 0)
    END_TIME = time(15, 45, 0)
    TIME_NOW = given_date_time.time()
    print(f"MARKET OPEN: time now is {TIME_NOW}")

    # Checks if currently the market is open
    # Monday is 1 and Sunday is 7
    if (
        given_date_time.isoweekday() <= 5
        and TIME_NOW >= START_TIME
        and TIME_NOW <= END_TIME
    ):
        return True
    return False


def get_current_price(investment_type, link):
    html_request = requests.get(link).text
    soup = BeautifulSoup(html_request, "html.parser")

    if investment_type == "stock" and market_open_checker(
        dt.now(timezone("US/Eastern"))
    ):
        print(
            f"Market is Open and giventime to test is {dt.now(timezone('US/Eastern'))} "
        )
        my_tags = soup.find_all(
            "fin-streamer", {"class": "Fw(b) Fz(36px) Mb(-4px) D(ib)"}
        )
        CURRENT_PRICE = my_tags[0].contents[0]

    elif investment_type == "crypto":
        my_tags = soup.find_all("div", {"class": "priceValue"})
        CURRENT_PRICE = (
            list(my_tags[0].children)[0].text.replace("$", "").replace(",", "")
        )
    else:
        CURRENT_PRICE = None

    if CURRENT_PRICE != None:
        return float(CURRENT_PRICE)


def price_getter(investment_name, target_price, comparison_type):

    investment_type = STOCK_AND_CRYPTO_DICT[investment_name]["type"]
    link = STOCK_AND_CRYPTO_DICT[f"{investment_name}"]["link"]

    CURRENT_PRICE = get_current_price(investment_type, link)
    if CURRENT_PRICE != None:
        compare_price_and_send_message(
            CURRENT_PRICE, target_price, investment_name, comparison_type
        )


# FIXME: MOVE THESE INTO FUNCTION CALLS
# CRYPTO CONSTANTS
BTC_target_price = 38500
SHIBA_target_price = 0.0023
# price_getter('ATOS', 5, 'lessThan')
price_getter("BTC", 5, "greaterThan")
# print("testing ATOS")
# price_getter("ATOS", 5, "lessThan")

# GIT TEST