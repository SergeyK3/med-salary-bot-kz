import csv
import sqlite3

csv_path = 'data/ets_coefficients.csv'
db_path = 'data/ets_coefficients.sqlite'
table_name = 'ets_coefficients'

try:
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        print('Заголовки:', headers)

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        cur.execute(f'DROP TABLE IF EXISTS {table_name}')
        columns = ', '.join([f'"{h}" TEXT' for h in headers])
        print('Создаём таблицу с колонками:', columns)
        cur.execute(f'CREATE TABLE {table_name} ({columns})')

        row_count = 0
        for row in reader:
            cur.execute(f'INSERT INTO {table_name} VALUES ({",".join(["?"]*len(row))})', row)
            row_count += 1

        conn.commit()
        conn.close()

        print(f'Таблица {table_name} успешно создана, вставлено строк: {row_count}')

except Exception as e:
    print('Ошибка:', e)