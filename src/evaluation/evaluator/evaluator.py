"""
Retrieval evaluator.

Coordinates semantic and metadata evaluation across the benchmark
dataset.
"""

from __future__ import annotations

from src.evaluation.benchmark import BENCHMARKS
from src.evaluation.benchmark_models import BenchmarkQuery
from src.evaluation.evaluator.models import EvaluationSummary
from src.evaluation.evaluator.semantic import SemanticEvaluator
from src.retrieval.retriever import Retriever


class RetrievalEvaluator:
    """
    Coordinates retrieval evaluation.
    """

    def __init__(
        self,
        retriever: Retriever,
    ) -> None:

        self._semantic = SemanticEvaluator(
            retriever=retriever,
        )

    def evaluate_all(
        self,
        top_k: int = 5,
    ) -> EvaluationSummary:
        """
        Evaluate all semantic benchmarks.

        Metadata benchmarks will be evaluated by a dedicated
        MetadataEvaluator in a later step.
        """

        semantic_benchmarks = self._semantic_benchmarks()

        metadata_benchmarks = self._metadata_benchmarks()

        # Placeholder until MetadataEvaluator exists.
        _ = metadata_benchmarks

        query_results = [
            self._semantic.evaluate(
                benchmark=benchmark,
                top_k=top_k,
            )
            for benchmark in semantic_benchmarks
        ]

        total_queries = len(query_results)

        average_recall = (
            sum(
                result.recall_at_k
                for result in query_results
            )
            / total_queries
            if total_queries
            else 0.0
        )

        average_precision = (
            sum(
                result.precision_at_k
                for result in query_results
            )
            / total_queries
            if total_queries
            else 0.0
        )

        hit_rate = (
            sum(
                result.hit_rate
                for result in query_results
            )
            / total_queries
            if total_queries
            else 0.0
        )

        mean_reciprocal_rank = (
            sum(
                result.reciprocal_rank
                for result in query_results
            )
            / total_queries
            if total_queries
            else 0.0
        )

        return EvaluationSummary(
            query_results=query_results,
            total_queries=total_queries,
            average_recall_at_k=average_recall,
            average_precision_at_k=average_precision,
            hit_rate=hit_rate,
            mean_reciprocal_rank=mean_reciprocal_rank,
        )

    @staticmethod
    def _semantic_benchmarks() -> list[BenchmarkQuery]:
        """
        Return semantic retrieval benchmarks.
        """

        return [
            benchmark
            for benchmark in BENCHMARKS
            if benchmark.relevant_asins
        ]

    @staticmethod
    def _metadata_benchmarks() -> list[BenchmarkQuery]:
        """
        Return metadata filter benchmarks.
        """

        return [
            benchmark
            for benchmark in BENCHMARKS
            if benchmark.expected_filter is not None
        ]