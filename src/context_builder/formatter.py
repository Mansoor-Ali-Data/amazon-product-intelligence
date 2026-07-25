"""
Utilities for formatting retrieved chunks into LLM-ready context.

This module is responsible only for converting RetrievedChunk
objects into formatted context using predefined templates.

It performs no retrieval, ranking, filtering, or prompt
construction.
"""

from src.retrieval.models import RetrievedChunk
from .templates import CONTEXT_TEMPLATE

# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

def format_context(
    chunk: RetrievedChunk,
    index: int,
) -> str:

    return CONTEXT_TEMPLATE.format (
        index=index,
        title=chunk.metadata.get("title", "Not specified"),
        asin=chunk.metadata.get("asin", "Not specified"),
        brand=chunk.metadata.get("brand_name", "Not specified"),
        category=chunk.metadata.get("breadcrumbs", "Not specified"),
        price=(
            f"${price:.2f}" 
            if isinstance((price := chunk.metadata.get("price_value")), (int, float)) 
            else "Not specified"
        ),
        list_price=chunk.metadata.get("list_price", "Not specified"),
        rating=(
            f"{rating:.1f} / 5"
            if isinstance((rating := chunk.metadata.get("rating_stars")), (int, float))
            else "Not specified"
        ),
        rating_count=(
            f"{int(rating_count)} ratings"
            if isinstance((rating_count := chunk.metadata.get("rating_count")), (int, float))
            else "Not specified"
        ),
        availability=chunk.metadata.get("availability", "Not specified"),
        seller=chunk.metadata.get("seller_name", "Not specified"),
        manufacturer=chunk.metadata.get("manufacturer", "Not specified"),
        recent_purchases=chunk.metadata.get("recent_purchases", "Not specified"),
        size=chunk.metadata.get("size", "Not specified"),
        color=chunk.metadata.get("color", "Not specified"),
        text=chunk.text.strip(),
    )