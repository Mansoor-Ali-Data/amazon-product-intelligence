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
    try:
        logger.info("Starting offline indexing pipeline.")

        # ------------------------------------------------------------------
        # Load processed datasets
        # ------------------------------------------------------------------
        products_df, reviews_df = load_processed_data()

        logger.info("Processed datasets loaded successfully.")

        # ------------------------------------------------------------------
        # Build documents
        # ------------------------------------------------------------------
        documents = build_documents(
            products_df=products_df,
            reviews_df=reviews_df,
        )

        logger.info(
            "Generated %d documents.",
            len(documents),
        )

        # ------------------------------------------------------------------
        # Chunk documents
        # ------------------------------------------------------------------
        chunks = build_chunks(
            documents=documents,
        )

        logger.info(
            "Generated %d chunks.",
            len(chunks),
        )

        # ------------------------------------------------------------------
        # Generate embeddings
        # ------------------------------------------------------------------
        embedded_chunks = build_embeddings(
            chunks=chunks,
        )

        logger.info(
            "Generated %d embeddings.",
            len(embedded_chunks),
        )

        # ------------------------------------------------------------------
        # Build vector store batch
        # ------------------------------------------------------------------
        vector_store_batch = VectorStoreBuilder().build(
            embedded_chunks=embedded_chunks,
        )

        logger.info(
            "Prepared %d records for vector storage.",
            len(vector_store_batch.ids),
        )

        # ------------------------------------------------------------------
        # Persist to ChromaDB
        # ------------------------------------------------------------------
        vector_store = VectorStore()

        vector_store.add_documents(
            ids=vector_store_batch.ids,
            documents=vector_store_batch.documents,
            embeddings=vector_store_batch.embeddings,
            metadatas=vector_store_batch.metadatas,
        )

        logger.info(
            "Vector store contains %d vectors.",
            vector_store.count(),
        )

        logger.info("Offline indexing pipeline completed successfully.")

    except Exception:
        logger.exception("Offline indexing pipeline failed.")
        raise