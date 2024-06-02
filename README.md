# Stock and Crypto Trade Assist

The **Stock and Crypto Trade Assist** is a Python program designed to fetch real-time price data for stocks and cryptocurrencies from various sources, compare them with predefined target prices and comparison types, and send notifications via Telegram to specified chats when the conditions are met.

This program utilizes the following technologies and APIs:

-   **Python**: The programming language used to write the script.
-   **Google Sheets API**: Used to retrieve information from a Google Sheet containing target prices and comparison types.
-   **Coin Gecko API**: Employed to get realtime crypto data.
-   **Telegram API**: Utilized to send notifications to specified Telegram chats.
-   **AWS Lambda**: The code is in the form of a lambda handler so it can easily be put into AWS Lambda and used alongside Cloudwatch for logging and EventBridge for scheduling.

## Features

1. **Data Retrieval**: The program fetches real-time price data for stocks (when the market is open) and cryptocurrencies from reliable sources.

2. **Google Sheets Integration**: The target prices and comparison types are stored in a Google Sheet. The program uses the Google Sheets API to retrieve this information.

3. **Price Comparison**: The fetched current prices are compared against the predefined target prices based on the specified comparison type (e.g., greater than, less than, equal to).

4. **Telegram Notifications**: If the price conditions match, the program sends notifications to designated Telegram chats, containing the current price and relevant details.

5. **Ready to go For AWS Use**: The code is in the form of a lambda handler so it can easily be put into AWS Lambda and used alongside Cloudwatch for logging and EventBridge for scheduling.

## Setup

1. **Install Dependencies**: Make sure you have the required Python libraries installed. You can install them using the following command:

    ```bash
    pip install google-api-python-client requests
    ```

2. **Google Sheets API Setup**:

-   Follow the instructions provided by Google to set up the Google Sheets API and obtain credentials.
-   Replace the `credentials.json` file with your own credentials.
-   Update the `SPREADSHEET_ID` in the script with the ID of your Google Sheet.

3. **Telegram API Setup**:

-   Create a new bot on Telegram and obtain the bot token.
-   Replace `YOUR_BOT_TOKEN` in the script with your actual bot token.
-   Obtain the chat ID of the chat where you want to receive notifications. You can use tools like [userinfobot](https://core.telegram.org/bots#botfather) to find your chat ID.
-   Replace `YOUR_CHAT_ID` in the script with your actual chat ID.

4. **Stocks and Crypto Price Scraping**:

-   Identify reliable sources for fetching real-time price data for stocks and cryptocurrencies.
-   Implement REST API Calls to get accurate price data

5. **Define Target Prices and Comparison Types**:

-   Set up a Google Sheet containing columns for the stock/cryptocurrency name, target price, and comparison type.
-   Populate this sheet with the relevant information.

## Usage

1. Run the Python script using the following command:

```bash
python lambda_function.py
```

2. The script will fetch current price data, compare it against target prices, and send notifications via Telegram when the conditions are met.

## Important Notes

-   Env setup is done via the `os` module. This is to ensure that the code can be easily deployed to AWS Lambda without having to hardcode any sensitive information.

-   The code is in the form of a lambda handler so it can easily be put into AWS Lambda and used alongside Cloudwatch for logging and EventBridge for scheduling.

-   Handle errors and exceptions gracefully to avoid unexpected crashes of the script.

-   Regularly update your credentials and tokens and keep them secure.

-   This program serves as a basic guide and can be expanded upon for more features and enhancements.

## Disclaimer

This program is intended for educational and informational purposes only. Use it responsibly and in accordance with relevant laws and regulations. The program might involve scraping data from third-party sources, which might have their own terms of use and legal considerations. Make sure you understand and respect these terms.
