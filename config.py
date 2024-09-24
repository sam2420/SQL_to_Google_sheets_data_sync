# config.py
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets configuration
SHEET_ID = "1APMVWfnGoS31pp3dBFfXbN7k260i2M8Q5Y2cpYXjClA"
CREDENTIALS_FILE = "credentials.json"

# MySQL configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Sami@2003",
    "database": "superjoinai"
}

# Google Sheets client setup
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
SHEET_CLIENT = gspread.authorize(CREDS)
