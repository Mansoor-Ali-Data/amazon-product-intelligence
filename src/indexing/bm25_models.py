"""
Data models for BM25 indexing.

These models represent the lexical search index used by the
BM25 retriever.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class BM25IndexData:
    """
    BM25 lexical index.

    Stores the information required by the BM25 retriever
    to perform lexical search over the chunk corpus.
    """

    tokenized_documents: list[list[str]]

    documents: list[str]

    chunk_ids: list[str]

    metadatas: list[dict[str, Any]]