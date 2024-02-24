import csv
import sqlite3

def export_table_to_csv(conn: sqlite3.Connection, filename: str) -> None:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM response_times')

    # Fetch all rows from the table
    data = cursor.fetchall()

    # Export data to CSV
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['id', 'timestamp', 'unix_timestamp', 'response_time_ms', 'payload_bytes', 'is_up'])
        csv_writer.writerows(data)


if __name__ == "__main__":
    conn = sqlite3.connect('response_times.db')
    export_table_to_csv(conn, 'output.csv')
