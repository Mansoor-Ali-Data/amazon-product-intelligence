from src.vector_store.chroma_store import VectorStore

vs = VectorStore()
print(vs._client.get_max_batch_size())
