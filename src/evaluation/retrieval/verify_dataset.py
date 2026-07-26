"""
Verify the retrieval evaluation benchmark.

This utility verifies that every expected ASIN in the retrieval
benchmark corresponds to the intended product in the processed dataset.

The script does NOT evaluate retrieval quality.
It is intended to maintain and audit the benchmark itself.
"""

from __future__ import annotations

from src.data.data_loader import load_processed_data
from src.evaluation.retrieval.dataset import EVALUATION_DATASET


def main() -> None:
    """
    Verify the retrieval benchmark dataset.
    """

    print("=" * 80)
    print("Retrieval Benchmark Verification")
    print("=" * 80)
    print()

    products_df, _ = load_processed_data()

    products_by_asin = (
        products_df
        .set_index("asin")
        .to_dict(orient="index")
    )

    total_queries = len(EVALUATION_DATASET)
    total_expected_asins = 0
    missing_asins = 0

    for example in EVALUATION_DATASET:

        print("=" * 80)
        print("Query")
        print("=" * 80)
        print()

        print(f"Query       : {example.query}")
        print(f"Category    : {example.category}")
        print(f"Description : {example.description}")
        print()

        for asin in example.expected_asins:

            total_expected_asins += 1

            product = products_by_asin.get(asin)

            print("-" * 80)

            if product is None:

                missing_asins += 1

                print(f"⚠ ASIN not found: {asin}")
                print()

                continue

            price = product.get("price_value")
            rating = product.get("rating_stars")

            print(f"ASIN        : {asin}")
            print(f"Brand       : {product.get('brand_name')}")
            print(f"Title       : {product.get('title')}")
            print(f"Price       : ${price:.2f}" if price == price else "Price       : N/A")
            print(f"Rating      : {rating}" if rating == rating else "Rating      : N/A")
            print(f"Category    : {product.get('breadcrumbs')}")
            print()

    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print()

    print(f"Queries             : {total_queries}")
    print(f"Expected ASINs      : {total_expected_asins}")
    print(f"Missing ASINs       : {missing_asins}")

    print()
    print("✅ Verification completed.")


if __name__ == "__main__":
    main()