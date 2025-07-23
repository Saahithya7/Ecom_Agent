import sqlite3

conn = sqlite3.connect("db/ecommerce.db")
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in db/ecommerce.db:")
for table in tables:
    print(table[0])
conn.close()