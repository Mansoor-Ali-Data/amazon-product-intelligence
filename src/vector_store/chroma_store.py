"""
ChromaDB-backed implementation of the project's Vector Store.

Responsibilities
----------------
- Load vector store configuration
- Initialize the ChromaDB persistent client
- Create or load the configured collection

This class intentionally hides ChromaDB implementation details from
the rest of the application.
"""

from __future__ import annotations

from typing import Any

import chromadb
from chromadb.api import ClientAPI
from chromadb.api.models.Collection import Collection

from config.loader import load_yaml
from config.logging import get_logger
logger = get_logger(__name__)

from .models import SearchResult

class VectorStore:
    """
    ChromaDB-backed vector store.

    This class manages the lifecycle of the vector database and provides
    a clean interface for storing and retrieving vector embeddings.
    """

    def __init__(
        self,
        collection_name: str | None = None,
    ) -> None:
        """Initialize the vector store."""

        self._config: dict[str, Any] = self._load_config()
        self._collection_name = (
            collection_name
            or self._config["collection_name"]
        )
        self._client: ClientAPI = self._create_client()
        self._collection: Collection = self._create_collection()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add_documents(
        self,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, Any]],
    ) -> None:
        """
        Add documents and their embeddings to the ChromaDB collection.

        Args:
            ids: Unique IDs for each document.
            documents: Text content of the documents.
            embeddings: Embedding vectors corresponding to each document.
            metadatas: Metadata dictionaries associated with each document.

        Raises:
            ValueError: If the input lists have different lengths.
        """
        if not (
            len(ids)
            == len(documents)
            == len(embeddings)
            == len(metadatas)
        ):
            raise ValueError(
            "ids, documents, embeddings, and metadatas must have the same length."
        )

        self._collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            
        )

        logger.info(
            "Added %d vectors to collection '%s'.",
            len(ids),
            self._collection.name,
        )


    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> SearchResult:
        """
        Perform semantic search using a query embedding.

        Args:
            query_embedding: Embedding vector of the query.
            top_k: Maximum number of results.

        Returns:
            Search results returned by ChromaDB.
    """
        results = self._collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )
        return SearchResult(
            ids=results["ids"][0],
            documents=results["documents"][0],
            metadatas=results["metadatas"][0],
            distances=results["distances"][0],
)

    def count(self) -> int:
        """
        Return the total number of documents in the collection.

        Returns:
            Number of stored documents.
        """
        return self._collection.count()


    def peek(self, limit: int = 5) -> dict[str, Any]:
        """
        Retrieve a small sample of stored documents.

        Args:
            limit: Maximum number of documents to return.

        Returns:
            Dictionary containing stored records.
        """
        return self._collection.peek(limit=limit)

    def reset(self) -> None:
        """
        Delete and recreate the collection.

        Raises:
            RuntimeError: If reset is disabled.
        """
        if not self._config["allow_reset"]:
            raise RuntimeError("Vector store reset is disabled.")

        collection_name = self._collection_name

        try:
            self._client.delete_collection(collection_name)
        except Exception:
            logger.info("Collection '%s' does not exist.", collection_name)

        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={
            "hnsw:space": self._config["distance_metric"]
        },
    ) 
    
    # ------------------------------------------------------------------
    # Private Helpers
    # ------------------------------------------------------------------

    def _load_config(self) -> dict[str, Any]:
        """
        Load the Vector Store configuration.

        Returns:
            Parsed vector store configuration.
        """
        return load_yaml("vector_store.yaml")["vector_store"]

    def _create_client(self) -> ClientAPI:
        """
        Create the ChromaDB persistent client.

        Returns:
            Initialized ChromaDB client.
        """
        return chromadb.PersistentClient(
            path=self._config["persist_directory"]
        )

    def _create_collection(self) -> Collection:
        """
        Create or load the configured ChromaDB collection.

        Returns:
            ChromaDB collection.
        """
        return self._client.get_or_create_collection(
            name=self._collection_name,
            metadata={
                "hnsw:space": self._config["distance_metric"]
            },
        )