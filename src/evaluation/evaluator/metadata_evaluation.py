"""
Metadata retrieval evaluator.

Evaluates whether retrieved products satisfy metadata constraints
such as price and rating filters.
"""

from __future__ import annotations

from src.evaluation.benchmark_models import BenchmarkQuery
from src.evaluation.evaluator.models import (
    MetadataEvaluation,
    RetrievedProduct,
)
from src.retrieval.models import RetrievedChunk


class MetadataEvaluator:
    """
    Evaluates metadata constraint satisfaction for a retrieval method.
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

    @property
    def retrieval_method(
        self,
    ) -> str:
        """
        Name of the retrieval method being evaluated.
        """

        return self._retrieval_method

    def evaluate(
        self,
        benchmark: BenchmarkQuery,
        top_k: int = 5,
    ) -> MetadataEvaluation:
        """
        Evaluate one metadata benchmark query.
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
                product,
                benchmark.expected_filter,
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
            matching_products
            / checked_products
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

    @staticmethod
    def _matches_filter(
        product: RetrievedProduct,
        expected_filter,
    ) -> bool:
        """
        Check whether a product satisfies the expected metadata filter.
        """

        if expected_filter.max_price is not None:

            if (
                product.price is None
                or product.price > expected_filter.max_price
            ):
                return False

        if expected_filter.min_price is not None:

            if (
                product.price is None
                or product.price < expected_filter.min_price
            ):
                return False

        if expected_filter.min_rating is not None:

            if (
                product.rating is None
                or product.rating < expected_filter.min_rating
            ):
                return False

        if expected_filter.max_rating is not None:

            if (
                product.rating is None
                or product.rating > expected_filter.max_rating
            ):
                return False

        return True