"""
Build embedded chunks from text chunks.
"""

from __future__ import annotations

import logging

from .embedder import (
    DEFAULT_BATCH_SIZE,
    embed_texts,
)
from .models import EmbeddedChunk
from src.chunking.models import Chunk

logger = logging.getLogger(__name__)


def build_embeddings(
    chunks: list[Chunk],
    batch_size: int = DEFAULT_BATCH_SIZE,
) -> list[EmbeddedChunk]:
    """
    Generate embeddings for a collection of chunks.

    Args:
        chunks: Input text chunks.
        batch_size: Batch size used during embedding generation.

    Returns:
        List of embedded chunks.
    """

    logger.info(
        "Starting embedding generation for %d chunks.",
        len(chunks),
    )

    texts = [chunk.text for chunk in chunks]

    embeddings = embed_texts(
        texts=texts,
        batch_size=batch_size,
    )

    embedded_chunks = [
        EmbeddedChunk(
            id=chunk.id,
            text=chunk.text,
            embedding=embedding,
            metadata=chunk.metadata.copy(),
        )
        for chunk, embedding in zip(chunks, embeddings)
    ]

    logger.info(
        "Successfully generated %d embeddings.",
        len(embedded_chunks),
    )

    return embedded_chunks