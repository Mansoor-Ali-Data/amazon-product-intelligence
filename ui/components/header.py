"""
Header component for the Streamlit application.

Responsible for rendering the application title and a brief
description of the assistant. This component contains only
presentation logic.
"""

from __future__ import annotations

import streamlit as st


def render_header() -> str | None:
    """
    Render the application header.
    """

    st.title("🛍️ Amazon Fashion Product Intelligence Assistant")

    st.caption(
        "An AI-powered Retrieval-Augmented Generation (RAG) assistant "
        "built on an Amazon Fashion product dataset."
    )

    st.info(
        """
        **Dataset Scope**

        This assistant answers questions using Amazon Fashion product
        information and customer reviews.
        """
        )
        
        
    st.markdown("### 💡 Try one of these questions")
    example_questions = [
            "Recommend a men's polo shirt under $25",
            "Compare two golf polo shirts",
            "Which polo shirt has the highest customer rating?",
            "What materials are used in this product?",
            "Summarize customer opinions for this item",
        
    ]
    for question in example_questions:
        if st.button(question,use_container_width=True,):
            return question
        
    st.divider()

    return None