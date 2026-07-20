from src.vector_store.chroma_store import VectorStore


def main() -> None:
    store = VectorStore()

    print("✅ Vector Store initialized successfully!")
    print(store)


if __name__ == "__main__":
    main()