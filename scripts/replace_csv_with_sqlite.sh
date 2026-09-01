#!/bin/sh
# filepath: scripts/replace_csv_with_sqlite.sh

for file in $(grep -rl --exclude-dir=.venv 'pd.read_csv(' .); do
  # Заменяем чтение zones.sqlite
  sed -i '
    s/pd\.read_csv(\(["'\'']data\/zones\.sqlite["'\''].*\))/import sqlite3\nconn = sqlite3.connect("data\/zones.sqlite")\ndf = pd.read_sql("SELECT * FROM zones", conn)\nconn.close()/g
    s/pd\.read_csv(\(["'\'']data\/risk_allowances\.sqlite["'\''].*\))/import sqlite3\nconn = sqlite3.connect("data\/risk_allowances.sqlite")\ndf = pd.read_sql("SELECT * FROM risk_allowances", conn)\nconn.close()/g
    s/pd\.read_csv(\(["'\'']data\/ets_coefficients\.sqlite["'\''].*\))/import sqlite3\nconn = sqlite3.connect("data\/ets_coefficients.sqlite")\ndf = pd.read_sql("SELECT * FROM ets_coefficients", conn)\nconn.close()/g
  ' "$file"
  echo "Обновлено: $file"
done

echo "Готово."