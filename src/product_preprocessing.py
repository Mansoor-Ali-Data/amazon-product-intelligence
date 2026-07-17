"""
Product dataset preprocessing.

Responsibilities
----------------
- Remove unnecessary columns.
- Rename product variant columns.
- Repair malformed variant data.
- Normalize variant formatting.
- Normalize text whitespace.

This module does NOT:
- Read or write CSV files.
- Load configuration.
- Validate data.
- Build RAG documents.
"""

from __future__ import annotations

import re

import pandas as pd

from config.logging import get_logger

logger = get_logger(__name__)

# ============================================================================
# Configuration
# ============================================================================

PRODUCT_COLUMNS_TO_DROP = [
    "s.no",
    "default_variant/2",
    "all_images",
    "scrape_time",
    "fastest_delivery_date",
    "model_number",
    "brand_page_url",
    "seller_page_url",
    "product_url",
    "product_description",
]


# ============================================================================
# Helper Functions
# ============================================================================

def clean_variant(value: str | None) -> str | None:
    """
    Remove formatting prefixes from variant values.

    Examples
    --------
    Size: Large -> Large
    Color : Black -> Black
    """
    if pd.isna(value):
        return None

    value = str(value).strip()

    value = re.sub(
        r"^(size|color)\s*:\s*",
        "",
        value,
        flags=re.IGNORECASE,
    )

    return value.strip()


def normalize_whitespace(text: str | None) -> str | None:
    """
    Collapse multiple whitespace characters into a single space.
    """
    if pd.isna(text):
        return None

    return re.sub(r"\s+", " ", str(text)).strip()


# ============================================================================
# Product Preprocessing
# ============================================================================

def preprocess_products(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize the products dataset.
    """
    logger.info("Preprocessing products dataset...")

    # ------------------------------------------------------------------
    # Work on a copy to avoid modifying the original dataframe.
    # ------------------------------------------------------------------
    df = df.copy()

    # ------------------------------------------------------------------
    # Repair malformed variant row before dropping default_variant/2.
    # One record stores the color value in default_variant/2.
    # ------------------------------------------------------------------
    if {
        "default_variant/1",
        "default_variant/2",
    }.issubset(df.columns):

        missing_color = (
            df["default_variant/1"].isna()
            & df["default_variant/2"].notna()
        )

        df.loc[
            missing_color,
            "default_variant/1",
        ] = df.loc[
            missing_color,
            "default_variant/2",
        ]

    # ------------------------------------------------------------------
    # Remove unnecessary columns.
    # ------------------------------------------------------------------
    df.drop(
        columns=PRODUCT_COLUMNS_TO_DROP,
        inplace=True,
        errors="ignore",
    )

    # ------------------------------------------------------------------
    # Rename variant columns.
    # ------------------------------------------------------------------
    df.rename(
        columns={
            "default_variant/0": "size",
            "default_variant/1": "color",
        },
        inplace=True,
    )

    # ------------------------------------------------------------------
    # Normalize variant formatting.
    # ------------------------------------------------------------------
    for column in ("size", "color"):

        if column in df.columns:
            df[column] = df[column].apply(clean_variant)

    # ------------------------------------------------------------------
    # Normalize whitespace in textual fields.
    # ------------------------------------------------------------------
    text_columns = [
        "title",
        "about_item",
        "breadcrumbs",
        "brand_name",
        "manufacturer",
        "seller_name",
    ]

    for column in text_columns:

        if column in df.columns:
            df[column] = df[column].apply(normalize_whitespace)

    logger.info("Products preprocessing completed.")

    return df