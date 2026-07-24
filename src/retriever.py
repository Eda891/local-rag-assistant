# src/retriever.py
"""Logic layer: find the chunks most relevant to a query."""
import numpy as np
from src.config import TOP_K
from src.database import get_all_chunks
from src.embeddings import embed_text

def _cosine(a, b) -> float:
          a, b = np.array(a), np.array(b)
          return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
def get_top_chunks(query: str, k: int = TOP_K) -> list[dict]:
          """Return the k chunks whose embeddings are closest to the query."""
          query_vec = embed_text(query)
          chunks = get_all_chunks()


def get_top_chunks(query: str, k: int = TOP_K) -> list[dict]:
    """Return the k chunks whose embeddings are closest to the query."""
    query_vec = embed_text(query)
    chunks = get_all_chunks()

    for chunk in chunks:
        chunk["score"] = _cosine(query_vec, chunk["embedding"])

    chunks.sort(key=lambda c: c["score"], reverse=True)

    return chunks[:k]

pass