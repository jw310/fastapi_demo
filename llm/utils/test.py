from llm.retrieval.vector.dbs.qdrant import connection, get_collection, upsert_vector
from llm.retrieval.vector.dbs.faiss import add_to_faiss_index, vector_search
from llm.retrieval.vector.embedding import get_embedding

# print('test')

# qclient = connection('test')

# 1. load data

# sentences = ["我會披星戴月的想你，我會奮不顧身的前進，遠方煙火越來越唏噓，凝視前方身後的距離",
#               "鯊魚寶寶 doo doo doo doo doo doo, 鯊魚寶寶"]

data_objs = [
    {
        "id": 1,
        "lyric": "我會披星戴月的想你，我會奮不顧身的前進，遠方煙火越來越唏噓，凝視前方身後的距離"
    },
    {
        "id": 2,
        "lyric": "而我，在這座城市遺失了你，順便遺失了自己，以為荒唐到底會有捷徑。而我，在這座城市失去了你，輸給慾望高漲的自己，不是你，過分的感情"
    }
]

# 2. spilt documents to chunks


# 3. text to vector  (Embedding)

# embeddings = get_embedding(sentences)

# embeddings_array = []
# for text in data_objs:
#     embeddings_array.append(get_embedding(text['lyric']))

# print(f"embeddings: {embeddings_array}")

# 4. save to  vector db
# faiss_index = add_to_faiss_index(embeddings)

# upsert_vector(qclient, 'test', embeddings_array, data_objs)

# search
# query_text = "昨天"
# query_embedding = get_embedding(query_text)

# search_result = vector_search(faiss_index, query_embedding, sentences, k=3)
# search_result = vector_search(qclient, 'test', query_embedding, k=1)

# print(f"尋找 {query_text}:", search_result)