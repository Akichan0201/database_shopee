import os
import gspread

from google.oauth2.service_account import Credentials


def service_account(SHEET_ID, SERVICE_ACC)->gspread.worksheet.Worksheet:
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    creds = Credentials.from_service_account_file(
        SERVICE_ACC,
        scopes=SCOPES
    )

    gc = gspread.authorize(creds)
    worksheet = gc.open_by_key(SHEET_ID).worksheet("Sheet1")
    
    return worksheet