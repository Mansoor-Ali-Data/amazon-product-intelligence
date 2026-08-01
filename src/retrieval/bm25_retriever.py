"""
BM25 lexical retriever.

Retrieves relevant chunks using a BM25 lexical index.
"""

from __future__ import annotations

from operator import itemgetter

from rank_bm25 import BM25Okapi

from src.bm25_store.store import BM25Store
from src.indexing.bm25_models import BM25IndexData
from src.retrieval.models import RetrievedChunk


class BM25Retriever:
    """
    Retrieves document chunks using BM25 lexical search.
    """

    def __init__(
        self,
        store: BM25Store | None = None,
    ) -> None:
        """
        Initialize the BM25 retriever.
        """

        self._store = store or BM25Store()

        (
            self._bm25,
            self._index_data,
        ) = self._store.load()

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[RetrievedChunk]:
        """
        Retrieve the most relevant chunks for a query.
        """

        query_tokens = self._tokenize(
            query,
        )

        ranked_indices = self._rank_documents(
            query_tokens=query_tokens,
            top_k=top_k,
        )

        return self._build_results(
            ranked_indices=ranked_indices,
        )

    @staticmethod
    def _tokenize(
        text: str,
    ) -> list[str]:
        """
        Tokenize a query for BM25 retrieval.
        """

        return text.lower().split()

    def _rank_documents(
        self,
        query_tokens: list[str],
        top_k: int,
    ) -> list[tuple[int, float]]:
        """
        Rank documents using BM25.

        Returns
        -------
        list[tuple[int, float]]
            (document_index, score)
        """

        scores = self._bm25.get_scores(
            query_tokens,
        )

        ranked = sorted(
            enumerate(scores),
            key=itemgetter(1),
            reverse=True,
        )

        return ranked[:top_k]

    def _build_results(
        self,
        ranked_indices: list[tuple[int, float]],
    ) -> list[RetrievedChunk]:
        """
        Convert ranked BM25 results into RetrievedChunk objects.
        """

        results: list[RetrievedChunk] = []

        for rank, (index, score) in enumerate(
            ranked_indices,
            start=1,
        ):

            metadata = self._index_data.metadatas[index]

            results.append(
                RetrievedChunk(
                    id=self._index_data.chunk_ids[index],
                    text=self._index_data.documents[index],
                    metadata=metadata,
                    distance=-score,
                    rank=rank,
                    asin=metadata["asin"],
                    chunk_index=metadata["chunk_index"],
                )
            )

        return results