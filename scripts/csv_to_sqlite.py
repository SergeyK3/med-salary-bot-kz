import csv
import sqlite3

csv_path = 'data/ets_coefficients.csv'
db_path = 'data/ets_coefficients.sqlite'
table_name = 'ets_coefficients'

with open(csv_path, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    headers = next(reader)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute(f'DROP TABLE IF EXISTS {table_name}')
    columns = ', '.join([f'"{h}" TEXT' for h in headers])
    cur.execute(f'CREATE TABLE {table_name} ({columns})')

    for row in reader:
        cur.execute(f'INSERT INTO {table_name} VALUES ({",".join(["?"]*len(row))})', row)

    conn.commit()
    conn.close()