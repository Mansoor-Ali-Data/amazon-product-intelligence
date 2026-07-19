"""
Validate the embedding generation pipeline.

This script loads the processed datasets, generates documents, chunks them,
creates embeddings, validates the results, and saves a sample embedded chunk.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from src.document_builder.builder import build_documents
from src.chunking.builder import build_chunks
from .builder import build_embeddings

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
    / "sample_embedding.txt"
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

    logger.info("Generating documents...")

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

    logger.info(
        "Generated %d chunks.",
        len(chunks),
    )

    logger.info("Generating embeddings...")

    embedded_chunks = build_embeddings(chunks)

    logger.info(
        "Generated %d embeddings.",
        len(embedded_chunks),
    )

    # -------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------

    dimensions = {
        len(chunk.embedding)
        for chunk in embedded_chunks
    }

    duplicate_ids = len(embedded_chunks) - len(
        {chunk.id for chunk in embedded_chunks}
    )

    logger.info(
        "Embedding dimension(s): %s",
        sorted(dimensions),
    )

    logger.info(
        "Duplicate IDs: %d",
        duplicate_ids,
    )

    assert len(dimensions) == 1
    assert duplicate_ids == 0

    sample = embedded_chunks[0]

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8",
    ) as file:

        file.write("=" * 100)
        file.write("\nEMBEDDING METADATA\n")
        file.write("=" * 100)
        file.write("\n\n")

        file.write(str(sample.metadata))

        file.write("\n\n")

        file.write("=" * 100)
        file.write("\nTEXT\n")
        file.write("=" * 100)
        file.write("\n\n")

        file.write(sample.text)

        file.write("\n\n")

        file.write("=" * 100)
        file.write("\nEMBEDDING\n")
        file.write("=" * 100)
        file.write("\n\n")

        file.write(f"Dimension: {len(sample.embedding)}\n\n")

        file.write(
            str(sample.embedding[:10])
        )

    logger.info(
        "Saved sample embedding to %s",
        OUTPUT_PATH.relative_to(PROJECT_ROOT),
    )

    print("=" * 100)
    print("EMBEDDING METADATA")
    print("=" * 100)
    print(sample.metadata)

    print()

    print("=" * 100)
    print("TEXT")
    print("=" * 100)
    print()

    print(sample.text[:1000])

    print()

    print("=" * 100)
    print("EMBEDDING")
    print("=" * 100)
    print()

    print(f"Dimension: {len(sample.embedding)}")

    print(sample.embedding[:10])

    logger.info(
        "Embedding validation completed successfully."
    )


if __name__ == "__main__":
    main()