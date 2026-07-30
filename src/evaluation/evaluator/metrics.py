"""
Retrieval evaluation metrics.

This module contains pure functions for computing retrieval metrics
for a single benchmark query.

These functions are independent of any retriever or vector database
implementation.
"""

from __future__ import annotations


def _count_relevant(
    expected_asins: set[str],
    retrieved_asins: list[str],
) -> int:
    """
    Count the number of relevant retrieved products.

    Parameters
    ----------
    expected_asins:
        Ground-truth relevant ASINs.

    retrieved_asins:
        ASINs returned by the retriever.

    Returns
    -------
    int
        Number of relevant retrieved products.
    """

    return len(
    expected_asins.intersection(retrieved_asins)
)


def calculate_recall(
    expected_asins: set[str],
    retrieved_asins: list[str],
) -> float:
    """
    Calculate Recall@K.

    Recall measures how many relevant products were retrieved.

    Parameters
    ----------
    expected_asins:
        Ground-truth relevant ASINs.

    retrieved_asins:
        Retrieved ASINs.

    Returns
    -------
    float
        Recall value in the range [0, 1].
    """

    if not expected_asins:
        return 0.0

    relevant = _count_relevant(
        expected_asins,
        retrieved_asins,
    )

    return relevant / len(expected_asins)


def calculate_precision(
    expected_asins: set[str],
    retrieved_asins: list[str],
) -> float:
    """
    Calculate Precision@K.

    Precision measures how many retrieved products
    are actually relevant.

    Parameters
    ----------
    expected_asins:
        Ground-truth relevant ASINs.

    retrieved_asins:
        Retrieved ASINs.

    Returns
    -------
    float
        Precision value in the range [0, 1].
    """

    if not retrieved_asins:
        return 0.0

    relevant = _count_relevant(
        expected_asins,
        retrieved_asins,
    )

    return relevant / len(retrieved_asins)


def calculate_hit_rate(
    expected_asins: set[str],
    retrieved_asins: list[str],
) -> bool:
    """
    Calculate Hit Rate@K.

    Hit Rate indicates whether at least one relevant
    product was retrieved.

    Parameters
    ----------
    expected_asins:
        Ground-truth relevant ASINs.

    retrieved_asins:
        Retrieved ASINs.

    Returns
    -------
    bool
        True if at least one relevant product was retrieved.
    """

    return any(
        asin in expected_asins
        for asin in retrieved_asins
    )


def calculate_reciprocal_rank(
    expected_asins: set[str],
    retrieved_asins: list[str],
) -> float:
    """
    Calculate Reciprocal Rank (RR).

    Reciprocal Rank is the inverse of the rank of the
    first relevant retrieved product.

    Parameters
    ----------
    expected_asins:
        Ground-truth relevant ASINs.

    retrieved_asins:
        Retrieved ASINs.

    Returns
    -------
    float
        Reciprocal Rank.

        Returns 0.0 if no relevant product is retrieved.
    """

    for rank, asin in enumerate(
        retrieved_asins,
        start=1,
    ):
        if asin in expected_asins:
            return 1.0 / rank

    return 0.0