import sqlite3

conn = sqlite3.connect("data/zones.sqlite")
cur = conn.cursor()
cur.execute("""
    INSERT INTO zones (code, name, calc_base, value, notes)
    VALUES ('none', 'Экологически благополучная зона', NULL, 0.0, 'Нет экологического неблагополучия')
""")
conn.commit()
conn.close()