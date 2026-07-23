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