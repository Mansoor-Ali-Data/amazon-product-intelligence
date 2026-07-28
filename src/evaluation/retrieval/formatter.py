"""
Formatter for retrieval evaluation results.

Responsible for rendering retrieval evaluation results in a readable
console format.

This module contains presentation logic only.
"""

from __future__ import annotations

from src.evaluation.retrieval.models import (
    EvaluationProduct,
    EvaluationResult,
    EvaluationSummary,
)


class EvaluationFormatter:
    """
    Pretty-print retrieval evaluation results.
    """

    def format(
        self,
        summary: EvaluationSummary,
    ) -> None:
        """
        Render the retrieval evaluation report.
        """

        self._print_summary(summary)

        for result in summary.results:

            self._print_query_result(result)

    def _print_summary(
        self,
        summary: EvaluationSummary,
    ) -> None:
        """
        Print overall evaluation metrics.
        """

        print("=" * 80)
        print("Retrieval Evaluation")
        print("=" * 80)
        print()

        print("Overall Metrics")
        print("-" * 80)

        print(
            f"Hit Rate             : {summary.average_hit_rate:.3f}"
        )

        print(
            f"Precision@3          : {summary.average_precision_at_k:.3f}"
        )

        print(
            f"Recall@3             : {summary.average_recall_at_k:.3f}"
        )

        print(
            f"Mean Reciprocal Rank : {summary.mean_reciprocal_rank:.3f}"
        )

        print()

    def _print_query_result(
        self,
        result: EvaluationResult,
    ) -> None:
        """
        Print a single benchmark query.
        """

        print("=" * 80)
        print("Benchmark Query")
        print("=" * 80)
        print()

        print(
            f"Benchmark : {result.benchmark.value}"
        )

        print(
            f"Category  : {result.category.value}"
        )

        print(
            f"Query     : {result.query}"
        )

        print()

        self._print_expected_products(
            result.expected_products,
        )

        self._print_retrieved_products(
            result.retrieved_products,
        )

        self._print_metrics(result)

    def _print_expected_products(
        self,
        products: list[EvaluationProduct],
    ) -> None:
        """
        Print expected products.
        """

        print("-" * 80)
        print("Expected Products")
        print("-" * 80)
        print()

        for index, product in enumerate(
            products,
            start=1,
        ):

            print(f"{index})")

            print(
                f"ASIN      : {product.asin}"
            )

            print(
                f"Brand     : {product.brand}"
            )

            print(
                f"Title     : {product.title}"
            )

            if product.price is not None:

                print(
                    f"Price     : ${product.price:.2f}"
                )

            else:

                print("Price     : N/A")

            if product.rating is not None:

                print(
                    f"Rating    : {product.rating:.1f}"
                )

            else:

                print("Rating    : N/A")

            print()

    def _print_retrieved_products(
        self,
        products: list[EvaluationProduct],
    ) -> None:
        """
        Print retrieved products.
        """

        print("-" * 80)
        print("Retrieved Products")
        print("-" * 80)
        print()

        for index, product in enumerate(
            products,
            start=1,
        ):

            print(f"{index})")

            print(
                f"ASIN      : {product.asin}"
            )

            print(
                f"Brand     : {product.brand}"
            )

            print(
                f"Title     : {product.title}"
            )

            if product.price is not None:

                print(
                    f"Price     : ${product.price:.2f}"
                )

            else:

                print("Price     : N/A")

            if product.rating is not None:

                print(
                    f"Rating    : {product.rating:.1f}"
                )

            else:

                print("Rating    : N/A")

            if product.distance is not None:

                print(
                    f"Distance  : {product.distance:.3f}"
                )

            print()

            if product.rule_match is not None:

                status = "✓ YES" if product.rule_match else "✗ NO"

                print(
                    f"Intent Match: {status}"
                )

    def _print_metrics(
        self,
        result: EvaluationResult,
    ) -> None:
        """
        Print retrieval metrics for a benchmark query.
        """

        print("-" * 80)
        print("Metrics")
        print("-" * 80)

        print(
            f"Hit Rate   : {result.hit_rate:.3f}"
        )

        print(
            f"Precision  : {result.precision_at_k:.3f}"
        )

        print(
            f"Recall     : {result.recall_at_k:.3f}"
        )

        print(
            f"RR         : {result.reciprocal_rank:.3f}"
        )

        print()