from src.context_builder.builder import ContextBuilder
from src.prompt_builder.builder import PromptBuilder
from src.retrieval.retriever import Retriever
from src.vector_store.chroma_store import VectorStore


def main() -> None:

    query = "men polo shirt"

    vector_store = VectorStore()

    retriever = Retriever(vector_store)

    chunks = retriever.retrieve(
        query=query,
        top_k=3,
    )

    context = ContextBuilder().build(chunks)

    prompt = PromptBuilder().build(
        query=query,
        context=context,
    )

    print("=" * 80)
    print("LLM Prompt")
    print("=" * 80)
    print(prompt)


if __name__ == "__main__":
    main()