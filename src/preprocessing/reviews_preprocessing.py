"""
Reviews dataset preprocessing.

Responsibilities
----------------
- Remove unnecessary columns.
- Extract structured product variant information.
- Normalize review text formatting.

"""

from __future__ import annotations
import re
import pandas as pd
from config.logging import get_logger

logger = get_logger(__name__)

# ============================================================================
# Configuration
# ============================================================================

REVIEW_COLUMNS_TO_DROP = [
    "s.no",
    "cleaned_review_text",
    "reviewURL",
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
# Variant Parsing
# ============================================================================

def parse_product_variant(
    value: str | None,
) -> tuple[str | None, str | None]:
    """
    Extract review size and color from the productVariant field.

    The Amazon dataset stores multiple attributes as concatenated
    key-value pairs without consistent delimiters.

    Example
    -------
    Color: BlackSize: X-LargeHeight: 5'8"Weight: 180-190 lb

    Returns
    -------
    (review_size, review_color)
    """
    if pd.isna(value):
        return None, None

    value = str(value)

    labels = list(
        re.finditer(
            r"(Color|Size|Height|Weight)\s*:",
            value,
            flags=re.IGNORECASE,
        )
    )

    attributes = {}

    for i, match in enumerate(labels):

        key = match.group(1).lower()

        value_start = match.end()

        if i + 1 < len(labels):
            value_end = labels[i + 1].start()
        else:
            value_end = len(value)

        attributes[key] = value[value_start:value_end].strip()

    return (
        clean_variant(attributes.get("size")),
        clean_variant(attributes.get("color")),
    )


# ============================================================================
# Reviews Preprocessing
# ============================================================================

def preprocess_reviews(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize the reviews dataset.
    """
    logger.info("Preprocessing reviews dataset...")

    # ------------------------------------------------------------------
    # Work on a copy to avoid modifying the original dataframe.
    # ------------------------------------------------------------------
    df = df.copy()

    # ------------------------------------------------------------------
    # Remove fixed unnecessary columns.
    # ------------------------------------------------------------------
    df.drop(
        columns=REVIEW_COLUMNS_TO_DROP,
        inplace=True,
        errors="ignore",
    )
    # ---------------------------------------------------------------------
    # Standardize column names
    # ---------------------------------------------------------------------

    df = df.rename(
    columns={
        "productASIN": "asin",
    }
    )

    # ------------------------------------------------------------------
    # Remove media columns.
    # ------------------------------------------------------------------
    media_columns = [
        column
        for column in df.columns
        if column.startswith("images/")
        or column.startswith("videos/")
    ]

    df.drop(
        columns=media_columns,
        inplace=True,
        errors="ignore",
    )

    # ------------------------------------------------------------------
    # Extract structured variant information.
    # ------------------------------------------------------------------
    if "productVariant" in df.columns:

        df[["review_size", "review_color"]] = (
            df["productVariant"]
            .apply(parse_product_variant)
            .apply(pd.Series)
        )

    # ------------------------------------------------------------------
    # Normalize review text.
    # ------------------------------------------------------------------
    text_columns = [
        "reviewTitle",
        "reviewText",
    ]

    for column in text_columns:

        if column in df.columns:
            df[column] = df[column].apply(normalize_whitespace)

    logger.info("Reviews preprocessing completed.")

    return df