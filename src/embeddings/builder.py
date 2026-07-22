"""
Build embedded chunks from text chunks.
"""
import time
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
    start_time = time.perf_counter()
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

    logger.info("Generated %d embeddings.", len(embedded_chunks))

    if embedded_chunks:
        sample_embedding = embedded_chunks[0].embedding

        logger.info(
            "Embedding dimension: %d",
            len(sample_embedding),
    )

        logger.info(
            "Sample embedding (first 10 values): %s",
            sample_embedding[:10],
    )

    elapsed = time.perf_counter() - start_time

    logger.info(
        "Embedding generation completed in %.2f seconds.",
        elapsed,
    )
    return embedded_chunks