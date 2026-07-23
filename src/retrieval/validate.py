"""
Validate the retrieval pipeline.
"""

from __future__ import annotations
import logging
from src.vector_store.chroma_store import VectorStore
from src.retrieval.retriever import Retriever


logger = logging.getLogger(__name__)

def main() -> None:

    vector_store = VectorStore()

    retriever = Retriever(vector_store)

    results = retriever.retrieve(
        query = "men polo shirt",
            
        top_k=5,
    )

    print("=" * 80)
    print("Retrieved Chunks")
    print("=" * 80)

    

    logger.info("Query: %s",query)

    for chunk in results:
        logger.info(
            "[Rank %d | Distance %.4f] %s",
            chunk.rank,
            chunk.distance,
            chunk.asin,
    )


if __name__ == "__main__":
    main()