"""
Offline indexing pipeline.

Coordinates the complete document indexing workflow from processed datasets
to vector database storage.
"""

from __future__ import annotations

from config.logging import get_logger

from src.data.data_loader import load_processed_data
from src.chunking.builder import build_chunks
from src.document_builder.builder import build_documents
from src.embeddings.builder import build_embeddings
from src.vector_store.builder import VectorStoreBuilder
from src.vector_store.chroma_store import VectorStore

logger = get_logger(__name__)


def run_indexing_pipeline() -> None:
    """
    Execute the offline indexing pipeline.
    """

    logger.info("Starting offline indexing pipeline.")

    products_df, reviews_df = load_processed_data()

    logger.info("Processed datasets loaded successfully.")

    documents = build_documents(
        products_df=products_df,
        reviews_df=reviews_df,
    )

    logger.info(
        "Generated %d documents.",
        len(documents),
    )

    # Remaining pipeline stages will be integrated incrementally.