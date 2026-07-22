"""
Builder module for the vector store.

Responsible for converting application-level EmbeddedChunk objects into the
data format expected by the vector database. This acts as an adapter between
the embedding pipeline and the storage layer, keeping both components
independent and loosely coupled.
"""

from dataclasses import dataclass
from typing import Any

from src.embeddings.models import EmbeddedChunk


@dataclass(slots=True)
class VectorStoreBatch:
    """Container for data formatted for vector store insertion."""

    ids: list[str]
    documents: list[str]
    embeddings: list[list[float]]
    metadatas: list[dict[str, Any]]


class VectorStoreBuilder:
    """Build vector store batches from embedded chunks."""

    def build(
        self,
        embedded_chunks: list[EmbeddedChunk],
    ) -> VectorStoreBatch:
        ids: list[str] = []
        documents: list[str] = []
        embeddings: list[list[float]] = []
        metadatas: list[dict[str, Any]] = []

        for chunk in embedded_chunks:
            ids.append(chunk.id)
            documents.append(chunk.text)
            embeddings.append(chunk.embedding)
            metadatas.append(chunk.metadata)

        return VectorStoreBatch(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )