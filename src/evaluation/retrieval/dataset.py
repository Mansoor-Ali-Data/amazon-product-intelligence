"""
Ground-truth benchmark dataset for retrieval evaluation.

Each evaluation example contains:

- A natural language query.
- The expected relevant ASIN(s).
- The benchmark type.
- A query category.
- A short description of what is being tested.

This dataset is manually curated from the processed Amazon Fashion
products dataset and serves as the benchmark for retrieval evaluation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from src.evaluation.retrieval.rules import RelevanceRule
from src.evaluation.retrieval.rules import RuleOperator
from src.evaluation.retrieval.enums import  ( QueryCategory , BenchmarkType)





@dataclass(frozen=True, slots=True)
class EvaluationExample:
    """
    Represents a single retrieval evaluation example.
    """

    query: str
    expected_asins: list[str]
    benchmark: BenchmarkType
    category: QueryCategory
    rules: list[RelevanceRule]
    description: str


EVALUATION_DATASET: list[EvaluationExample] = [

    # ------------------------------------------------------------------
    # Recommendation
    # ------------------------------------------------------------------

    EvaluationExample(
        query="Recommend a men's polo shirt.",
        expected_asins=[
            "B0B59BJG6Y",
        ],
        benchmark=BenchmarkType.SEMANTIC,
        category=QueryCategory.RECOMMENDATION,
        description="General recommendation for a men's polo shirt.",
        rules=[]
    ),

    EvaluationExample(
        query="Recommend a moisture-wicking polo shirt.",
        expected_asins=[
            "B0DLGB4RYH",
            "B0DK5FZ325",
            "B0BGXTC1FR",
        ],
        benchmark=BenchmarkType.SEMANTIC,
        category=QueryCategory.RECOMMENDATION,
        description="Retrieve moisture-wicking polo shirts.",
        rules=[
            RelevanceRule(
                field="title",
                operator=RuleOperator.CONTAINS,
                value="moisture wicking",
            )
        ]
    ),

    EvaluationExample(
        query="Recommend a golf polo shirt.",
        expected_asins=[
            "B0DLGB4RYH",
            "B0DK5FZ325",
            "B0BGXTC1FR",
        ],
        benchmark=BenchmarkType.SEMANTIC,
        category=QueryCategory.RECOMMENDATION,
        description="Retrieve golf polo shirts.",
        rules=[
            RelevanceRule(
                field="title",
                operator=RuleOperator.CONTAINS,
                value="golf",
            )
        ]
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
        benchmark=BenchmarkType.SEMANTIC,
        category=QueryCategory.BRAND,
        description="Retrieve products from the ZITY brand.",
        rules=[
            RelevanceRule(
                field="brand",
                operator=RuleOperator.EQUALS,
                value="ZITY Store",
            )
        ]
    ),

    EvaluationExample(
        query="Show me COOFANDY polo shirts.",
        expected_asins=[
            "B0DLGB4RYH",
        ],
        benchmark=BenchmarkType.SEMANTIC,
        category=QueryCategory.BRAND,
        description="Retrieve products from COOFANDY.",
        rules=[
            RelevanceRule(
                field="brand",
                operator=RuleOperator.EQUALS,
                value="COOFANDY Store",
            )
        ]
    ),

    EvaluationExample(
        query="Show me M MAELREG golf shirts.",
        expected_asins=[
            "B0DPQC1NSV",
            "B0CQTCDJJ7",
        ],
        benchmark=BenchmarkType.SEMANTIC,
        category=QueryCategory.BRAND,
        description="Retrieve products from M MAELREG.",
        rules=[
            RelevanceRule(
                field="brand",
                operator=RuleOperator.EQUALS,
                value="M MAELREG Store",
            )
        ]
    ),

    # ------------------------------------------------------------------
    # Price (Metadata Retrieval)
    # ------------------------------------------------------------------

    EvaluationExample(
        query="Recommend a polo shirt under $20.",
        expected_asins=[
            "B0DLGB4RYH",
        ],
        benchmark=BenchmarkType.METADATA,
        category=QueryCategory.PRICE,
        description="Retrieve polo shirts priced below $20.",
        rules=[
            RelevanceRule(
                field="price",
                operator=RuleOperator.LESS_EQUAL,
                value=20.0,
            )
        ]
    ),

    EvaluationExample(
        query="Recommend polo shirts under $30.",
        expected_asins=[
            "B0DLGB4RYH",
            "B0BGXTC1FR",
            "B0CQTCDJJ7",
        ],
        benchmark=BenchmarkType.METADATA,
        category=QueryCategory.PRICE,
        description="Retrieve polo shirts priced below $30.",
        rules=[
            RelevanceRule(
                field="price",
                operator=RuleOperator.LESS_EQUAL,
                value=30.0,
            )
        ]
    ),

    # ------------------------------------------------------------------
    # Rating (Metadata Retrieval)
    # ------------------------------------------------------------------

    EvaluationExample(
        query="Show the highest rated polo shirts.",
        expected_asins=[
            "B0DK5FZ325",
            "B0DPQC1NSV",
        ],
        benchmark=BenchmarkType.METADATA,
        category=QueryCategory.RATING,
        description="Retrieve the highest rated polo shirts.",
        rules=[
            RelevanceRule(
                field="rating",
                operator=RuleOperator.GREATER_EQUAL,
                value=4.0,
            )
        ]
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
        benchmark=BenchmarkType.SEMANTIC,
        category=QueryCategory.FEATURE,
        description="Retrieve quick-dry polo shirts.",
        rules=[
            RelevanceRule(
                field="title",
                operator=RuleOperator.CONTAINS,
                value="quick dry",
            )
        ]
    ),

    EvaluationExample(
        query="Show lightweight polo shirts.",
        expected_asins=[
            "B0CQTCDJJ7",
        ],
        benchmark=BenchmarkType.SEMANTIC,
        category=QueryCategory.FEATURE,
        description="Retrieve lightweight polo shirts.",
        rules=[
            RelevanceRule(
                field="title",
                operator=RuleOperator.CONTAINS,
                value="lightweight",
            )
        ]
    ),

    EvaluationExample(
        query="Show performance golf shirts.",
        expected_asins=[
            "B0DK5FZ325",
            "B0DPQC1NSV",
        ],
        benchmark=BenchmarkType.SEMANTIC,
        category=QueryCategory.FEATURE,
        description="Retrieve performance golf shirts.",
        rules=[
            RelevanceRule(
                field="title",
                operator=RuleOperator.CONTAINS,
                value="performance",
            )
        ]
    ),
]


# ------------------------------------------------------------------
# Benchmark Views
# ------------------------------------------------------------------

SEMANTIC_BENCHMARK: list[EvaluationExample] = [
    example
    for example in EVALUATION_DATASET
    if example.benchmark == BenchmarkType.SEMANTIC
]

METADATA_BENCHMARK: list[EvaluationExample] = [
    example
    for example in EVALUATION_DATASET
    if example.benchmark == BenchmarkType.METADATA
]


def get_semantic_benchmark() -> list[EvaluationExample]:
    """
    Return the semantic retrieval benchmark.
    """

    return SEMANTIC_BENCHMARK


def get_metadata_benchmark() -> list[EvaluationExample]:
    """
    Return the metadata retrieval benchmark.
    """

    return METADATA_BENCHMARK