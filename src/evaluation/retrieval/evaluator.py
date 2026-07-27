"""
Retrieval evaluator.

Coordinates retrieval evaluation by executing the benchmark dataset,
computing retrieval metrics, and aggregating the results.

This module contains orchestration logic only.
"""

from __future__ import annotations

from statistics import mean

from src.data.data_loader import load_processed_data

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
    EvaluationProduct,
    EvaluationResult,
    EvaluationSummary,
)

from src.retrieval.models import RetrievedChunk
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

        products_df, _ = load_processed_data()

        self._products = (
            products_df
            .set_index("asin")
            .to_dict("index")
        )

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
                Number of retrieved chunks.

        Returns:
            Retrieval evaluation summary.
        """

        results: list[EvaluationResult] = []

        for example in dataset:

            chunks = self._retriever.retrieve(
                query=example.query,
                top_k=top_k,
            )

            expected_products = (
                self._build_expected_products(
                    example.expected_asins,
                )
            )

            retrieved_products = (
                self._build_retrieved_products(
                    chunks,
                )
            )

            expected_asins = self._extract_asins(
                expected_products,
            )

            retrieved_asins = self._extract_asins(
                retrieved_products,
            )

            results.append(
                EvaluationResult(
                    query=example.query,
                    benchmark=example.benchmark,
                    category=example.category,
                    expected_products=expected_products,
                    retrieved_products=retrieved_products,
                    hit_rate=hit_rate(
                        expected_asins,
                        retrieved_asins,
                    ),
                    precision_at_k=precision_at_k(
                        expected_asins,
                        retrieved_asins,
                    ),
                    recall_at_k=recall_at_k(
                        expected_asins,
                        retrieved_asins,
                    ),
                    reciprocal_rank=reciprocal_rank(
                        expected_asins,
                        retrieved_asins,
                    ),
                )
            )

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

    def _build_expected_products(
        self,
        expected_asins: list[str],
    ) -> list[EvaluationProduct]:
        """
        Build evaluation products from expected ASINs.
        """

        products: list[EvaluationProduct] = []

        for asin in expected_asins:

            product = self._products[asin]

            products.append(
                EvaluationProduct(
                    asin=asin,
                    brand=product["brand_name"],
                    title=product["title"],
                    price=product["price_value"],
                    rating=product["rating_stars"],
                )
            )

        return products

    def _build_retrieved_products(
        self,
        chunks: list[RetrievedChunk],
    ) -> list[EvaluationProduct]:
        """
        Build evaluation products from retrieved chunks.

        Duplicate ASINs are removed while preserving retrieval order.
        """

        seen: set[str] = set()

        products: list[EvaluationProduct] = []

        for chunk in chunks:

            if chunk.asin in seen:
                continue

            seen.add(chunk.asin)

            product = self._products[chunk.asin]

            products.append(
                EvaluationProduct(
                    asin=chunk.asin,
                    brand=product["brand_name"],
                    title=product["title"],
                    price=product["price_value"],
                    rating=product["rating_stars"],
                    distance=chunk.distance,
                )
            )

        return products

    @staticmethod
    def _extract_asins(
        products: list[EvaluationProduct],
    ) -> list[str]:
        """
        Extract ASINs from evaluation products.
        """

        return [
            product.asin
            for product in products
        ]