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


class VectorStore:
    """
    ChromaDB-backed vector store.

    This class manages the lifecycle of the vector database and provides
    a clean interface for storing and retrieving vector embeddings.
    """

    def __init__(self) -> None:
        """Initialize the vector store."""

        self._config: dict[str, Any] = self._load_config()
        self._client: ClientAPI = self._create_client()
        self._collection: Collection = self._create_collection()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add_documents(self) -> None:
        """Add embedded documents to the collection."""
        raise NotImplementedError

    def search(self):
        """Search the collection using a query embedding."""
        raise NotImplementedError

    def count(self) -> int:
        """Return the number of indexed vectors."""
        raise NotImplementedError

    def peek(self, limit: int = 5):
        """Return a sample of indexed documents."""
        raise NotImplementedError

    def reset(self) -> None:
        """Reset the vector store."""
        raise NotImplementedError

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
            name=self._config["collection_name"],
            metadata={
                "hnsw:space": self._config["distance_metric"]
            },
        )