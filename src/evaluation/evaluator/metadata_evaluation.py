"""
Metadata retrieval evaluator.

Evaluates metadata retrieval benchmarks using structured filters
rather than semantic relevance.
"""

from __future__ import annotations

from src.evaluation.benchmark_models import (
    BenchmarkQuery,
    ExpectedFilter,
)
from src.evaluation.evaluator.models import (
    MetadataEvaluation,
    RetrievedProduct,
)
from src.retrieval.models import RetrievedChunk
from src.retrieval.retriever import Retriever


class MetadataEvaluator:
    """
    Evaluates metadata retrieval benchmarks.
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
    ) -> MetadataEvaluation:
        """
        Evaluate a metadata benchmark.
        """

        if benchmark.expected_filter is None:
            raise ValueError(
                f"Benchmark '{benchmark.query_id}' has no expected filter."
            )

        retrieved_products = self._retrieve_products(
            query=benchmark.query,
            top_k=top_k,
        )

        matching_products = sum(
            self._matches_filter(
                product=product,
                expected_filter=benchmark.expected_filter,
            )
            for product in retrieved_products
        )

        checked_products = len(
            retrieved_products
        )

        violations = (
            checked_products
            - matching_products
        )

        constraint_accuracy = (
            matching_products / checked_products
            if checked_products
            else 0.0
        )

        passed = matching_products > 0

        return MetadataEvaluation(
            query_id=benchmark.query_id,
            query=benchmark.query,
            category=benchmark.category,
            retrieved_products=retrieved_products,
            checked_products=checked_products,
            matching_products=matching_products,
            violations=violations,
            constraint_accuracy=constraint_accuracy,
            passed=passed,
        )

    def _matches_filter(
        self,
        product: RetrievedProduct,
        expected_filter: ExpectedFilter,
    ) -> bool:
        """
        Check whether a retrieved product satisfies the expected filter.
        """

        if (
            expected_filter.min_price is not None
            and (
                product.price is None
                or product.price < expected_filter.min_price
            )
        ):
            return False

        if (
            expected_filter.max_price is not None
            and (
                product.price is None
                or product.price > expected_filter.max_price
            )
        ):
            return False

        if (
            expected_filter.min_rating is not None
            and (
                product.rating is None
                or product.rating < expected_filter.min_rating
            )
        ):
            return False

        if (
            expected_filter.max_rating is not None
            and (
                product.rating is None
                or product.rating > expected_filter.max_rating
            )
        ):
            return False

        return True

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

        for chunk in chunks:

            if chunk.asin in seen_asins:
                continue

            seen_asins.add(chunk.asin)
            unique_chunks.append(chunk)

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
                    price=chunk.metadata.get(
                        "price_value",
                    ),
                    rating=chunk.metadata.get(
                        "rating_stars",
                    ),
                )
            )

        return products