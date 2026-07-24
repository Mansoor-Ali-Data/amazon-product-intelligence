"""
Validate the Context Builder.
"""

from __future__ import annotations

from src.context_builder.builder import ContextBuilder
from src.retrieval.retriever import Retriever
from src.vector_store.chroma_store import VectorStore


def main() -> None:

    vector_store = VectorStore()

    retriever = Retriever(vector_store)

    chunks = retriever.retrieve(
        query="men polo shirt",
        top_k=3,
    )

    builder = ContextBuilder()

    context = builder.build(chunks)

    print("=" * 80)
    print("LLM Context")
    print("=" * 80)
    print(context)


if __name__ == "__main__":
    main()