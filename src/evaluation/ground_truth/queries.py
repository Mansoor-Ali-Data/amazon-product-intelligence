"""
Ground truth benchmark queries for retrieval evaluation.

Each query represents a realistic user search and is used to
generate candidate relevant products from the processed dataset.

The final approved candidates will become the benchmark dataset
used by the retrieval evaluator.
"""

from __future__ import annotations

from src.evaluation.enums import QueryCategory
from src.evaluation.ground_truth.models import GroundTruthQuery


GROUND_TRUTH_QUERIES: list[GroundTruthQuery] = [

    # ==========================================================
    # Brand Queries
    # ==========================================================

    GroundTruthQuery(
        id="brand_coofandy",
        query="Show me COOFANDY polo shirts.",
        relevant_asins=[],
        category=QueryCategory.BRAND,
        description="Retrieve all COOFANDY polo shirts.",
    ),

    GroundTruthQuery(
        id="brand_zity",
        query="Show me ZITY polo shirts.",
        relevant_asins=[],
        category=QueryCategory.BRAND,
        description="Retrieve all ZITY polo shirts.",
    ),

    GroundTruthQuery(
        id="brand_m_maelreg",
        query="Show me M MAELREG golf shirts.",
        relevant_asins=[],
        category=QueryCategory.BRAND,
        description="Retrieve golf shirts from M MAELREG.",
    ),

    # ==========================================================
    # Feature Queries
    # ==========================================================

    GroundTruthQuery(
        id="feature_quick_dry",
        query="Show quick dry polo shirts.",
        relevant_asins=[],
        category=QueryCategory.FEATURE,
        description="Retrieve quick-dry polo shirts.",
    ),

    GroundTruthQuery(
        id="feature_moisture_wicking",
        query="Show moisture wicking polo shirts.",
        relevant_asins=[],
        category=QueryCategory.FEATURE,
        description="Retrieve moisture-wicking polo shirts.",
    ),

    GroundTruthQuery(
        id="feature_lightweight",
        query="Show lightweight golf polo shirts.",
        relevant_asins=[],
        category=QueryCategory.FEATURE,
        description="Retrieve lightweight golf polo shirts.",
    ),

    # ==========================================================
    # Price Queries
    # ==========================================================

    GroundTruthQuery(
        id="price_under_20",
        query="Show polo shirts under $20.",
        relevant_asins=[],
        category=QueryCategory.PRICE,
        description="Retrieve polo shirts priced below $20.",
    ),

    GroundTruthQuery(
        id="price_under_30",
        query="Show polo shirts under $30.",
        relevant_asins=[],
        category=QueryCategory.PRICE,
        description="Retrieve polo shirts priced below $30.",
    ),

    # ==========================================================
    # Rating Queries
    # ==========================================================

    GroundTruthQuery(
        id="rating_above_45",
        query="Show polo shirts rated above 4.5 stars.",
        relevant_asins=[],
        category=QueryCategory.RATING,
        description="Retrieve highly-rated polo shirts.",
    ),

    GroundTruthQuery(
        id="rating_best",
        query="Show the highest rated golf polo shirts.",
        relevant_asins=[],
        category=QueryCategory.RATING,
        description="Retrieve the highest-rated golf polo shirts.",
    ),

    # ==========================================================
    # Recommendation Queries
    # ==========================================================

    GroundTruthQuery(
        id="recommend_golf",
        query="Recommend a golf polo shirt.",
        relevant_asins=[],
        category=QueryCategory.RECOMMENDATION,
        description="General recommendation for golf polo shirts.",
    ),

    GroundTruthQuery(
        id="recommend_performance",
        query="Recommend a performance polo shirt.",
        relevant_asins=[],
        category=QueryCategory.RECOMMENDATION,
        description="Recommend performance polo shirts suitable for sports.",
    ),
]