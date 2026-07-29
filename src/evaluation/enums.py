"""
Shared enumerations for the evaluation package.
"""

from __future__ import annotations

from enum import StrEnum


class QueryCategory(StrEnum):
    """
    Categories used to organize retrieval benchmark queries.
    """

    RECOMMENDATION = "recommendation"
    BRAND = "brand"
    FEATURE = "feature"
    PRICE = "price"
    RATING = "rating"
    COMPARISON = "comparison"