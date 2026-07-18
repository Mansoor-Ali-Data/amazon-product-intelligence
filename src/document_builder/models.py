from dataclasses import dataclass
from typing import Any


@dataclass
class Product:
    """Represents a processed product."""

    asin: str
    title: str
    brand_name: str
    seller_name: str
    manufacturer: str
    breadcrumbs: str
    about_item: str

    price_value: float
    list_price: float

    rating_stars: float
    rating_count: int
    best_sellers_rank: str
    recent_purchases: str

    size: str
    color: str


@dataclass
class Review:
    """Represents a processed customer review."""

    asin: str
    reviewID: str
    reviewTitle: str
    reviewText: str
    rating: float
    verifiedPurchase: bool
    review_size: str
    review_color: str


@dataclass
class Document:
    """Represents a knowledge document for the RAG pipeline."""

    id: str
    text: str
    metadata: dict[str, Any]