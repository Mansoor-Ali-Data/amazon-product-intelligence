"""
Shared enums for retrieval evaluation.
"""

from __future__ import annotations

from enum import StrEnum


class QueryCategory(StrEnum):
    """
    Supported retrieval evaluation query categories.
    """

    RECOMMENDATION = "recommendation"
    BRAND = "brand"
    PRICE = "price"
    FEATURE = "feature"
    RATING = "rating"
    COMPARISON = "comparison"


class BenchmarkType(StrEnum):
    """
    Supported retrieval benchmark types.
    """

    SEMANTIC = "semantic"
    METADATA = "metadata"


class RuleOperator(StrEnum):
    """
    Supported relevance rule operators.
    """

    EQUALS = "equals"
    CONTAINS = "contains"
    GREATER_EQUAL = "greater_equal"
    LESS_EQUAL = "less_equal"