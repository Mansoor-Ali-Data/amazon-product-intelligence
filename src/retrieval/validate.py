"""
Validate retrieval implementations.

Runs smoke tests for all retrieval strategies.
"""

from __future__ import annotations

import logging
import re

from src.bm25_store.store import BM25Store
from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.models import RetrievedChunk
from src.retrieval.retriever import Retriever
from src.vector_store.chroma_store import VectorStore

logger = logging.getLogger(__name__)

QUERY = "men polo shirt"
LINE_WIDTH = 100


def main() -> None:
    """
    Run retrieval validation.
    """

    print()
    print("=" * LINE_WIDTH)
    print("Retrieval Validation")
    print("=" * LINE_WIDTH)

    _validate_dense_retriever()

    print()

    _validate_bm25_retriever()

    print()

    print("=" * LINE_WIDTH)
    print("Validation Passed")
    print("=" * LINE_WIDTH)


def _validate_dense_retriever() -> None:
    """
    Validate dense semantic retrieval.
    """

    vector_store = VectorStore()

    retriever = Retriever(
        vector_store=vector_store,
    )

    results = retriever.retrieve(
        query=QUERY,
        top_k=5,
    )

    _print_results(
        title="Dense Retrieval",
        query=QUERY,
        metric_name="Distance",
        results=results,
    )


def _validate_bm25_retriever() -> None:
    """
    Validate BM25 lexical retrieval.
    """

    retriever = BM25Retriever(
        store=BM25Store(),
    )

    results = retriever.retrieve(
        query=QUERY,
        top_k=5,
    )

    _print_results(
        title="BM25 Retrieval",
        query=QUERY,
        metric_name="Score",
        results=results,
    )


def _print_results(
    title: str,
    query: str,
    metric_name: str,
    results: list[RetrievedChunk],
) -> None:
    """
    Print retrieval results.
    """

    print("=" * LINE_WIDTH)
    print(title)
    print("=" * LINE_WIDTH)

    print(f"Query            : {query}")
    print(f"Retrieved Chunks : {len(results)}")

    print("-" * LINE_WIDTH)

    for chunk in results:

        print(f"Rank             : {chunk.rank}")
        value = (
            -chunk.distance
            if metric_name == "Score"
            else chunk.distance
        )

        print(
            f"{metric_name:<17}: {value:.4f}"
        )
        print(f"ASIN             : {chunk.asin}")
        print(
            f"Brand            : "
            f"{chunk.metadata.get('brand_name', 'N/A')}"
        )

        print()
        print("Preview:")
        print(_preview(chunk.text))
        print("-" * LINE_WIDTH)

    logger.info("%s results", title)

    for chunk in results:
        logger.info(
            "[Rank %d | %s %.4f] %s",
            chunk.rank,
            metric_name,
            value,
            chunk.asin,
        )


def _preview(
    text: str,
) -> str:
    """
    Create a short preview of a retrieved chunk.
    """

    preview = re.sub(
        r"\s+",
        " ",
        text,
    )

    preview = re.sub(
        r"[=]{2,}",
        "",
        preview,
    )

    about_index = preview.find(
        "ABOUT THIS ITEM",
    )

    if about_index != -1:
        preview = preview[about_index:]

    return preview[:200] + "..."


if __name__ == "__main__":
    main()