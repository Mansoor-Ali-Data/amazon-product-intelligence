"""
Validate the retrieval pipeline.
"""

from __future__ import annotations
import logging
from src.vector_store.chroma_store import VectorStore
from src.retrieval.retriever import Retriever
import re

logger = logging.getLogger(__name__)

def main() -> None:

    vector_store = VectorStore()

    retriever = Retriever(vector_store)

    query = "men polo shirt"
    results = retriever.retrieve(
        query= query,
        top_k=5,
    )

    print(f"Retrieved {len(results)} chunks")
    print("=" * 80)
    print("Retrieved Chunks")
    print("=" * 80)
    print(f"Query     : {query}")
    print("=" * 80)

    for chunk in results:
        preview = re.sub(r"\s+", " ", chunk.text)
        preview = re.sub(r"[=]{2,}", "", preview)
        about_idx = preview.find("ABOUT THIS ITEM")

        if about_idx != -1:
            preview = preview[about_idx:]

        preview = preview[:200]

        print(f"Rank     : {chunk.rank}")
        print(f"Distance : {chunk.distance:.4f}")
        print(f"ASIN     : {chunk.asin}")
        print(f"Brand    : {chunk.metadata.get('brand_name', 'N/A')}")
        print()
        print("Preview:")
        print(preview + "...")
        print("-" * 80)

    

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