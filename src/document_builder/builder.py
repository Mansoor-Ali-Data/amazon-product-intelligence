"""
Build Document objects from processed product and review datasets.
"""

from __future__ import annotations

import pandas as pd

from config.logging import get_logger

from .formatter import format_document
from .models import Document, Product, Review

logger = get_logger(__name__)


def build_documents(
    products_df: pd.DataFrame,
    reviews_df: pd.DataFrame,
) -> list[Document]:
    """
    Build one Document for each product.

    Args:
        products_df:
            Processed products dataframe.

        reviews_df:
            Processed reviews dataframe.

    Returns:
        List of Document objects.
    """
    logger.info(
        "Starting document generation for %d products and %d reviews.",
        len(products_df),
        len(reviews_df),
    )

    try:
        documents: list[Document] = []

        reviews_by_asin = {
            asin: group
            for asin, group in reviews_df.groupby("asin")
        }

        logger.info(
            "Grouped reviews into %d product groups.",
            len(reviews_by_asin),
        )

        for _, product_row in products_df.iterrows():

            asin = product_row["asin"]

            logger.debug("Building document for ASIN '%s'.", asin)

            product = Product(
                asin=product_row["asin"],
                title=product_row["title"],
                brand_name=product_row["brand_name"],
                seller_name=product_row["seller_name"],
                manufacturer=product_row["manufacturer"],
                breadcrumbs=product_row["breadcrumbs"],
                about_item=product_row["about_item"],
                price_value=product_row["price_value"],
                list_price=product_row["list_price"],
                rating_stars=product_row["rating_stars"],
                rating_count=product_row["rating_count"],
                best_sellers_rank=product_row["best_sellers_rank"],
                recent_purchases=product_row["recent_purchases"],
                size=product_row["size"],
                color=product_row["color"],
            )

            review_objects: list[Review] = []

            if asin in reviews_by_asin:
                for _, review_row in reviews_by_asin[asin].iterrows():
                    review_objects.append(
                        Review(
                            asin=review_row["asin"],
                            reviewID=review_row["reviewID"],
                            reviewTitle=review_row["reviewTitle"],
                            reviewText=review_row["reviewText"],
                            rating=review_row["rating"],
                            verifiedPurchase=review_row["verifiedPurchase"],
                            review_size=review_row["review_size"],
                            review_color=review_row["review_color"],
                        )
                    )

            document = Document(
                id=asin,
                text=format_document(product, review_objects),
                metadata={
                    "asin": asin,
                    "brand_name": product.brand_name,
                    "breadcrumbs": product.breadcrumbs,
                    "price_value": product.price_value,
                    "rating_stars": product.rating_stars,
                },
            )

            documents.append(document)

        logger.info(
            "Successfully built %d documents.",
            len(documents),
        )

        return documents

    except Exception:
        logger.exception("Failed to build document collection.")
        raise