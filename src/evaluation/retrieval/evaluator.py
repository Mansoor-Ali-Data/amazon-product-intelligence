"""
Retrieval evaluator.

Coordinates retrieval evaluation by executing the benchmark dataset,
computing retrieval metrics, and aggregating the results.

This module contains orchestration logic only.
"""

from __future__ import annotations

from statistics import mean

from src.evaluation.retrieval.dataset import (
    EvaluationExample,
)
from src.evaluation.retrieval.metrics import (
    hit_rate,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)
from src.evaluation.retrieval.models import (
    EvaluationResult,
    EvaluationSummary,
)
from src.retrieval.retriever import Retriever


class RetrievalEvaluator:
    """
    Evaluate retrieval quality using a benchmark dataset.
    """

    def __init__(
        self,
        retriever: Retriever,
    ) -> None:
        """
        Initialize the evaluator.

        Args:
            retriever:
                Retriever used during evaluation.
        """

        self._retriever = retriever

    def evaluate(
        self,
        dataset: list[EvaluationExample],
        top_k: int = 3,
    ) -> EvaluationSummary:
        """
        Evaluate retrieval performance.

        Args:
            dataset:
                Benchmark evaluation dataset.

            top_k:
                Number of documents to retrieve.

        Returns:
            Evaluation summary.
        """

        results: list[EvaluationResult] = []

        for example in dataset:

            chunks = self._retriever.retrieve(
                query=example.query,
                top_k=top_k,
            )

            retrieved_asins = self._extract_unique_asins(
                chunks,
            )

            result = EvaluationResult(
                query=example.query,
                category=example.category,
                expected_asins=example.expected_asins,
                retrieved_asins=retrieved_asins,
                hit_rate=hit_rate(
                    example.expected_asins,
                    retrieved_asins,
                ),
                precision_at_k=precision_at_k(
                    example.expected_asins,
                    retrieved_asins,
                ),
                recall_at_k=recall_at_k(
                    example.expected_asins,
                    retrieved_asins,
                ),
                reciprocal_rank=reciprocal_rank(
                    example.expected_asins,
                    retrieved_asins,
                ),
            )

            results.append(result)

        return EvaluationSummary(
            average_hit_rate=mean(
                result.hit_rate
                for result in results
            ),
            average_precision_at_k=mean(
                result.precision_at_k
                for result in results
            ),
            average_recall_at_k=mean(
                result.recall_at_k
                for result in results
            ),
            mean_reciprocal_rank=mean(
                result.reciprocal_rank
                for result in results
            ),
            results=results,
        )

    @staticmethod
    def _extract_unique_asins(
        chunks,
    ) -> list[str]:
        """
        Extract unique ASINs from retrieved chunks while preserving
        retrieval order.

        Args:
            chunks:
                Retrieved chunks.

        Returns:
            Ordered list of unique retrieved ASINs.
        """

        seen: set[str] = set()
        unique_asins: list[str] = []

        for chunk in chunks:

            asin = chunk.metadata["asin"]

            if asin not in seen:
                seen.add(asin)
                unique_asins.append(asin)

        return unique_asins