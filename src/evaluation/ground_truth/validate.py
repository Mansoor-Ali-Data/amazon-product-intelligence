"""
Validate the Ground Truth Builder.

This script verifies that all required components are correctly
configured before generating the benchmark dataset.
"""

from __future__ import annotations

from src.evaluation.enums import QueryCategory
from src.evaluation.ground_truth.builder import GroundTruthBuilder
from src.evaluation.ground_truth.queries import GROUND_TRUTH_QUERIES


def _check(
    condition: bool,
    success: str,
    failure: str,
) -> None:
    """
    Print validation result.
    """

    if condition:
        print(f"✓ {success}")
    else:
        raise RuntimeError(failure)


def main() -> None:
    """
    Run validation checks.
    """

    print()
    print("=" * 80)
    print("Ground Truth Builder Validation")
    print("=" * 80)
    print()

    builder = GroundTruthBuilder()

    # ------------------------------------------------------------------
    # Dataset
    # ------------------------------------------------------------------

    _check(
        len(builder._products_df) > 0,
        f"Loaded {len(builder._products_df)} products.",
        "Products dataset is empty.",
    )

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    _check(
        len(GROUND_TRUTH_QUERIES) > 0,
        f"Loaded {len(GROUND_TRUTH_QUERIES)} benchmark queries.",
        "No benchmark queries found.",
    )

    # ------------------------------------------------------------------
    # Generator Registry
    # ------------------------------------------------------------------

    expected_categories = {
        QueryCategory.BRAND,
        QueryCategory.RECOMMENDATION,
    }

    registered_categories = set(
        builder._generators.keys()
    )

    _check(
        expected_categories == registered_categories,
        "All query categories have registered generators.",
        "Generator registry is incomplete.",
    )

    # ------------------------------------------------------------------
    # Generator Smoke Test
    # ------------------------------------------------------------------

    print()

    print("Running semantic query validation...")

    print()

    for example in GROUND_TRUTH_QUERIES:

        candidates = builder.build(example)

        _check(
            isinstance(candidates, list),
            f"{example.id:<30} ({len(candidates)} candidates)",
            f"Generator failed for '{example.id}'.",
        )

    print()
    print("=" * 80)
    print("Validation Passed")
    print("=" * 80)


if __name__ == "__main__":
    main()