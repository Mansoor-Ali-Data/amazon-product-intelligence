"""
Run the retrieval evaluation benchmark.
"""

from __future__ import annotations

from src.evaluation.retrieval.dataset import (
    get_semantic_benchmark,
)
from src.evaluation.retrieval.evaluator import (
    RetrievalEvaluator,
)
from src.evaluation.retrieval.formatter import (
    EvaluationFormatter,
)
from src.retrieval.retriever import Retriever
from src.vector_store.chroma_store import VectorStore

TOP_K = 3


def main() -> None:
    """
    Execute the semantic retrieval benchmark.
    """

    vector_store = VectorStore()

    retriever = Retriever(
        vector_store,
    )

    evaluator = RetrievalEvaluator(
        retriever=retriever,
    )

    summary = evaluator.evaluate(
        dataset=get_semantic_benchmark(),
        top_k=TOP_K,
    )

    formatter = EvaluationFormatter()

    formatter.format(
        summary,
    )


if __name__ == "__main__":
    main()