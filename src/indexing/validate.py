"""
Validation script for the offline indexing pipeline.
"""

from __future__ import annotations

from src.indexing.pipeline import run_indexing_pipeline


def main() -> None:
    """
    Validate that the offline indexing pipeline executes successfully.
    """

    run_indexing_pipeline()

    print("✅ Offline indexing pipeline validation completed.")


if __name__ == "__main__":
    main()