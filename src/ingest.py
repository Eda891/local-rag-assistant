# src/ingest.py
"""Read docs -> chunk -> embed -> store. Run this once to build the knowledge base."""
from src.config import DOCS_DIR
from src.database import init_db, insert_chunk
from src.embeddings import embed_batch
from src.chunking import chunk_text

def ingest():
          init_db()
          doc_files = list(DOCS_DIR.glob("*.txt"))
          print(f"Found {len(doc_files)} documents.")
          
          for path in doc_files:
                    text = path.read_text(encoding="utf-8")
                    chunks = chunk_text(text)
                    vectors = embed_batch(chunks)          
                    # embed all chunks of this doc at once
                    for chunk, vector in zip(chunks, vectors):
                              insert_chunk(source=path.name, content=chunk, embedding=vector)
                    print(f"  {path.name}: {len(chunks)} chunks stored")
          print("Ingestion complete.")
if __name__ == "__main__":
          ingest()