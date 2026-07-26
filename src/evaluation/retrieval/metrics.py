"""
Retrieval evaluation metrics.

This module implements pure evaluation metrics used to measure the
quality of document retrieval.

The functions operate on a single query. Dataset-level metrics (e.g.
Mean Reciprocal Rank) are computed by the evaluator.
"""

from __future__ import annotations


def relevant_count(
    expected_asins: list[str],
    retrieved_asins: list[str],
) -> int:
    """
    Return the number of relevant retrieved ASINs.

    Args:
        expected_asins:
            Ground-truth relevant ASINs.

        retrieved_asins:
            Retrieved ASINs.

    Returns:
        Number of relevant retrieved products.
    """

    expected = set(expected_asins)
    retrieved = set(retrieved_asins)

    return len(expected & retrieved)


def first_relevant_rank(
    expected_asins: list[str],
    retrieved_asins: list[str],
) -> int | None:
    """
    Return the rank of the first relevant retrieved document.

    Rank is 1-based.

    Args:
        expected_asins:
            Ground-truth relevant ASINs.

        retrieved_asins:
            Retrieved ASINs ordered by retrieval score.

    Returns:
        Rank of the first relevant document, or None if no relevant
        document was retrieved.
    """

    expected = set(expected_asins)

    for rank, asin in enumerate(
        retrieved_asins,
        start=1,
    ):
        if asin in expected:
            return rank

    return None


def hit_rate(
    expected_asins: list[str],
    retrieved_asins: list[str],
) -> float:
    """
    Compute Hit Rate.

    Hit Rate is 1.0 if at least one relevant document is retrieved,
    otherwise 0.0.
    """

    return (
        1.0
        if relevant_count(
            expected_asins,
            retrieved_asins,
        )
        > 0
        else 0.0
    )


def precision_at_k(
    expected_asins: list[str],
    retrieved_asins: list[str],
) -> float:
    """
    Compute Precision@K.

    Precision@K measures the proportion of retrieved documents that
    are relevant.
    """

    if not retrieved_asins:
        return 0.0

    return relevant_count(
        expected_asins,
        retrieved_asins,
    ) / len(retrieved_asins)


def recall_at_k(
    expected_asins: list[str],
    retrieved_asins: list[str],
) -> float:
    """
    Compute Recall@K.

    Recall@K measures the proportion of relevant documents that were
    successfully retrieved.
    """

    if not expected_asins:
        return 0.0

    return relevant_count(
        expected_asins,
        retrieved_asins,
    ) / len(expected_asins)


def reciprocal_rank(
    expected_asins: list[str],
    retrieved_asins: list[str],
) -> float:
    """
    Compute Reciprocal Rank (RR).

    Reciprocal Rank is defined as:

        RR = 1 / rank

    where rank is the position of the first relevant retrieved
    document.

    If no relevant document is retrieved, RR is 0.0.
    """

    rank = first_relevant_rank(
        expected_asins,
        retrieved_asins,
    )

    if rank is None:
        return 0.0

    return 1.0 / rank