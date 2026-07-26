
import sqlite3

conn = sqlite3.connect("scratch/practice.db")
cur = conn.cursor()
cur.execute("""
          CREATE TABLE IF NOT EXISTS notes (
                    id      
                    INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL
          )
          """)

cur.execute("INSERT INTO notes (content) VALUES (?)", ("Buy milk",))
cur.execute("INSERT INTO notes (content) VALUES (?)", ("Learn RAG",))
conn.commit()   

cur.execute("SELECT id, content FROM notes")
for row in cur.fetchall():
          print(row)
conn.close()