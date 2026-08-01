from __future__ import annotations
from importlib.resources import path
"""
Offline indexing pipeline.

Coordinates the complete document indexing workflow from processed datasets
to vector database storage and BM25 Artiifact storage.
"""


from config.logging import get_logger

from src.data.data_loader import load_processed_data
from src.chunking.builder import build_chunks
from src.document_builder.builder import build_documents
from src.embeddings.builder import build_embeddings
from src.vector_store.builder import VectorStoreBuilder
from src.vector_store.chroma_store import VectorStore

from src.indexing.bm25_index import BM25IndexBuilder
from src.bm25_store.builder import BM25StoreBuilder
from src.bm25_store.store import BM25Store

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
        #  Build Dense Vector Store (ChromaDB)
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
        

        # ------------------------------------------------------------------
        # Build BM25 Lexical Store
        # ------------------------------------------------------------------
        bm25_index_data = BM25IndexBuilder().build(
            chunks=chunks,
        )

        bm25 = BM25StoreBuilder().build(
            index_data=bm25_index_data,
        )

        bm25_store = BM25Store()

        bm25_store.save(
            bm25=bm25,
            index_data=bm25_index_data,
        )
        logger.info(
            "BM25 index built successfully."
        )

        logger.info(
            "BM25 lexical store persisted to artifacts/.",
        )

        logger.info("Offline indexing pipeline completed successfully.")

    except Exception:
        logger.exception("Offline indexing pipeline failed.")
        raise



