import sqlite3

conn = sqlite3.connect("data/zones.sqlite")
cur = conn.cursor()
# Оставляем только одну строку с code='none'
cur.execute("""
    DELETE FROM zones
    WHERE code = 'none'
    AND rowid NOT IN (
        SELECT MIN(rowid) FROM zones WHERE code = 'none'
    )
""")
conn.commit()
conn.close()