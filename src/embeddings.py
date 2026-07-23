# src/embeddings.py
"""AI layer: text -> vectors. Loads the model once, reuses it."""
from sentence_transformers import SentenceTransformer
from src.config import EMBED_MODEL
_model = None   # module-level cache
def _get_model():
          global _model
          if _model is None:
                    _model = SentenceTransformer(EMBED_MODEL)   # loaded only on first call
          return _model



def embed_text(text: str) -> list[float]:
          """One string -> one vector (as a plain Python list)."""
          return _get_model().encode(text).tolist()
def embed_batch(texts: list[str]) -> list[list[float]]:
          """Many strings -> many vectors. Faster than looping embed_text."""
          return _get_model().encode(texts).tolist()