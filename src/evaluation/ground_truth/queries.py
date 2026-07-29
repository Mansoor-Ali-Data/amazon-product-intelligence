"""
Ground truth benchmark queries for retrieval evaluation.

Each query represents a realistic user search and is used to
generate candidate relevant products from the processed dataset.

The final approved candidates will become the benchmark dataset
used by the retrieval evaluator.
"""

from __future__ import annotations

from src.evaluation.enums import QueryCategory
from src.evaluation.ground_truth.models import GroundTruthExample


GROUND_TRUTH_QUERIES: list[GroundTruthExample] = [

    # ==========================================================
    # Brand Queries
    # ==========================================================

    GroundTruthExample(
        id="brand_coofandy",
        query="Show me COOFANDY polo shirts.",
        relevant_asins=[],
        category=QueryCategory.BRAND,
        description="Retrieve all COOFANDY polo shirts.",
        search_terms=[
            "coofandy",
        ],
    ),

    GroundTruthExample(
        id="brand_zity",
        query="Show me ZITY polo shirts.",
        relevant_asins=[],
        category=QueryCategory.BRAND,
        description="Retrieve all ZITY polo shirts.",
        search_terms=[
            "zity",
        ],
    ),

    # ==========================================================
    # Feature Queries
    # ==========================================================

    GroundTruthExample(
        id="feature_quick_dry",
        query="Show quick dry polo shirts.",
        relevant_asins=[],
        category=QueryCategory.FEATURE,
        description="Retrieve quick-dry polo shirts.",
        search_terms=[
                "quick dry",
        ],
    ),
    

    GroundTruthExample(
        id="feature_moisture_wicking",
        query="Show moisture wicking polo shirts.",
        relevant_asins=[],
        category=QueryCategory.FEATURE,
        description="Retrieve moisture-wicking polo shirts.",
        search_terms=[
            "moisture wicking",
    ],

    ),

    GroundTruthExample(
        id="feature_lightweight",
        query="Show lightweight golf polo shirts.",
        relevant_asins=[],
        category=QueryCategory.FEATURE,
        description="Retrieve lightweight golf polo shirts.",
        search_terms=[
            "lightweight", 
            "polo",
    ],

    ),

    # ==========================================================
    # Price Queries
    # ==========================================================

    GroundTruthExample(
        id="price_under_20",
        query="Show products under $20.",
        relevant_asins=[],
        category=QueryCategory.PRICE,
        description="Retrieve products priced below $20.",
        search_terms= ["polo",]
    ),

    GroundTruthExample(
        id="price_under_30",
        query="Show products under $30.",
        relevant_asins=[],
        category=QueryCategory.PRICE,
        description="Retrieve products priced below $30.",
        search_terms= []
    ),

    # ==========================================================
    # Rating Queries
    # ==========================================================

    GroundTruthExample(
        id="rating_above_45",
        query="Show products rated above 4.5 stars.",
        relevant_asins=[],
        category=QueryCategory.RATING,
        description="Retrieve highly-rated products.",
        search_terms= []
    ),

    GroundTruthExample(
        id="rating_best",
        query="Show the highest rated product",
        relevant_asins=["polo",],
        category=QueryCategory.RATING,
        description="Retrieve the highest-rated products.",
        search_terms= []
    ),

    # ==========================================================
    # Recommendation Queries
    # ==========================================================

    GroundTruthExample(
        id="recommend_golf",
        query="Recommend a golf polo shirt.",
        relevant_asins=[],
        category=QueryCategory.RECOMMENDATION,
        description="General recommendation for golf polo shirts.",
        search_terms= ["golf",
                       "polo",
                       "shirt",
        ]
    ),

    GroundTruthExample(
        id="recommend_performance",
        query="Recommend a performance polo shirt.",
        relevant_asins=[],
        category=QueryCategory.RECOMMENDATION,
        description="Recommend performance polo shirts suitable for sports.",
        search_terms=["performance",
                      "polo",
                      "shirts",
        ]
    ),
]