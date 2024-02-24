import requests
import time
import sqlite3
import os
from dotenv import load_dotenv

def create_table_if_not_exists(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS response_times (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            unix_timestamp INT,
            response_time_ms REAL,
            payload_bytes INT,
            is_up BOOLEAN
        )
    ''')
    conn.commit()


def insert_result_to_db(
    conn: sqlite3.Connection,
    timestamp: str,
    unix_timestamp: int,
    response_time_ms: float,
    payload_bytes: int,
    is_up: bool
) -> None:
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO response_times (timestamp, unix_timestamp, response_time_ms, payload_bytes, is_up)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, unix_timestamp, response_time_ms, payload_bytes, is_up))
    conn.commit()


def measure_and_store_response_time(api_url: str, conn: sqlite3.Connection):
    try:
        start_time = time.time()
        response = requests.get(api_url,timeout=59)
        end_time = time.time()
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')  # Current timestamp in the format 'YYYY-MM-DD HH:MM:SS'
        timestamp_struct = time.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        unix_timestamp = time.mktime(timestamp_struct)
        response_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
        is_up = True if 200 <= response.status_code < 300 else False
        payload_bytes = len(response.content)
        print(f"Response time: {response_time_ms:.2f} ms, payload {payload_bytes} bytes")
        insert_result_to_db(conn, timestamp, unix_timestamp, response_time_ms, payload_bytes, is_up)

    except requests.RequestException as e:
        print(f"Error: {e}")


def main() -> None:
    load_dotenv()
    api_url = os.getenv('API_URL')
    conn = sqlite3.connect('response_times.db')
    create_table_if_not_exists(conn)
    measure_and_store_response_time(api_url, conn)
    conn.close()


if __name__ == "__main__":
    main()
