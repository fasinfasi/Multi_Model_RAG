"""FAISS vector store builder.

This module builds an in-memory FAISS index from embeddings computed in
`backend.embedding`. It's imported by `backend.response` to perform k-NN
searches. No CLI — used programmatically by the frontend.
"""

import faiss
import numpy as np
import embedding

dimension = len(embedding.embeddings[0])

index = faiss.IndexFlatL2(dimension)

embeddings_array = np.vstack([emb for emb in embedding.embeddings if len(emb) == len(embedding.embeddings[0])])

index.add(embeddings_array)

print(f"FAISS index contains {index.ntotal} vectors")

