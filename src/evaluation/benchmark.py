"""
Finalized retrieval benchmark.

Semantic queries use manually approved relevant ASINs.

Metadata queries are evaluated using ExpectedFilter rather than
hardcoded ASIN lists.
"""

from src.evaluation.benchmark_models import (
    BenchmarkQuery,
    ExpectedFilter,
)
from src.evaluation.enums import QueryCategory


BENCHMARKS: list[BenchmarkQuery] = [

    # ==========================================================
    # Semantic Retrieval Benchmarks
    # ==========================================================

    BenchmarkQuery(
        query_id="recommend_golf",
        category=QueryCategory.RECOMMENDATION,
        query="Recommend a golf polo shirt.",
        relevant_asins = [
                "B0B59BJG6Y",
                "B0DLGB4RYH",
                "B0DRXF62JH",
                "B0DK5FZ325",
                "B0BGXTC1FR",
                "B0BGSDG377",
                "B0CXDL2NP6",
                "B09MHPSWY2",
                "B0DPQC1NSV",
                "B0DWXNDJPK",
                "B0DWFMDQBT",
                "B0CQTCDJJ7",
                "B005LCMU00",
                "B0DSBXZY87",
                "B0C8GBQ3QS",
                "B08SM3CDLN",
                "B00PUAO7MM",
                "B0DN375DNC",
                "B0CS69YKZQ",
                "B0D38YFY3K",
                "B07TF5NCTY",
                "B0DR7WSCFQ",
                "B0DJ6QSC4R",
                "B0BXSP3W6R",
                "B09TK9248H",
                "B0D9GXG945",
                "B0C1SC8PR9",
                "B0DPWXCXBX",
                "B0CQY7PMMK",
                "B09MHS6C6Z",
                "B0D391J394",
                "B0DRXCWRYM",
                "B0DHLFBLB4",
                "B0BGJ5XZTQ",
                "B0C2ZSX1RL",
                "B0DSFZP271",
                "B0DYSWTXH4",
                "B0DR8Q5186",
                "B0DSDL34G4",
                "B0DMSVLHJ1",

        ],

        ground_truth_answer=(
            "Recommend golf polo shirts that are designed for "
            "performance, comfort, and outdoor activities. "
            "Suitable products should emphasize breathable or "
            "moisture-wicking fabrics, lightweight construction, "
            "and good customer satisfaction through high ratings "
            "and positive reviews."
            ),        
    ),

        

    BenchmarkQuery(
        query_id="recommend_performance",
        category=QueryCategory.RECOMMENDATION,
        query="Recommend a performance polo shirt.",
        relevant_asins = [
            "B0DK5FZ325",
            "B0BGSDG377",
            "B0CXDL2NP6",
            "B0DPQC1NSV",
            "B0DWXNDJPK",
            "B0DWFMDQBT",
            "B0CQTCDJJ7",
            "B0DN375DNC",
            "B0D38YFY3K",
            "B07TF5NCTY",
            "B0DR7WSCFQ",
            "B0DPWXCXBX",
            "B0CQY7PMMK",
            "B0D391J394",
            "B0BGJ5XZTQ",
            "B0DSFZP271",
        ],

        ground_truth_answer=(
            "Recommend polo shirts intended for athletic or "
            "performance use. Suitable recommendations should "
            "highlight moisture-wicking materials, breathability, "
            "lightweight comfort, and functionality during sports "
            "or outdoor activities. Products should preferably "
            "have strong customer ratings and review counts."
        ),

    ),

    BenchmarkQuery(
        query_id="recommend_coofandy",
        category=QueryCategory.BRAND,
        query="Recommend a COOFANDY polo shirt.",
        relevant_asins = [
            "B0DLGB4RYH",
            "B0DJ6QSC4R",
            "B0BV257YG8",
            "B0CJTZLCQ2",
            "B0CW39BXTQ",
            "B0CQLQLWXL",
            "B08BC5YNP3",
            "B0DJQWS3VY",
            "B0CNGR3PSB",
            "B0D59TM92S",
            "B085NF55WL",
            "B08PF4YNVQ",
            "B083W4JW26",
            "B0DMSVLHJ1",
        ],

        ground_truth_answer=(
            "Recommend polo shirts manufactured by COOFANDY. "
            "The answer should recommend only COOFANDY products "
            "that match the user's request and may highlight "
            "features such as comfort, style, fit, material, "
            "or customer ratings where supported by the "
            "retrieved product information."
        ),
    ),

    BenchmarkQuery(
        query_id="recommend_zity",
        category=QueryCategory.BRAND,
        query="Recommend a ZITY polo shirt.",
        relevant_asins = [
            "B0DRXF62JH",
            "B09MHPSWY2",
            "B0DWFMDQBT",
            "B08SM3CDLN",
            "B09TK9248H",
            "B0BB2JC2QX",
            "B09MHS6C6Z",
            "B0DRXCWRYM",
            "B0BGJ5XZTQ",
            "B0DR8Q5186",
        ],

        ground_truth_answer=(
            "Recommend polo shirts manufactured by ZITY. "
            "The answer should recommend only ZITY products "
            "and may summarize important product features, "
            "materials, customer ratings, or performance "
            "characteristics supported by the retrieved context."
        ),
    ),

    # ==========================================================
    # Metadata Retrieval Benchmarks
    # ==========================================================

    BenchmarkQuery(
        query_id="under_20",
        category=QueryCategory.PRICE,
        query="Show products under $20.",
        expected_filter=ExpectedFilter(
            max_price=20.0,
        ),

        ground_truth_answer=(
            "Return only products priced below $20. "
            "Do not include products priced above the requested limit. "
            "If multiple qualifying products exist, present them clearly "
            "with their prices."
        )
    ),

    BenchmarkQuery(
        query_id="under_30",
        category=QueryCategory.PRICE,
        query="Show products under $30.",
        expected_filter=ExpectedFilter(
            max_price=30.0,
        ),

        ground_truth_answer=(
            "Return only products priced below $30. "
            "Every recommended product must satisfy the requested "
            "price constraint and should include its price."
        )
    ),

    BenchmarkQuery(
        query_id="rating_above_45",
        category=QueryCategory.RATING,
        query="Show products rated above 4.5 stars.",
        expected_filter=ExpectedFilter(
            min_rating=4.5,
        ),

        ground_truth_answer=(
            "Return only products with customer ratings of at least "
            "4.5 stars. The response should not recommend products "
            "below the requested rating threshold."
        )
    ),
]