# watchdog.py
import time
from google_sheets import fetch_google_data
from database import fetch_mysql_data
from sync import bidirectional_sync, bidirectional_sync_mysql_priority, data_has_changed

def monitor_changes(interval=5):
    last_google_data = fetch_google_data()
    last_mysql_data = fetch_mysql_data()

    while True:
        current_google_data = fetch_google_data()
        if data_has_changed(last_google_data, current_google_data):
            print("Google Sheets data changed. Running sync...")
            bidirectional_sync()
            last_google_data = current_google_data

        current_mysql_data = fetch_mysql_data()
        if data_has_changed(last_mysql_data, current_mysql_data):
            print("MySQL data changed. Running sync...")
            bidirectional_sync_mysql_priority()
            last_mysql_data = current_mysql_data

        time.sleep(interval)

if __name__ == "__main__":
    monitor_changes(interval=5)
