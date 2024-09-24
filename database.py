# database.py
import mysql.connector
from config import DB_CONFIG

def connect_to_database():
    return mysql.connector.connect(**DB_CONFIG)

def fetch_mysql_data():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, value, last_updated FROM sync_data")
    mysql_data = {
        row[0]: {"name": row[1], "value": row[2], "last_updated": str(row[3])}
        for row in cursor.fetchall()
    }
    cursor.close()
    connection.close()
    return mysql_data
