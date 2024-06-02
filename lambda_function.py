from stock_crypto_telegram_bots import TelegramBots


def lambda_handler(event, context):
    telegram_bots = TelegramBots()
    telegram_bots.send_crypto_messages()
