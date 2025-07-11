import numpy as np
import faiss
import json

def add_to_faiss_index(embeddings):
    # 建立 embeddings 維度陣列
    vector = np.array(embeddings)
    index = faiss.IndexFlatL2(vector.shape[1])
    index.add(vector)
    return index

def vector_search(index, query_embedding, sentences, k=1):
    distances, indices = index.search(
        np.array([query_embedding]), k)
    return [(sentences[i], float(dist)) for dist, i in zip(distances[0], indices[0])]