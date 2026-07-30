"""
Formatter for the ground truth builder.

Responsible for formatting candidate products into a
human-readable report.

This module performs no searching or evaluation.
"""

from __future__ import annotations

from src.evaluation.ground_truth.models import (
    CandidateProduct,
    GroundTruthExample,
)


class GroundTruthFormatter:
    """
    Formats ground truth builder results.
    """

    LINE_WIDTH = 80

    def format(
        self,
        example: GroundTruthExample,
        candidates: list[CandidateProduct],
    ) -> str:
        """
        Format candidate products for a benchmark query.

        Parameters
        ----------
        example:
            Benchmark query.

        candidates:
            Candidate products.

        Returns
        -------
        str
            Formatted report.
        """

        lines: list[str] = []

        lines.append("=" * self.LINE_WIDTH)
        lines.append("Ground Truth Builder")
        lines.append("=" * self.LINE_WIDTH)
        lines.append("")

        lines.append(f"Query ID    : {example.id}")
        lines.append(f"Category    : {example.category.value}")
        lines.append(f"Query       : {example.query}")
        lines.append(f"Description : {example.description}")
        lines.append("")

        lines.append("-" * self.LINE_WIDTH)
        lines.append("Candidate Products")
        lines.append("-" * self.LINE_WIDTH)
        lines.append("")

        lines.append(
            f"Found {len(candidates)} candidate product(s)."
        )
        lines.append("")

        if not candidates:
            lines.append("No candidate products found.")
            lines.append("")
            lines.append("-" * self.LINE_WIDTH)
            lines.append("Summary")
            lines.append("-" * self.LINE_WIDTH)
            lines.append("")
            lines.append("Candidates Found : 0")
            lines.append("")
            lines.append(
                "Next Step: Review the query or improve the candidate generator."
            )
            return "\n".join(lines)

        for index, product in enumerate(candidates, start=1):

            lines.extend(
                self._format_candidate(
                    index=index,
                    product=product,
                )
            )

        lines.append("Summary")
        lines.append("-" * self.LINE_WIDTH)
        lines.append("")
        lines.append(
            f"Candidates Found : {len(candidates)}"
        )
        lines.append("")
        lines.append(
            "Next Step:"
        )
        lines.append(
            "Review the candidate products and manually approve the relevant ASINs."
        )

        return "\n".join(lines)

    def _format_candidate(
        self,
        index: int,
        product: CandidateProduct,
    ) -> list[str]:
        """
        Format a single candidate product.
        """

        price = (
            f"${product.price:.2f}"
            if product.price is not None
            else "N/A"
        )

        rating = (
            f"{product.rating:.1f}"
            if product.rating is not None
            else "N/A"
        )

        return [
        f"[{index}]",
        "",
        f"ASIN   : {product.asin}",
        f"Brand  : {product.brand}",
        f"Price  : {price}",
        f"Rating : {rating}",
        "Title",
        product.title,
        "",
        "-" * self.LINE_WIDTH,
        "",
    ]