from src.embeddings.models import EmbeddedChunk
from src.vector_store.builder import VectorStoreBuilder
from src.vector_store.chroma_store import VectorStore

from config.loader import load_yaml
from src.embeddings.embedder import embed_texts

def main() -> None:
    text="This is a sample chunk.",
    embedded_chunk = EmbeddedChunk(
        id="chunk_001",
        embedding = embed_texts([text])[0],
        metadata={
            "asin": "B001",
            "chunk_index": 0,
        },
    )

    batch = VectorStoreBuilder().build(
        embedded_chunks=[embedded_chunk],
    )

    config = load_yaml("vector_store.yaml")

    vector_store = VectorStore(
        collection_name=config["vector_store"][
            "validation_collection_name"
        ],
    )

    vector_store.add_documents(
        ids=batch.ids,
        documents=batch.documents,
        embeddings=batch.embeddings,
        metadatas=batch.metadatas,
    )

    print("✅ VectorStore insertion successful!")


if __name__ == "__main__":
    main()