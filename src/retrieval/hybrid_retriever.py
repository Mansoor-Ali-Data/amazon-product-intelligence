"""
Hybrid retriever.

Combines semantic and lexical retrieval using
Reciprocal Rank Fusion (RRF).
"""

from __future__ import annotations

from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.fusion import ReciprocalRankFusion
from src.retrieval.models import RetrievedChunk
from src.retrieval.retriever import Retriever


class HybridRetriever:
    """
    Hybrid retrieval using Dense + BM25 retrieval.

    Retrieval results are merged using Reciprocal Rank Fusion (RRF).
    """

    def __init__(
        self,
        dense_retriever: Retriever,
        bm25_retriever: BM25Retriever,
        fusion: ReciprocalRankFusion | None = None,
    ) -> None:
        """
        Initialize the hybrid retriever.

        Args:
            dense_retriever:
                Semantic retriever.

            bm25_retriever:
                Lexical BM25 retriever.

            fusion:
                Rank fusion algorithm. Defaults to
                ReciprocalRankFusion.
        """

        self._dense = dense_retriever
        self._bm25 = bm25_retriever
        self._fusion = (
            fusion
            or ReciprocalRankFusion()
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[RetrievedChunk]:
        """
        Retrieve documents using hybrid retrieval.

        Args:
            query:
                User search query.

            top_k:
                Number of results to return.

        Returns:
            Ranked retrieved chunks.
        """

        dense_results = self._dense.retrieve(
            query=query,
            top_k=top_k,
        )

        bm25_results = self._bm25.retrieve(
            query=query,
            top_k=top_k,
        )

        fused_results = self._fusion.fuse(
            rankings=[
                dense_results,
                bm25_results,
            ],
        )

        return fused_results[:top_k]