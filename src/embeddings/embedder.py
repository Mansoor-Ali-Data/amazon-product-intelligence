"""
Embedding generation utilities.
"""

from __future__ import annotations

from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

DEFAULT_BATCH_SIZE = 32

# Load once when the module is imported.
model = SentenceTransformer(EMBEDDING_MODEL)


def embed_texts(
    texts: list[str],
    batch_size: int = DEFAULT_BATCH_SIZE,
) -> list[list[float]]:
    """
    Generate embeddings for a batch of texts.
    """

    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        convert_to_numpy=False,
        normalize_embeddings=True,
    )

    return embeddings

def embed_query(
    query: str,
) -> list[float]:
    """
    Generate an embedding for a single query.

    Args:
        query: User query to embed.

    Returns:
        Query embedding vector.
    """