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
            "Review the candidate products and approve the relevant ASINs."
        )
        lines.append(
            "Copy the approved ASINs into the retrieval benchmark dataset."
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
            f"{index})",
            "",
            f"ASIN      : {product.asin}",
            f"Brand     : {product.brand}",
            f"Price     : {price}",
            f"Rating    : {rating}",
            "Title",
            f"{product.title}",
            "",
            "-" * self.LINE_WIDTH,
            "",
        ]

    def format_benchmark_template(
        self,
        example: GroundTruthExample,
        candidates: list[CandidateProduct],
    ) -> str:
        """
        Generate a copy-paste benchmark template.

        The generated template already contains all candidate ASINs.
        During review, simply remove the false positives before
        adding the example to the benchmark dataset.
        """

        lines: list[str] = []

        lines.append("=" * self.LINE_WIDTH)
        lines.append("Copy-Paste Benchmark Template")
        lines.append("=" * self.LINE_WIDTH)
        lines.append("")

        lines.append("GroundTruthExample(")
        lines.append(f'    id="{example.id}",')
        lines.append(f'    query="{example.query}",')
        lines.append("")

        lines.append("    relevant_asins=[")

        if candidates:
            for candidate in candidates:
                lines.append(f'        "{candidate.asin}",')
        else:
            lines.append("        # No candidates found")

        lines.append("    ],")
        lines.append("")
        lines.append(
            f"    category=QueryCategory.{example.category.name},"
        )
        lines.append(
            f'    description="{example.description}",'
        )
        lines.append(")")
        lines.append("")

        lines.append("# Review Checklist")
        lines.append("# 1. Remove false-positive ASINs.")
        lines.append("# 2. Verify every remaining ASIN satisfies the query intent.")
        lines.append("# 3. Save the approved example into benchmark.py.")

        return "\n".join(lines)