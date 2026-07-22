# scratch/hello_sqlite.py
import sqlite3

# Connect (creates the file if it doesn't exist).
conn = sqlite3.connect("scratch/practice.db")
cur = conn.cursor()

# Create a table. Do this once; IF NOT EXISTS makes it safe to re-run.
cur.execute("""
          CREATE TABLE IF NOT EXISTS notes (
                    id      
                    INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL
          )
          """)

# Insert rows. The ? is a placeholder — ALWAYS use it, never f-strings in SQL.
cur.execute("INSERT INTO notes (content) VALUES (?)", ("Buy milk",))
cur.execute("INSERT INTO notes (content) VALUES (?)", ("Learn RAG",))
conn.commit()   

# commit = actually save to disk
# Read rows back.
cur.execute("SELECT id, content FROM notes")
for row in cur.fetchall():
          print(row)
conn.close()