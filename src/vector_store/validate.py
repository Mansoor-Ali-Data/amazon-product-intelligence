from src.vector_store.chroma_store import VectorStore


def main() -> None:
    store = VectorStore()

    print(f"Documents: {store.count()}")

    print(store.peek())


if __name__ == "__main__":
    main()