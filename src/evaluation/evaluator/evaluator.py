"""
Retrieval evaluator.

Evaluates the retriever against the benchmark dataset using
product-level metrics.
"""

from __future__ import annotations

from src.evaluation.benchmark import BENCHMARKS
from src.evaluation.benchmark_models import BenchmarkQuery
from src.evaluation.evaluator.metrics import (
    calculate_hit_rate,
    calculate_precision,
    calculate_recall,
    calculate_reciprocal_rank,
)
from src.evaluation.evaluator.models import (
    EvaluationSummary,
    QueryEvaluation,
)
from src.retrieval.models import (
    RetrievedChunk,
    RetrievedProduct,
)
from src.retrieval.retriever import Retriever


class RetrievalEvaluator:
    """
    Evaluates retrieval performance on the benchmark dataset.
    """

    def __init__(
        self,
        retriever: Retriever,
    ) -> None:
        self._retriever = retriever

    def evaluate(
        self,
        benchmark: BenchmarkQuery,
        top_k: int = 5,
    ) -> QueryEvaluation:
        """
        Evaluate a single benchmark query.
        """

        retrieved_products = self._retrieve_products(
            query=benchmark.query,
            top_k=top_k,
        )

        retrieved_asins = [
            product.asin
            for product in retrieved_products
        ]

        expected_asins = set(
            benchmark.relevant_asins or []
        )

        expected_count = len(
            expected_asins
        )

        retrieved_count = len(
            retrieved_asins
        )

        relevant_retrieved = len(
            expected_asins.intersection(
                retrieved_asins,
            )
        )

        precision = calculate_precision(
            expected_asins=expected_asins,
            retrieved_asins=retrieved_asins,
        )

        recall = calculate_recall(
            expected_asins=expected_asins,
            retrieved_asins=retrieved_asins,
        )

        hit_rate = calculate_hit_rate(
            expected_asins=expected_asins,
            retrieved_asins=retrieved_asins,
        )

        reciprocal_rank = calculate_reciprocal_rank(
            expected_asins=expected_asins,
            retrieved_asins=retrieved_asins,
        )

        return QueryEvaluation(
            query_id=benchmark.query_id,
            query=benchmark.query,
            category=benchmark.category,

            retrieved_products=retrieved_products,

            expected_count=expected_count,
            retrieved_count=retrieved_count,
            relevant_retrieved=relevant_retrieved,

            recall_at_k=recall,
            precision_at_k=precision,
            hit_rate=hit_rate,
            reciprocal_rank=reciprocal_rank,
        )

    def evaluate_all(
        self,
        top_k: int = 5,
    ) -> EvaluationSummary:
        """
        Evaluate the entire benchmark dataset.
        """

        semantic_benchmarks = self._semantic_benchmarks()

        metadata_benchmarks = self._metadata_benchmarks()


        query_results = [
            self.evaluate(
                benchmark=benchmark,
                top_k=top_k,
            )
            for benchmark in semantic_benchmarks
        ]
        
        total_queries = len(
            query_results
        )

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

    def _retrieve_products(
        self,
        query: str,
        top_k: int,
    ) -> list[RetrievedProduct]:
        """
        Retrieve unique products for a query.
        """

        chunks = self._retriever.retrieve(
            query=query,
            top_k=top_k,
        )

        return self._deduplicate_products(
            chunks,
        )

    @staticmethod
    def _deduplicate_products(
        chunks: list[RetrievedChunk],
    ) -> list[RetrievedProduct]:
        """
        Convert retrieved chunks into unique products.

        Only the highest-ranked chunk for each ASIN is kept.
        Product ranks are reassigned after deduplication.
        """

        unique_chunks: list[RetrievedChunk] = []
        seen_asins: set[str] = set()

        # Keep only the first (highest-ranked) chunk for each product
        for chunk in chunks:

            if chunk.asin in seen_asins:
                continue

            seen_asins.add(chunk.asin)
            unique_chunks.append(chunk)

        # Reassign contiguous product ranks
        products: list[RetrievedProduct] = []

        for rank, chunk in enumerate(
            unique_chunks,
            start=1,
        ):

            products.append(
                RetrievedProduct(
                    asin=chunk.asin,
                    rank=rank,
                    distance=chunk.distance,
                    metadata=chunk.metadata,
                )
            )

        return products


    def _semantic_benchmarks(
        self,
    ) -> list[BenchmarkQuery]:
        """
        Return benchmarks evaluated using semantic retrieval.

        Semantic benchmarks define relevant ASINs.
        """

        return [
            benchmark
            for benchmark in BENCHMARKS
            if benchmark.relevant_asins
        ]


    def _metadata_benchmarks(
        self,
    ) -> list[BenchmarkQuery]:
        """
        Return benchmarks evaluated using metadata filters.

        Metadata benchmarks define expected filters.
        """

        return [
            benchmark
            for benchmark in BENCHMARKS
            if benchmark.expected_filter is not None
        ]