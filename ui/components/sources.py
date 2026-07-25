"""
Source attribution component.

Responsible for displaying the retrieved products that
were used as context for answer generation.
"""

from __future__ import annotations

import streamlit as st

from src.retrieval.models import RetrievedChunk


def render_sources(
    chunks: list[RetrievedChunk],
) -> None:
    """
    Render retrieved product sources.

    Parameters
    ----------
    chunks:
        Retrieved chunks returned by the RAG pipeline.
    """

    if not chunks:
        return

    st.divider()

    st.subheader("📚 Sources Used")

    for index, chunk in enumerate(chunks, start=1):

        title = chunk.metadata.get(
            "title",
            "Unknown Product",
        )

        with st.expander(
            f"{index}. {title}",
            expanded=False,
        ):

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Price",
                    (
                        f"${chunk.metadata['price_value']:.2f}"
                        if chunk.metadata.get("price_value") is not None
                        else "Not specified"
                    ),
                )

                st.metric(
                    "Rating",
                    (
                        f"{chunk.metadata['rating_stars']} / 5"
                        if chunk.metadata.get("rating_stars") is not None
                        else "Not specified"
                    ),
                )

            with col2:

                st.metric(
                    "Brand",
                    chunk.metadata.get(
                        "brand_name",
                        "Not specified",
                    ),
                )

                st.metric(
                    "Category",
                    chunk.metadata.get(
                        "breadcrumbs",
                        "Not specified",
                    ).split("›")[-1].strip(),
                )

            st.markdown("---")

            st.write(
                f"**ASIN:** {chunk.asin}"
            )

            st.write(
                f"**Chunk Index:** {chunk.chunk_index}"
            )