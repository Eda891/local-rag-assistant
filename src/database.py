# src/database.py
"""Data layer: the ONLY place that talks to SQLite."""
import json
import sqlite3
from src.config import DB_PATH

def _connect():
    return sqlite3.connect(DB_PATH)

def init_db():
    """Create the chunks table if it doesn't exist."""
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                source    TEXT NOT NULL,      -- which document this came from
                content   TEXT NOT NULL,      -- the chunk text
                embedding TEXT NOT NULL       -- the vector, JSON-encoded
            )
        """)

def insert_chunk(source: str, content: str, embedding: list[float]):
    """Save one chunk + its vector. The vector becomes JSON text."""
    with _connect() as conn:
        conn.execute(
            "INSERT INTO chunks (source, content, embedding) VALUES (?, ?, ?)",
            (source, content, json.dumps(embedding)),
        )

def get_all_chunks() -> list[dict]:
    """Return every chunk as a dict: {source, content, embedding(list)}."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT source, content, embedding FROM chunks")
    rows = cursor.fetchall()
    conn.close()

    chunks = []
    for source, content, embedding_json in rows:
        chunks.append({
            "source": source,
            "content": content,
            "embedding": json.loads(embedding_json),
        })
    return chunks