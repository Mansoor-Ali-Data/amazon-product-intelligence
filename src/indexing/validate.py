"""
Validation script for the offline indexing pipeline.
"""

from src.indexing.pipeline import run_indexing_pipeline


def main() -> None:
    run_indexing_pipeline()

    print("✅ Offline indexing pipeline validation completed.")


if __name__ == "__main__":
    main()