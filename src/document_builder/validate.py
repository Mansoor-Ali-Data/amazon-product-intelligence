"""
Validate the Document Builder by generating sample documents
from the processed datasets.

This script is intended for manual inspection during development.
"""

from pathlib import Path

import pandas as pd

from src.document_builder.builder import build_documents
from config.logging import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

PRODUCTS_PATH = Path("data/processed/products.csv")
REVIEWS_PATH = Path("data/processed/reviews.csv")

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SAMPLE_OUTPUT = OUTPUT_DIR / "sample_document.txt"


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main() -> None:
    """Run Document Builder validation."""

    logger.info("Loading processed datasets...")

    products_df = pd.read_csv(PRODUCTS_PATH)
    reviews_df = pd.read_csv(REVIEWS_PATH)

    logger.info(
        "Loaded %d products and %d reviews.",
        len(products_df),
        len(reviews_df),
    )

    documents = build_documents(products_df, reviews_df)

    logger.info(
        "Generated %d documents.",
        len(documents),
    )

    # -----------------------------------------------------------------
    # Basic validation
    # -----------------------------------------------------------------

    assert len(documents) == len(products_df), (
        "Expected one document per product."
    )

    logger.info("Document count validation passed.")

    # -----------------------------------------------------------------
    # Save first document for inspection
    # -----------------------------------------------------------------

    SAMPLE_OUTPUT.write_text(
        documents[0].text,
        encoding="utf-8",
    )

    logger.info(
        "Saved sample document to %s",
        SAMPLE_OUTPUT,
    )

    # -----------------------------------------------------------------
    # Console preview
    # -----------------------------------------------------------------

    print("=" * 100)
    print("DOCUMENT METADATA")
    print("=" * 100)

    print(documents[0].metadata)

    print("\n")
    print("=" * 100)
    print("DOCUMENT TEXT")
    print("=" * 100)

    print(documents[0].text)

    logger.info("Document Builder validation completed successfully.")


if __name__ == "__main__":
    main()