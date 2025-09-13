import sqlite3

conn = sqlite3.connect('data/ets_coefficients.db')  # или .sqlite
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print('Таблицы:', cursor.fetchall())  # Должен вывести список таблиц

cursor.execute("SELECT * FROM ets_coefficients LIMIT 5;")
print('Строки:', cursor.fetchall())  # Должны быть строки из таблицы

conn.close()