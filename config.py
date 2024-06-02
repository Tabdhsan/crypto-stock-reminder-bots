from dotenv import load_dotenv
import os
from tokens import (
    CRYPTO_BOT_TOKEN_FROM_TOKENS,
    CRYPTO_CHAT_ID_FROM_TOKENS,
    STOCK_BOT_TOKEN_FROM_TOKENS,
    STOCK_CHAT_ID_FROM_TOKENS,
    COIN_GECKO_API_KEY_FROM_TOKENS,
)

loaded_path = load_dotenv(".env")

if loaded_path:
    # Retrieve environment variables
    CRYPTO_BOT_TOKEN = os.getenv("CRYPTO_BOT_TOKEN")
    STOCK_BOT_TOKEN = os.getenv("STOCK_BOT_TOKEN")
    CRYPTO_CHAT_ID = os.getenv("CRYPTO_CHAT_ID")
    STOCK_CHAT_ID = os.getenv("STOCK_CHAT_ID")
    COIN_GECKO_API_KEY = os.getenv("COIN_GECKO_API_KEY")


# If the .env file is not loaded, manually set the API keys (This is just to make lambda process easier)
else:
    print("Error loading .env file")
    print("Manually Setting up API Keys")
    CRYPTO_BOT_TOKEN = CRYPTO_BOT_TOKEN_FROM_TOKENS
    STOCK_BOT_TOKEN = STOCK_BOT_TOKEN_FROM_TOKENS
    CRYPTO_CHAT_ID = CRYPTO_CHAT_ID_FROM_TOKENS
    STOCK_CHAT_ID = STOCK_CHAT_ID_FROM_TOKENS
    COIN_GECKO_API_KEY = COIN_GECKO_API_KEY_FROM_TOKENS
