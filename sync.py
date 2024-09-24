# sync.py
from datetime import datetime
from google_sheets import fetch_google_data, update_google_sheet
from database import fetch_mysql_data, connect_to_database
from config import SHEET_CLIENT, SHEET_ID
def normalize_date_format(date_str):
    try:
        parsed_date = datetime.strptime(date_str, "%m/%d/%Y")
    except ValueError:
        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValueError(f"Unrecognized date format: {date_str}")
    return parsed_date.strftime("%Y-%m-%d %H:%M:%S")

def data_has_changed(old_data, new_data):
    return old_data != new_data

def bidirectional_sync():
    previous_google_data = {}
    google_data = fetch_google_data()
    mysql_data = fetch_mysql_data()

    changes_detected = False
    connection = connect_to_database()
    cursor = connection.cursor()

    for id in set(google_data.keys()).union(mysql_data.keys()):
        g_entry = google_data.get(id)
        m_entry = mysql_data.get(id)

        if g_entry and not m_entry:
            query = "INSERT INTO sync_data (id, name, value, last_updated) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (id, g_entry["name"], g_entry["value"], g_entry["last_updated"]))
            changes_detected = True

        elif m_entry and not g_entry:
            query = "DELETE FROM sync_data WHERE id=%s"
            cursor.execute(query, (id,))
            changes_detected = True

        elif g_entry and m_entry:
            g_timestamp = datetime.strptime(g_entry["last_updated"], '%Y-%m-%d %H:%M:%S')
            m_timestamp = datetime.strptime(m_entry["last_updated"], '%Y-%m-%d %H:%M:%S')

            if g_timestamp > m_timestamp:
                query = "UPDATE sync_data SET name=%s, value=%s, last_updated=%s WHERE id=%s"
                cursor.execute(query, (g_entry["name"], g_entry["value"], g_entry["last_updated"], id))
                changes_detected = True
            elif m_timestamp > g_timestamp:
                row_index = list(google_data.keys()).index(id) + 2
                update_google_sheet(row_index, [id, m_entry["name"], m_entry["value"], m_entry["last_updated"]])
                changes_detected = True

    connection.commit()
    cursor.close()
    connection.close()

    if changes_detected:
        print("Sync completed with changes.")
    else:
        print("No changes detected.")

def bidirectional_sync_mysql_priority():
    previous_google_data = {}
    google_data = fetch_google_data()
    mysql_data = fetch_mysql_data()

    changes_detected = False
    connection = connect_to_database()
    cursor = connection.cursor()

    for id in set(google_data.keys()).union(mysql_data.keys()):
        g_entry = google_data.get(id)
        m_entry = mysql_data.get(id)

        if g_entry and not m_entry:
            query = "INSERT INTO sync_data (id, name, value, last_updated) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (id, g_entry["name"], g_entry["value"], g_entry["last_updated"]))
            changes_detected = True

        elif m_entry and not g_entry:
            new_google_row = [id, m_entry["name"], m_entry["value"], m_entry["last_updated"]]
            sheet = SHEET_CLIENT.open_by_key(SHEET_ID).sheet1
            sheet.append_row(new_google_row)
            changes_detected = True

        elif g_entry and m_entry:
            g_timestamp = datetime.strptime(g_entry["last_updated"], '%Y-%m-%d %H:%M:%S')
            m_timestamp = datetime.strptime(m_entry["last_updated"], '%Y-%m-%d %H:%M:%S')

            if g_timestamp > m_timestamp:
                query = "UPDATE sync_data SET name=%s, value=%s, last_updated=%s WHERE id=%s"
                cursor.execute(query, (g_entry["name"], g_entry["value"], g_entry["last_updated"], id))
                changes_detected = True
            elif m_timestamp > g_timestamp:
                row_index = list(google_data.keys()).index(id) + 2
                update_google_sheet(row_index, [id, m_entry["name"], m_entry["value"], m_entry["last_updated"]])
                changes_detected = True

    connection.commit()
    cursor.close()
    connection.close()

    if changes_detected:
        print("Sync completed with changes.")
    else:
        print("No changes detected.")
