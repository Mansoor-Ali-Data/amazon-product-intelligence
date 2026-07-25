"""
Templates used by the Context Builder.

This module defines the canonical text template for constructing
LLM-ready context from retrieved document chunks.

The template specifies only the presentation layout.
It contains no retrieval logic, formatting logic, or business rules.
"""


CONTEXT_TEMPLATE = """
Retrieved Context {index}
================================================================================

Title          : {title}
ASIN           : {asin}
Brand          : {brand}
Category       : {category}
Price          : {price}
List Price     : {list_price}
Rating         : {rating}
Rating Count   : {rating_count}
Availability   : {availability}
Seller         : {seller}
Manufacturer   : {manufacturer}
Recent Purchase: {recent_purchases}
Size           : {size}
Color          : {color}

--------------------------------------------------------------------------------
Retrieved Product Description

{text}
""".strip()