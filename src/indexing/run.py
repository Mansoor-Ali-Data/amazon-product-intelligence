"""
Run the offline indexing pipeline.

This executable serves as the primary entry point for building
the vector database from the processed product dataset.
"""

from __future__ import annotations

from src.indexing.pipeline import run_indexing_pipeline


def main() -> None:
    """
    Execute the offline indexing pipeline.
    """

    run_indexing_pipeline()

    print("=" * 80)
    print("Offline Indexing Pipeline")
    print("=" * 80)
    print("Knowledge base built successfully.")
    print()


if __name__ == "__main__":
    main()