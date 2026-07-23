"""
Data models for the Vector Store.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class SearchResult:
    """

    Represents the results of a vector similarity search.

    This model abstracts the underlying vector database response and
    prevents database-specific details from leaking into the retrieval
    layer.
    
    """

    ids: list[str]
    documents: list[str]
    metadatas: list[dict[str, Any]]
    distances: list[float]