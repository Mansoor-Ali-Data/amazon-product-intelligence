"""
Data models for the retrieval layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class RetrievedChunk:
    """
    Represents a chunk retrieved from the vector store.

    This model is the domain object consumed by the retrieval pipeline.
    """

    id: str
    text: str
    metadata: dict[str, Any]

    distance: float
    rank: int

    asin: str
    chunk_index: int


@dataclass(frozen=True, slots=True)
class RetrievedProduct:
    """
    Represents a unique retrieved product.

    Multiple retrieved chunks belonging to the same product are
    collapsed into a single RetrievedProduct during evaluation.
    """

    asin: str

    rank: int

    distance: float

    metadata: dict[str, Any]