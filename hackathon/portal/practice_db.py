import sqlite3

db = sqlite3.connect("practice.db")

db.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)")

db.execute("INSERT INTO notes (text) VALUES (?)", ("buy milk",))
db.execute("INSERT INTO notes (text) VALUES (?)", ("finish homework",))
db.commit()

for row in db.execute("SELECT * FROM notes"):
    print(row)
print(db.execute("SELECT * FROM notes WHERE id = 2").fetchone())