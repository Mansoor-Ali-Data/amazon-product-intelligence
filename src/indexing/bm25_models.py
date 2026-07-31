"""
Data models for BM25 indexing.

These models represent the lexical corpus used to build
the BM25 search index.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class BM25Document:
    """
    Document stored in the BM25 corpus.

    Each document corresponds to a single chunk used by
    the retrieval system.
    """

    chunk_id: str

    text: str

    metadata: dict[str, Any]


@dataclass(frozen=True, slots=True)
class BM25IndexData:
    """
    Input corpus for building a BM25 index.

    The corpus is built from the same chunks that are
    indexed into the vector store, ensuring both retrieval
    systems operate over an identical collection.
    """

    documents: list[BM25Document]