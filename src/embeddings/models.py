"""
Data models for embedding generation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class EmbeddedChunk:
    """
    A chunk enriched with its embedding vector.
    """

    id: str
    text: str
    embedding: list[float]
    metadata: dict[str, Any]