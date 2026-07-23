"""
Retriever implementation.

Responsibilities
----------------
- Embed user queries
- Search the vector store
- Convert search results into RetrievedChunk objects
"""

from __future__ import annotations

from src.embeddings.embedder import embed_query

from src.retrieval.models import RetrievedChunk
from src.vector_store.chroma_store import VectorStore
from src.vector_store.models import SearchResult




class Retriever:
    """
    Retrieves the most relevant chunks for a user query.
    """

    def __init__(
        self,
        vector_store: VectorStore,
    ) -> None:

        self._vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[RetrievedChunk]:
        """
        Retrieve the most relevant chunks for a query.

        Args:
            query:
                User question.

            top_k:
                Maximum number of chunks to return.

        Returns:
            Ranked RetrievedChunk objects.
        """

        query_embedding = embed_query(query)

        search_result = self._vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        return self._build_results(search_result)

    def _build_results(
        self,
        search_result: SearchResult,
    ) -> list[RetrievedChunk]:
        """
        Convert SearchResult into RetrievedChunk objects.
        """

        retrieved_chunks: list[RetrievedChunk] = []

        for rank, (
            chunk_id,
            text,
            metadata,
            distance,
        ) in enumerate(
            zip(
                search_result.ids,
                search_result.documents,
                search_result.metadatas,
                search_result.distances,
            ),
            start=1,
        ):

            retrieved_chunks.append(
                RetrievedChunk(
                    id=chunk_id,
                    text=text,
                    metadata=metadata,
                    distance=distance,
                    rank=rank,
                    asin=metadata["asin"],
                    chunk_index=metadata["chunk_index"],
                )
            )

        return retrieved_chunks