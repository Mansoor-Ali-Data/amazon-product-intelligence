"""
Run the end-to-end RAG pipeline.

This executable serves as the primary entry point for interacting
with the Retrieval-Augmented Generation system from the command line.
"""

from __future__ import annotations

from src.pipeline.rag_pipeline import RAGPipeline


def main() -> None:
    """
    Run the RAG pipeline for a sample query.
    """

    query = "Recommend a good men's polo shirt."

    pipeline = RAGPipeline()

    response = pipeline.ask(query)

    print("=" * 80)
    print("Amazon Product Intelligence Assistant")
    print("=" * 80)
    print()
    print(f"Question:\n{query}")
    print()
    print("-" * 80)
    print("Answer")
    print("-" * 80)
    print(response.answer)
    print()


if __name__ == "__main__":
    main()