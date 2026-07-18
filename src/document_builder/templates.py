"""
Document templates used by the Document Builder.

This module contains the canonical text template for constructing
knowledge documents from the processed Amazon product dataset.

The template defines only the document layout.
It contains no formatting or business logic.
"""

DOCUMENT_TEMPLATE = """
================================================================================
PRODUCT INFORMATION
================================================================================

Title: {title}

Brand: {brand_name}

Seller: {seller_name}

Category: {breadcrumbs}

Price: {price_value}

List Price: {list_price}

Rating: {rating_stars} / 5

Rating Count: {rating_count}

Best Seller Rank: {best_sellers_rank}

Recent Purchases: {recent_purchases}

Size: {size}

Color: {color}

Manufacturer: {manufacturer}


================================================================================
ABOUT THIS ITEM
================================================================================

{about_item}

================================================================================
CUSTOMER REVIEWS
================================================================================

{reviews}
""".strip()


REVIEW_TEMPLATE = """
Review #{review_number}

ID: {reviewID}

Title: {reviewTitle}

Rating: {rating}/5

Verified Purchase: {verifiedPurchase}

Purchased Size: {review_size}

Purchased Color: {review_color}

Review:

{reviewText}
""".strip()