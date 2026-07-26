"""
Run the retrieval evaluation benchmark.
"""

from __future__ import annotations

from src.evaluation.retrieval.dataset import EVALUATION_DATASET
from src.evaluation.retrieval.evaluator import RetrievalEvaluator
from src.retrieval.retriever import Retriever
from src.vector_store.chroma_store import VectorStore


def main() -> None:
    """
    Execute the retrieval benchmark.
    """

    print("=" * 80)
    print("Retrieval Evaluation")
    print("=" * 80)
    print()

    vector_store = VectorStore()

    retriever = Retriever(
        vector_store,
    )

    evaluator = RetrievalEvaluator(
        retriever=retriever,
    )

    summary = evaluator.evaluate(
        dataset=EVALUATION_DATASET,
        top_k=3,
    )

    # ------------------------------------------------------------------
    # Overall Metrics
    # ------------------------------------------------------------------

    print("Overall Metrics")
    print("-" * 80)

    print(
        f"Hit Rate           : {summary.average_hit_rate:.3f}"
    )

    print(
        f"Precision@3        : {summary.average_precision_at_k:.3f}"
    )

    print(
        f"Recall@3           : {summary.average_recall_at_k:.3f}"
    )

    print(
        f"Mean Reciprocal Rank: {summary.mean_reciprocal_rank:.3f}"
    )

    print()

    # ------------------------------------------------------------------
    # Per Query Results
    # ------------------------------------------------------------------

    print("=" * 80)
    print("Per Query Results")
    print("=" * 80)

    for result in summary.results:

        print()
        print("-" * 80)

        print(f"Category   : {result.category}")
        print(f"Query      : {result.query}")

        print(
            f"Expected   : {', '.join(result.expected_asins)}"
        )

        print(
            f"Retrieved  : {', '.join(result.retrieved_asins)}"
        )

        print(f"Hit Rate   : {result.hit_rate:.3f}")

        print(
            f"Precision  : {result.precision_at_k:.3f}"
        )

        print(
            f"Recall     : {result.recall_at_k:.3f}"
        )

        print(
            f"RR         : {result.reciprocal_rank:.3f}"
        )


if __name__ == "__main__":
    main()