"""
Validate the end-to-end LLM generation pipeline.
"""

from __future__ import annotations

from src.context_builder.builder import ContextBuilder
from src.llm.client import LLMClient
from src.prompt_builder.builder import PromptBuilder
from src.retrieval.retriever import Retriever
from src.vector_store.chroma_store import VectorStore


def main() -> None:
    """
    Validate the complete retrieval and generation pipeline.
    """

    query = "Recommend a good men's polo shirt."

    # ------------------------------------------------------------------
    # Retrieve relevant chunks
    # ------------------------------------------------------------------

    vector_store = VectorStore()

    retriever = Retriever(vector_store)

    chunks = retriever.retrieve(
        query=query,
        top_k=3,
    )

    # ------------------------------------------------------------------
    # Build context
    # ------------------------------------------------------------------

    context = ContextBuilder().build(chunks)

    # ------------------------------------------------------------------
    # Build prompt
    # ------------------------------------------------------------------

    prompt = PromptBuilder().build(
        query=query,
        context=context,
    )

    # ------------------------------------------------------------------
    # Generate response
    # ------------------------------------------------------------------

    llm = LLMClient()

    answer = llm.generate(prompt)

    # ------------------------------------------------------------------
    # Display response
    # ------------------------------------------------------------------

    print("=" * 80)
    print("LLM Response")
    print("=" * 80)
    print()
    print(answer)


if __name__ == "__main__":
    main()