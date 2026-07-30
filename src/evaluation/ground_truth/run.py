"""
Entry point for the Ground Truth Builder.
"""

from __future__ import annotations

from src.evaluation.ground_truth.builder import GroundTruthBuilder
from src.evaluation.ground_truth.formatter import GroundTruthFormatter
from src.evaluation.ground_truth.queries import GROUND_TRUTH_QUERIES
from src.evaluation.ground_truth.writer import GroundTruthWriter


def main() -> None:
    """Generate candidate reports for all semantic benchmark queries."""

    builder = GroundTruthBuilder()
    formatter = GroundTruthFormatter()
    writer = GroundTruthWriter()

    total = len(GROUND_TRUTH_QUERIES)

    print("\nGenerating ground truth reports...\n")

    for index, example in enumerate(
        GROUND_TRUTH_QUERIES,
        start=1,
    ):
        print(
            f"[{index}/{total}] {example.id}"
        )

        candidates = builder.build(example)

        report = formatter.format(
            example,
            candidates,
        )

        writer.write_report(
            example.id,
            report,
        )

        print(
            f"✓ Saved {example.id}"
        )

    print(
        "\nGround truth reports generated successfully."
    )


if __name__ == "__main__":
    main()