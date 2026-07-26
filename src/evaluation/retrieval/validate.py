"""
Validate the retrieval evaluation pipeline.
"""

from __future__ import annotations

from src.evaluation.retrieval.dataset import (
    EVALUATION_DATASET,
)
from src.evaluation.retrieval.evaluator import (
    RetrievalEvaluator,
)
from src.retrieval.retriever import Retriever
from src.vector_store.chroma_store import VectorStore


def main() -> None:
    """
    Validate the retrieval evaluator.
    """

    vector_store = VectorStore()

    retriever = Retriever(
        vector_store,
    )

    evaluator = RetrievalEvaluator(
        retriever=retriever,
    )

    summary = evaluator.evaluate(
        dataset=EVALUATION_DATASET[:1],
        top_k=3,
    )

    assert len(summary.results) == 1

    print("✅ Retrieval evaluation validation passed.")


if __name__ == "__main__":
    main()