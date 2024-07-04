from oauth2client.service_account import ServiceAccountCredentials
import gspread


class CustomGoogleSheetsApi:
    def __init__(self, creds_json_file: str, sheet_name: str):
        self.scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
        ]

        creds = ServiceAccountCredentials.from_json_keyfile_name(
            creds_json_file, self.scope
        )

        self.client = gspread.authorize(creds)

        self.sheet_name = sheet_name

        self.spreadsheet = self.client.open(self.sheet_name).sheet1
        self.headers = self.spreadsheet.row_values(1)  # Get the headers
        self.time_col = self.headers.index("Prev_Msg_Time") + 1
        self.price_col = self.headers.index("Prev_Msg_Price") + 1

    def get_all_records(self) -> dict:
        return self.spreadsheet.get_all_records()

    def update_time_and_price(self, row_number, time, price):
        self.spreadsheet.update_cell(row_number, self.time_col, time)
        self.spreadsheet.update_cell(row_number, self.price_col, price)
        print(f"Updated time and price for row {row_number} to {time} and {price}.")
