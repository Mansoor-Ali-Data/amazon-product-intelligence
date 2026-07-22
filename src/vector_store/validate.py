from src.embeddings.models import EmbeddedChunk
from src.vector_store.builder import VectorStoreBuilder
from src.vector_store.chroma_store import VectorStore


def main() -> None:
    embedded_chunk = EmbeddedChunk(
        id="chunk_001",
        text="This is a sample chunk.",
        embedding=[0.1, 0.2, 0.3],
        metadata={
            "asin": "B001",
            "chunk_index": 0,
        },
    )

    batch = VectorStoreBuilder().build(
        embedded_chunks=[embedded_chunk],
    )

    vector_store = VectorStore()

    vector_store.add_documents(
        ids=batch.ids,
        documents=batch.documents,
        embeddings=batch.embeddings,
        metadatas=batch.metadatas,
    )

    print("✅ VectorStore insertion successful!")


if __name__ == "__main__":
    main()