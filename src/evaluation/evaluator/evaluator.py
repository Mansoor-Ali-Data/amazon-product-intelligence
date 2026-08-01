"""
Retrieval evaluator.

Coordinates evaluation of multiple retrieval methods.
"""

from __future__ import annotations

from src.evaluation.benchmark import BENCHMARKS
from src.evaluation.benchmark_models import BenchmarkQuery
from src.evaluation.evaluator.metadata_evaluation import MetadataEvaluator
from src.evaluation.evaluator.models import (
    EvaluationSummary,
    RetrievalMethodSummary,
)
from src.evaluation.evaluator.semantic_evaluation import SemanticEvaluator


class RetrievalEvaluator:
    """
    Coordinates evaluation across multiple retrieval methods.
    """

    def __init__(
        self,
        semantic_evaluators: list[SemanticEvaluator],
        metadata_evaluators: list[MetadataEvaluator],
    ) -> None:

        if len(semantic_evaluators) != len(metadata_evaluators):
            raise ValueError(
                "Semantic and metadata evaluators must have the same length."
            )

        self._semantic_evaluators = semantic_evaluators
        self._metadata_evaluators = metadata_evaluators

    def evaluate_all(
        self,
        top_k: int = 5,
    ) -> EvaluationSummary:
        """
        Evaluate every retrieval method.
        """

        semantic_benchmarks = self._semantic_benchmarks()
        metadata_benchmarks = self._metadata_benchmarks()

        retrieval_methods: list[
            RetrievalMethodSummary
        ] = []

        for semantic_evaluator, metadata_evaluator in zip(
            self._semantic_evaluators,
            self._metadata_evaluators,
            strict=True,
        ):

            semantic_results = [
                semantic_evaluator.evaluate(
                    benchmark=benchmark,
                    top_k=top_k,
                )
                for benchmark in semantic_benchmarks
            ]

            metadata_results = [
                metadata_evaluator.evaluate(
                    benchmark=benchmark,
                    top_k=top_k,
                )
                for benchmark in metadata_benchmarks
            ]

            retrieval_methods.append(
                self._build_summary(
                    semantic_evaluator=semantic_evaluator,
                    semantic_results=semantic_results,
                    metadata_results=metadata_results,
                )
            )

        return EvaluationSummary(
            retrieval_methods=retrieval_methods,
        )

    @staticmethod
    def _build_summary(
        semantic_evaluator: SemanticEvaluator,
        semantic_results,
        metadata_results,
    ) -> RetrievalMethodSummary:
        """
        Build one retrieval-method summary.
        """

        total_semantic = len(
            semantic_results
        )

        total_metadata = len(
            metadata_results
        )

        return RetrievalMethodSummary(
            retrieval_method=semantic_evaluator.retrieval_method,

            semantic_results=semantic_results,
            metadata_results=metadata_results,

            total_semantic_queries=total_semantic,
            total_metadata_queries=total_metadata,

            average_recall_at_k=(
                sum(
                    r.recall_at_k
                    for r in semantic_results
                )
                / total_semantic
                if total_semantic
                else 0.0
            ),

            average_precision_at_k=(
                sum(
                    r.precision_at_k
                    for r in semantic_results
                )
                / total_semantic
                if total_semantic
                else 0.0
            ),

            hit_rate=(
                sum(
                    r.hit_rate
                    for r in semantic_results
                )
                / total_semantic
                if total_semantic
                else 0.0
            ),

            mean_reciprocal_rank=(
                sum(
                    r.reciprocal_rank
                    for r in semantic_results
                )
                / total_semantic
                if total_semantic
                else 0.0
            ),

            average_constraint_accuracy=(
                sum(
                    r.constraint_accuracy
                    for r in metadata_results
                )
                / total_metadata
                if total_metadata
                else 0.0
            ),

            metadata_pass_rate=(
                sum(
                    r.passed
                    for r in metadata_results
                )
                / total_metadata
                if total_metadata
                else 0.0
            ),
        )

    @staticmethod
    def _semantic_benchmarks(
    ) -> list[BenchmarkQuery]:
        """
        Return semantic retrieval benchmarks.
        """

        return [
            benchmark
            for benchmark in BENCHMARKS
            if benchmark.relevant_asins
        ]

    @staticmethod
    def _metadata_benchmarks(
    ) -> list[BenchmarkQuery]:
        """
        Return metadata retrieval benchmarks.
        """

        return [
            benchmark
            for benchmark in BENCHMARKS
            if benchmark.expected_filter is not None
        ]