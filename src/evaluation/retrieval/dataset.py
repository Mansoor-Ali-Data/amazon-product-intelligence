"""
Ground-truth benchmark dataset for retrieval evaluation.

Each evaluation example contains:

- A natural language query.
- The expected relevant ASIN(s).
- A query category.
- A short description of what is being tested.

This dataset is manually curated from the processed Amazon Fashion
products dataset and serves as the benchmark for retrieval evaluation.
"""

from __future__ import annotations

from dataclasses import dataclass
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


@dataclass(frozen=True, slots=True)
class EvaluationExample:
    """
    Represents a single retrieval evaluation example.
    """

    query: str
    expected_asins: list[str]
    category: QueryCategory
    description: str

EVALUATION_DATASET: list[EvaluationExample] = [

    # ------------------------------------------------------------------
    # Recommendation
    # ------------------------------------------------------------------

    EvaluationExample(
        query="Recommend a men's polo shirt.",
        expected_asins=["B0B59BJG6Y"],
        category="recommendation",
        description="General recommendation for a men's polo shirt.",
    ),

    EvaluationExample(
        query="Recommend a moisture-wicking polo shirt.",
        expected_asins=[
            "B0DLGB4RYH",
            "B0DK5FZ325",
            "B0BGXTC1FR",
        ],
        category="recommendation",
        description="Retrieve moisture-wicking polo shirts.",
    ),

    EvaluationExample(
        query="Recommend a golf polo shirt.",
        expected_asins=[
            "B0DLGB4RYH",
            "B0DK5FZ325",
            "B0BGXTC1FR",
        ],
        category="recommendation",
        description="Retrieve golf polo shirts.",
    ),

    # ------------------------------------------------------------------
    # Brand
    # ------------------------------------------------------------------

    EvaluationExample(
        query="Show me ZITY polo shirts.",
        expected_asins=[
            "B0DRXF62JH",
            "B09MHPSWY2",
        ],
        category="brand",
        description="Retrieve products from the ZITY brand.",
    ),

    EvaluationExample(
        query="Show me COOFANDY polo shirts.",
        expected_asins=[
            "B0DLGB4RYH",
        ],
        category="brand",
        description="Retrieve products from COOFANDY.",
    ),

    EvaluationExample(
        query="Show me M MAELREG golf shirts.",
        expected_asins=[
            "B0DPQC1NSV",
            "B0CQTCDJJ7",
        ],
        category="brand",
        description="Retrieve products from M MAELREG.",
    ),

    # ------------------------------------------------------------------
    # Price
    # ------------------------------------------------------------------

    EvaluationExample(
        query="Recommend a polo shirt under $20.",
        expected_asins=[
            "B0DLGB4RYH",
        ],
        category="price",
        description="Retrieve affordable polo shirts.",
    ),

    EvaluationExample(
        query="Recommend polo shirts under $30.",
        expected_asins=[
            "B0DLGB4RYH",
            "B0BGXTC1FR",
            "B0CQTCDJJ7",
        ],
        category="price",
        description="Retrieve polo shirts priced below $30.",
    ),

    # ------------------------------------------------------------------
    # Rating
    # ------------------------------------------------------------------

    EvaluationExample(
        query="Show the highest rated polo shirts.",
        expected_asins=[
            "B0DK5FZ325",
            "B0DPQC1NSV",
        ],
        category="rating",
        description="Retrieve highly rated polo shirts.",
    ),

    # ------------------------------------------------------------------
    # Feature
    # ------------------------------------------------------------------

    EvaluationExample(
        query="Show quick dry polo shirts.",
        expected_asins=[
            "B0B59BJG6Y",
            "B0DK5FZ325",
            "B0BGSDG377",
        ],
        category="feature",
        description="Retrieve quick-dry polo shirts.",
    ),

    EvaluationExample(
        query="Show lightweight polo shirts.",
        expected_asins=[
            "B0CQTCDJJ7",
        ],
        category="feature",
        description="Retrieve lightweight polo shirts.",
    ),

    EvaluationExample(
        query="Show performance golf shirts.",
        expected_asins=[
            "B0DK5FZ325",
            "B0DPQC1NSV",
        ],
        category="feature",
        description="Retrieve performance golf shirts.",
    ),
]