"""
Reporting utilities for retrieval evaluation.

Formats retrieval evaluation results into a
human-readable report.
"""

from __future__ import annotations

from src.evaluation.evaluator.models import (
    EvaluationSummary,
    MetadataEvaluation,
    QueryEvaluation,
    RetrievalMethodSummary,
)


class EvaluationReporter:
    """
    Formats retrieval evaluation results.
    """

    LINE_WIDTH = 100

    def generate(
        self,
        summary: EvaluationSummary,
    ) -> str:
        """
        Generate a complete evaluation report.
        """

        lines: list[str] = []

        lines.append("=" * self.LINE_WIDTH)
        lines.append("Retrieval Evaluation Report")
        lines.append("=" * self.LINE_WIDTH)
        lines.append("")

        for method in summary.retrieval_methods:

            lines.extend(
                self._method_report(
                    method,
                )
            )

            lines.append("")

        lines.extend(
            self._comparison(
                summary,
            )
        )

        lines.append("")

        lines.extend(
            self._selected_retriever(
                summary,
            )
        )

        return "\n".join(lines)

    
    def _method_report(
        self,
        summary: RetrievalMethodSummary,
    ) -> list[str]:
        """
        Format one retrieval method report.
        """

        lines: list[str] = []

        lines.append("=" * self.LINE_WIDTH)
        lines.append(
            f"{summary.retrieval_method} Retrieval"
        )
        lines.append("=" * self.LINE_WIDTH)
        lines.append("")

        lines.extend(
            self._semantic_summary(
                summary,
            )
        )

        lines.append("")
        lines.append("=" * self.LINE_WIDTH)
        lines.append("Semantic Query Results")
        lines.append("=" * self.LINE_WIDTH)
        lines.append("")

        for result in summary.semantic_results:

            lines.extend(
                self._semantic_query(
                    result,
                )
            )

        lines.append("")
        lines.append("=" * self.LINE_WIDTH)
        lines.append("Metadata Evaluation")
        lines.append("=" * self.LINE_WIDTH)
        lines.append("")

        lines.extend(
            self._metadata_summary(
                summary,
            )
        )

        lines.append("")
        lines.append("=" * self.LINE_WIDTH)
        lines.append("Metadata Query Results")
        lines.append("=" * self.LINE_WIDTH)
        lines.append("")

        for result in summary.metadata_results:

            lines.extend(
                self._metadata_query(
                    result,
                )
            )

        return lines


    def _semantic_summary(
        self,
        summary: RetrievalMethodSummary,
    ) -> list[str]:
        """
        Format semantic evaluation summary.
        """

        return [
            "Semantic Evaluation",
            "-" * self.LINE_WIDTH,
            (
                f"Queries                  : "
                f"{summary.total_semantic_queries}"
            ),
            (
                f"Average Precision@K      : "
                f"{summary.average_precision_at_k:.3f}"
            ),
            (
                f"Average Recall@K         : "
                f"{summary.average_recall_at_k:.3f}"
            ),
            (
                f"Average Hit Rate         : "
                f"{summary.hit_rate:.3f}"
            ),
            (
                f"Mean Reciprocal Rank     : "
                f"{summary.mean_reciprocal_rank:.3f}"
            ),
        ]
    

    def _metadata_summary(
        self,
        summary: RetrievalMethodSummary,
    ) -> list[str]:
        """
        Format metadata evaluation summary.
        """

        return [
            "Metadata Evaluation",
            "-" * self.LINE_WIDTH,
            (
                f"Queries                     : "
                f"{summary.total_metadata_queries}"
            ),
            (
                f"Average Constraint Accuracy : "
                f"{summary.average_constraint_accuracy:.3f}"
            ),
            (
                f"Metadata Pass Rate          : "
                f"{summary.metadata_pass_rate:.3f}"
            ),
        ]

    def _semantic_query(
        self,
        evaluation: QueryEvaluation,
    ) -> list[str]:
        """
        Format one semantic benchmark result.
        """

        lines: list[str] = []

        lines.append(f"Query ID : {evaluation.query_id}")
        lines.append(f"Category : {evaluation.category.value}")
        lines.append(f"Query    : {evaluation.query}")
        lines.append("")

        lines.append(
            f"Expected Products  : {evaluation.expected_count}"
        )

        lines.append(
            f"Retrieved Products : {evaluation.retrieved_count}"
        )

        lines.append(
            f"Relevant Retrieved : {evaluation.relevant_retrieved}"
        )

        lines.append("")

        lines.append(
            f"Precision@K        : {evaluation.precision_at_k:.3f}"
        )

        lines.append(
            f"Recall@K           : {evaluation.recall_at_k:.3f}"
        )

        lines.append(
            f"Hit Rate           : {evaluation.hit_rate}"
        )

        lines.append(
            f"Reciprocal Rank    : {evaluation.reciprocal_rank:.3f}"
        )

        lines.append("")
        lines.append("Retrieved Products")

        if not evaluation.retrieved_products:

            lines.append("  None")

        else:

            for product in evaluation.retrieved_products:

                lines.append(
                    f"  Rank {product.rank:<2}"
                    f" ASIN={product.asin}"
                    f" Distance={product.distance:.4f}"
                )

        lines.append("")
        lines.append("-" * self.LINE_WIDTH)
        lines.append("")

        return lines

    def _metadata_query(
        self,
        evaluation: MetadataEvaluation,
    ) -> list[str]:
        """
        Format one metadata benchmark result.
        """

        lines: list[str] = []

        lines.append(f"Query ID : {evaluation.query_id}")
        lines.append(f"Category : {evaluation.category.value}")
        lines.append(f"Query    : {evaluation.query}")
        lines.append("")

        lines.append(
            f"Checked Products    : {evaluation.checked_products}"
        )

        lines.append(
            f"Matching Products   : {evaluation.matching_products}"
        )

        lines.append(
            f"Violations          : {evaluation.violations}"
        )

        lines.append("")

        lines.append(
            f"Constraint Accuracy : "
            f"{evaluation.constraint_accuracy:.3f}"
        )

        lines.append(
            f"Passed              : {evaluation.passed}"
        )

        lines.append("")

        lines.append("Retrieved Products")

        if not evaluation.retrieved_products:

            lines.append("  None")

        else:

            for product in evaluation.retrieved_products:

                lines.append(
                    f"  Rank {product.rank:<2}"
                    f" ASIN={product.asin}"
                    f" Price={product.price}"
                    f" Rating={product.rating}"
                )

        lines.append("")
        lines.append("-" * self.LINE_WIDTH)
        lines.append("")

        return lines


    def _comparison(
        self,
        summary: EvaluationSummary,
    ) -> list[str]:
        """
        Format retrieval method comparison.
        """

        lines: list[str] = []

        lines.append("=" * self.LINE_WIDTH)
        lines.append("Retriever Comparison")
        lines.append("=" * self.LINE_WIDTH)
        lines.append("")

        lines.append(
            f"{'Method':<12}"
            f"{'Precision':>12}"
            f"{'Recall':>10}"
            f"{'Hit Rate':>12}"
            f"{'MRR':>10}"
            f"{'Metadata':>14}"
        )

        lines.append("-" * self.LINE_WIDTH)

        for method in summary.retrieval_methods:

            lines.append(
                f"{method.retrieval_method:<12}"
                f"{method.average_precision_at_k:>12.3f}"
                f"{method.average_recall_at_k:>10.3f}"
                f"{method.hit_rate:>12.3f}"
                f"{method.mean_reciprocal_rank:>10.3f}"
                f"{method.average_constraint_accuracy:>14.3f}"
            )

        return lines

    def _selected_retriever(
        self,
        summary: EvaluationSummary,
    ) -> list[str]:
        """
        Format selected retriever section.
        """

        return [
            "=" * self.LINE_WIDTH,
            "Selected Retriever",
            "=" * self.LINE_WIDTH,
            "",
            summary.selected_retriever,
            "",
            "Reason:",
            summary.selection_reason,
        ]