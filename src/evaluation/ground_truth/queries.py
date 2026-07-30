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