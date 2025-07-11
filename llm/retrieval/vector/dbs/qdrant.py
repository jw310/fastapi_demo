from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct

def connection(collection_name):
    client = QdrantClient("http://localhost:6333")

    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            distance=models.Distance.COSINE,
            size=1536),
        optimizers_config=models.OptimizersConfigDiff(memmap_threshold=20000),
        hnsw_config=models.HnswConfigDiff(on_disk=True, m=16, ef_construct=100)
    )
    return client

def get_collection(client, collection_name):
    return client.get_collection(collection_name)

def upsert_vector(client, collection_name, vectors, data):
    for i, vector in enumerate(vectors):
        client.upsert(
            collection_name=collection_name,
            points=[PointStruct(id=i,
                vector=vectors[i],
                payload=data[i])]
        )

    print("upsert finish")

def search_from_qdrant(client, collection_name, vector, k=1):
    search_result = client.search(
        collection_name=collection_name,
        query_vector=vector,
        limit=k,
        append_payload=True,
    )
    return search_result