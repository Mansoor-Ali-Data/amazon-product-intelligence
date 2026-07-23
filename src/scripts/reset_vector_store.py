from src.vector_store.chroma_store import VectorStore

def main() -> None:
    vector_store = VectorStore()

    vector_store.reset()

    print("✅ Vector store reset successfully.")

if __name__ == "__main__":
    main()