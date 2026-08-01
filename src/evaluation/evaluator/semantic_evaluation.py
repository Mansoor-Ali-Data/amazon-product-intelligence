"""
Semantic retrieval evaluator.

Evaluates retrieval quality for any retrieval implementation.
"""

from __future__ import annotations

from src.evaluation.benchmark_models import BenchmarkQuery
from src.evaluation.evaluator.metrics import (
    calculate_hit_rate,
    calculate_precision,
    calculate_recall,
    calculate_reciprocal_rank,
)
from src.evaluation.evaluator.models import (
    QueryEvaluation,
    RetrievedProduct,
)
from src.retrieval.models import (
    RetrievedChunk,
)
from src.retrieval.retriever import Retriever


class SemanticEvaluator:
    """
    Evaluates semantic retrieval quality for a retrieval method.
    """

    def __init__(
        self,
        retriever,
        retrieval_method: str,
    ) -> None:
        """
        Initialize the evaluator.

        Args:
            retriever:
                Any retriever implementing retrieve().

            retrieval_method:
                Display name used in reports.
        """

        self._retriever = retriever
        self._retrieval_method = retrieval_method

    def evaluate(
        self,
        benchmark: BenchmarkQuery,
        top_k: int = 5,
    ) -> QueryEvaluation:
        """
        Evaluate a semantic benchmark query.
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

    def _retrieve_products(
        self,
        query: str,
        top_k: int,
    ) -> list[RetrievedProduct]:
        """
        Retrieve unique products.
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
        Convert retrieved chunks into unique retrieved products.
        """

        unique_chunks: list[RetrievedChunk] = []

        seen_asins: set[str] = set()

        for chunk in chunks:

            if chunk.asin in seen_asins:
                continue

            seen_asins.add(
                chunk.asin,
            )

            unique_chunks.append(
                chunk,
            )

        products: list[RetrievedProduct] = []

        for rank, chunk in enumerate(
            unique_chunks,
            start=1,
        ):

            metadata = chunk.metadata

            products.append(
                RetrievedProduct(
                    asin=chunk.asin,
                    rank=rank,
                    distance=chunk.distance,
                    price=metadata.get(
                        "price_value",
                    ),
                    rating=metadata.get(
                        "rating_stars",
                    ),
                )
            )

        return products