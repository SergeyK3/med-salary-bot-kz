import csv
import sqlite3

csv_path = 'data/zones.csv'
db_path = 'data/zones.sqlite'
table_name = 'zones'

with open(csv_path, newline='', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';')
    headers = next(reader)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute(f'DROP TABLE IF EXISTS {table_name}')
    columns = ', '.join([f'"{h}" TEXT' for h in headers])
    cur.execute(f'CREATE TABLE {table_name} ({columns})')

    row_count = 0
    for row in reader:
        cur.execute(f'INSERT INTO {table_name} VALUES ({",".join(["?"]*len(row))})', row)
        row_count += 1

    conn.commit()
    conn.close()

print(f'Таблица {table_name} успешно создана, вставлено строк: {row_count}')