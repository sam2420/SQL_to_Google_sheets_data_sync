# google_sheets.py
from config import SHEET_CLIENT, SHEET_ID
from datetime import datetime

def fetch_google_data():
    sheet = SHEET_CLIENT.open_by_key(SHEET_ID).sheet1
    sheet_data = sheet.get_all_values()
    google_data = {
        int(row[0]): {
            "name": row[1],
            "value": row[2],
            "last_updated": row[3]
        }
        for row in sheet_data[1:] if len(row) >= 4 and row[0].isdigit()
    }
    return google_data

def update_google_sheet(row_index, row_data):
    sheet = SHEET_CLIENT.open_by_key(SHEET_ID).sheet1
    cell_range = f"A{row_index}:D{row_index}"
    sheet.update(cell_range, [row_data])
