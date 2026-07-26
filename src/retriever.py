"""Logic layer: find the chunks most relevant to a query."""
import numpy as np
from src.config import TOP_K
from src.database import get_all_chunks
from src.embeddings import embed_text


def _cosine(a, b) -> float:
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def get_top_chunks(query: str, k: int = TOP_K, min_score: float = 0.3) -> list[dict]:
    """Return the k chunks whose embeddings are closest to the query,
    filtering out anything below min_score (not actually relevant)."""
    query_vec = embed_text(query)
    chunks = get_all_chunks()

    for chunk in chunks:
        chunk["score"] = _cosine(query_vec, chunk["embedding"])

    chunks.sort(key=lambda c: c["score"], reverse=True)

    print("Top candidate scores:", [round(c["score"], 3) for c in chunks[:5]])

    relevant = [c for c in chunks if c["score"] >= min_score]
    return relevant[:k]