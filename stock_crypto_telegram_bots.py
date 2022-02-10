# FIXME: TESTING

from bs4 import BeautifulSoup, SoupStrainer
import requests
from datetime import datetime as dt, time
from pytz import timezone

# TELEGRAM CONSTANTS
CRYPTO_BOT_TOKEN = "5087210892:AAGmv8Up5MHuiyt-BVt21lVUh7-KgLvYC54"
CRYPTO_CHAT_ID = "-619492712"
CRYPTO_TELEGRAM_URL = f"https://api.telegram.org/bot{CRYPTO_BOT_TOKEN}/sendMessage"


STOCK_BOT_TOKEN = "5172522415:AAEqnv01yFDyzCN20fXJUUMx1PATlv5sfFs"
STOCK_CHAT_ID = "-646527859"
STOCK_TELEGRAM_URL = f"https://api.telegram.org/bot{STOCK_BOT_TOKEN}/sendMessage"



# Dict containing all stock and crypto options
# FIXME: moe this to gsheets?
STOCK_AND_CRYPTO_DICT = {
    "BTC": {
        "type": "crypto",
        "link": "https://www.marketwatch.com/investing/cryptocurrency/btcusd",
    },
    "SHIBA_INU": {
        "type": "crypto",
        "link": "https://www.marketwatch.com/investing/cryptocurrency/shibusd?iso=kraken&mod=over_search",
    },
    "ATOS": {
        "type": "stock",
        "link": "https://www.marketwatch.com/investing/stock/atos?mod=over_search",
    },
}


# Sends message on Telegram
def telegram_messenger(stock_crypto_name, investment_type, price):
    chat_id = STOCK_CHAT_ID if investment_type == "stock" else CRYPTO_CHAT_ID
    url = STOCK_TELEGRAM_URL if investment_type == "stock" else CRYPTO_TELEGRAM_URL

    # datetime
    time = dt.now(timezone("US/Eastern"))
    dt_string = time.strftime("%m/%d/%Y %H:%M")
    print(f"TELEGRAM_MESSENGER : time rn is {dt_string}")

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

    investment_type = STOCK_AND_CRYPTO_DICT[investment_name]["type"]
    link = STOCK_AND_CRYPTO_DICT[f"{investment_name}"]["link"]

    CURRENT_PRICE = get_current_price(investment_type, link)
    if CURRENT_PRICE != None:
        compare_price_and_send_message(
            CURRENT_PRICE,
            target_price,
            investment_name,
            comparison_type,
            investment_type,
        )


# FIXME: MOVE THESE INTO FUNCTION CALLS
# CRYPTO CONSTANTS
# BTC_target_price = 38500
# SHIBA_target_price = 0.0023
price_getter("ATOS", 5, "lessThan")
