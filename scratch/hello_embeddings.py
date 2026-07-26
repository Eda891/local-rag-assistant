from sentence_transformers import SentenceTransformer
import numpy as np
model = SentenceTransformer("all-MiniLM-L6-v2")
sentences = [
          "The cat sat on the mat.",
          "A feline rested on the rug.",
          "Python is a programming language.",
]
vectors = model.encode(sentences)
print("Vector shape:", vectors.shape)   

def cosine_similarity(a, b):
          return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print("cat vs feline :", cosine_similarity(vectors[0], vectors[1]))  
print("cat vs python :", cosine_similarity(vectors[0], vectors[2]))  