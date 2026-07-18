"""
Utilities for formatting Product and Review objects into
human-readable RAG documents.

This module is responsible only for converting dataclass
objects into formatted text using predefined templates.
It performs no data loading, preprocessing, or document
construction.
"""

from __future__ import annotations

from .models import Product, Review
from .templates import DOCUMENT_TEMPLATE, REVIEW_TEMPLATE


# Separator inserted between formatted reviews
REVIEW_SEPARATOR = "\n\n" + "-" * 80 + "\n\n"


def format_review(review: Review, review_number: int) -> str:
    """
    Format a single customer review.

    Args:
        review: Review dataclass.
        review_number: Sequential review number.

    Returns:
        Formatted review text.
    """
    return REVIEW_TEMPLATE.format(
        review_number=review_number,
        reviewTitle=review.reviewTitle,
        reviewID=review.reviewID,
        rating=review.rating,
        verifiedPurchase=(
            "Yes"
            if review.verifiedPurchase
            else "No"
        ),
        review_size=(
            review.review_size
            if review.review_size and str(review.review_size).lower() != "nan"
            else "Not specified"
        ),
        review_color=(
            review.review_color
                if review.review_color and str(review.review_color).lower() != "nan"
                else "Not specified"
        ),
        reviewText=review.reviewText,
    )


def format_reviews(reviews: list[Review]) -> str:
    """
    Format multiple reviews into a single text block.

    Args:
        reviews: List of Review dataclasses.

    Returns:
        Concatenated review section.
    """
    if not reviews:
        return "No customer reviews available."

    formatted_reviews = [
        format_review(review, index)
        for index, review in enumerate(reviews, start=1)
    ]

    return REVIEW_SEPARATOR.join(formatted_reviews)


def format_document(product: Product, reviews: list[Review]) -> str:
    """
    Format a complete product document.

    Args:
        product: Product dataclass.
        reviews: Reviews associated with the product.

    Returns:
        Complete formatted document.
    """
    return DOCUMENT_TEMPLATE.format(
        title=product.title,
        brand_name=product.brand_name,
        seller_name=product.seller_name,
        breadcrumbs=product.breadcrumbs,
        price_value=(
            f"${product.price_value:.2f}"
                if product.price_value is not None
                else "Not specified"
            ),
        list_price=product.list_price,
        rating_stars=product.rating_stars,
        rating_count=product.rating_count,
        best_sellers_rank=product.best_sellers_rank,
        recent_purchases=product.recent_purchases,
        size=product.size,
        color=product.color,
        manufacturer=product.manufacturer,
        about_item=product.about_item,
        reviews=format_reviews(reviews),
    )