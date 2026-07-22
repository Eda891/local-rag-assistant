# scratch/hello_embeddings.py
from sentence_transformers import SentenceTransformer
import numpy as np
model = SentenceTransformer("all-MiniLM-L6-v2")
sentences = [
          "The cat sat on the mat.",
          "A feline rested on the rug.",
          "Python is a programming language.",
]
# Each sentence becomes a 384-number vector.
vectors = model.encode(sentences)
print("Vector shape:", vectors.shape)   # (3, 384)

def cosine_similarity(a, b):
          return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Compare sentence 0 to sentences 1 and 2:
print("cat vs feline :", cosine_similarity(vectors[0], vectors[1]))  # expect HIGH
print("cat vs python :", cosine_similarity(vectors[0], vectors[2]))  # expect LOW