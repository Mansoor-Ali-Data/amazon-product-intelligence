"""
Run the data preprocessing pipeline.

Responsibilities:
- Load preprocessing configuration.
- Read raw datasets.
- Execute preprocessing.
- Save processed datasets.
"""

from pathlib import Path

import pandas as pd
import yaml

from config.logging import get_logger
from src.preprocessing.products_preprocessing import preprocess_products
from src.preprocessing.reviews_preprocessing import preprocess_reviews

logger = get_logger(__name__)


def load_config(config_path: str) -> dict:
    """
    Load preprocessing configuration.
    """
    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def main() -> None:
    """
    Execute the preprocessing pipeline.
    """
    logger.info("Starting preprocessing pipeline...")

    # -------------------------------------------------------------
    # Load configuration
    # -------------------------------------------------------------
    config = load_config("config/preprocessing_config.yml")

    products_config = config["datasets"]["products"]
    reviews_config = config["datasets"]["reviews"]

    # -------------------------------------------------------------
    # Load raw datasets
    # -------------------------------------------------------------
    logger.info("Loading raw datasets...")

    products_df = pd.read_csv(products_config["input"])
    reviews_df = pd.read_csv(reviews_config["input"])

    logger.info(f"Products loaded: {len(products_df):,} rows")
    logger.info(f"Reviews loaded: {len(reviews_df):,} rows")

    # -------------------------------------------------------------
    # Preprocess datasets
    # -------------------------------------------------------------
    processed_products = preprocess_products(products_df)
    processed_reviews = preprocess_reviews(reviews_df)

    # -------------------------------------------------------------
    # Ensure output directories exist
    # -------------------------------------------------------------
    Path(products_config["output"]).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    Path(reviews_config["output"]).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # -------------------------------------------------------------
    # Save processed datasets
    # -------------------------------------------------------------
    logger.info("Saving processed datasets...")

    processed_products.to_csv(
        products_config["output"],
        index=False,
    )

    processed_reviews.to_csv(
        reviews_config["output"],
        index=False,
    )

    logger.info("Preprocessing pipeline completed successfully.")


if __name__ == "__main__":
    main()