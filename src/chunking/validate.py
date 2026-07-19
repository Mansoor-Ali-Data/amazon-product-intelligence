"""
Validate the chunking pipeline.

This script generates rich product documents, splits them into embedding-ready
chunks, performs integrity checks, and saves a sample chunk for inspection.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from src.document_builder.builder import build_documents
from .builder import build_chunks

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PRODUCTS_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "products.csv"
)

REVIEWS_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "reviews.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "sample_chunk.txt"
)


# ---------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------

def main() -> None:

    logger.info("Loading processed datasets...")

    products_df = pd.read_csv(PRODUCTS_PATH)
    reviews_df = pd.read_csv(REVIEWS_PATH)

    logger.info(
        "Loaded %d products and %d reviews.",
        len(products_df),
        len(reviews_df),
    )

    logger.info("Generating rich documents...")

    documents = build_documents(
        products_df,
        reviews_df,
    )

    logger.info(
        "Generated %d documents.",
        len(documents),
    )

    logger.info("Generating chunks...")

    chunks = build_chunks(documents)

    chunk_lengths = [
    len(chunk.text.split())
    for chunk in chunks
    ]

    logger.info(
        "Smallest chunk: %d words",
        min(chunk_lengths),
    )

    logger.info(
        "Largest chunk: %d words",
        max(chunk_lengths),
    )

    logger.info(
        "Average chunk size: %.1f words",
        sum(chunk_lengths) / len(chunk_lengths),
    )

    logger.info(
        "Generated %d chunks.",
        len(chunks),
    )

    # -------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------

    duplicate_ids = len(chunks) - len(
        {chunk.id for chunk in chunks}
    )

    empty_chunks = sum(
        1
        for chunk in chunks
        if not chunk.text.strip()
    )

    logger.info(
        "Average chunks per document: %.2f",
        len(chunks) / len(documents),
    )

    logger.info(
        "Duplicate chunk IDs: %d",
        duplicate_ids,
    )

    logger.info(
        "Empty chunks: %d",
        empty_chunks,
    )

    assert duplicate_ids == 0
    assert empty_chunks == 0

    # -------------------------------------------------------------
    # Save sample chunk
    # -------------------------------------------------------------

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    sample = chunks[0]

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8",
    ) as file:

        file.write("=" * 100)
        file.write("\nCHUNK METADATA\n")
        file.write("=" * 100)
        file.write("\n")

        file.write(str(sample.metadata))

        file.write("\n\n")

        file.write("=" * 100)
        file.write("\nCHUNK TEXT\n")
        file.write("=" * 100)
        file.write("\n\n")

        file.write(sample.text)

    logger.info(
        "Saved sample chunk to %s",
        OUTPUT_PATH.relative_to(PROJECT_ROOT),
    )

    print("=" * 100)
    print("CHUNK METADATA")
    print("=" * 100)
    print(sample.metadata)

    print()

    print("=" * 100)
    print("CHUNK TEXT")
    print("=" * 100)
    print()

    print(sample.text)

    logger.info(
        "Chunk validation completed successfully."
    )


if __name__ == "__main__":
    main()