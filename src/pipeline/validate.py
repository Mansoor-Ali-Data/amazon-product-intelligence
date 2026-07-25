"""
Validate the end-to-end RAG pipeline.

This validation script executes each stage of the pipeline separately,
allowing intermediate outputs to be inspected before the final LLM
response is generated.
"""

from __future__ import annotations

from src.context_builder.builder import ContextBuilder
from src.llm.client import LLMClient
from src.prompt_builder.builder import PromptBuilder
from src.retrieval.retriever import Retriever
from src.vector_store.chroma_store import VectorStore


def main() -> None:
    """
    Validate the complete RAG workflow.
    """

    query = "Recommend a good men's polo shirt."

    print("=" * 80)
    print("RAG Pipeline Validation")
    print("=" * 80)
    print(f"Query: {query}")
    print()

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    vector_store = VectorStore()

    retriever = Retriever(vector_store)

    chunks = retriever.retrieve(
        query=query,
        top_k=3,
    )

    print(f"✓ Retrieved {len(chunks)} chunks")

    # ------------------------------------------------------------------
    # Context Builder
    # ------------------------------------------------------------------

    context = ContextBuilder().build(chunks)

    print("✓ Context built")

    # ------------------------------------------------------------------
    # Prompt Builder
    # ------------------------------------------------------------------

    prompt = PromptBuilder().build(
        query=query,
        context=context,
    )

    print("✓ Prompt built")

    # ------------------------------------------------------------------
    # LLM
    # ------------------------------------------------------------------

    llm = LLMClient()

    answer = llm.generate(prompt)

    print("✓ LLM response generated")

    print()
    print("=" * 80)
    print("Final Answer")
    print("=" * 80)
    print(answer)


if __name__ == "__main__":
    main()