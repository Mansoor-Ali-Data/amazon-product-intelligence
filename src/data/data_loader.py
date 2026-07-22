"""
Load processed datasets from disk.
"""

from __future__ import annotations

import pandas as pd

from config.loader import load_yaml
from config.logging import get_logger

logger = get_logger(__name__)


def load_processed_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load the processed product and review datasets.

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        Processed products and reviews dataframes.
    """

    logger.info("Starting processed dataset loading.")

    try:
        config = load_yaml("data.yml")

        data_config = config["data"]

        products_path = data_config["processed_products"]
        reviews_path = data_config["processed_reviews"]

        products_df = pd.read_csv(products_path)
        reviews_df = pd.read_csv(reviews_path)

        logger.info(
            "Loaded products dataset with %d rows.",
            len(products_df),
        )

        logger.info(
            "Loaded reviews dataset with %d rows.",
            len(reviews_df),
        )

        logger.info(
            "Processed datasets loaded successfully."
        )

        return products_df, reviews_df

    except Exception:
        logger.exception(
            "Failed to load processed datasets."
        )
        raise