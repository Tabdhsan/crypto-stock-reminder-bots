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

    # Gets all rows and columns as a dictionary from google sheets
    def get_all_records(self) -> dict:
        return self.spreadsheet.get_all_records()
