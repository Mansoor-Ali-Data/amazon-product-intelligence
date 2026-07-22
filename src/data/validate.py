"""
Validation script for the processed data loader.
"""

from __future__ import annotations

from .data_loader import load_processed_data


def main() -> None:
    products_df, reviews_df = load_processed_data()

    print("✅ Processed datasets loaded successfully!")
    print(f"Products: {products_df.shape}")
    print(f"Reviews : {reviews_df.shape}")


if __name__ == "__main__":
    main()