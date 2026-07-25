"""
Streamlit application for the Amazon Fashion Product Intelligence Assistant.
"""

from __future__ import annotations

import streamlit as st

from ui.components.answer import render_answer
from ui.components.chat import (
    get_user_query,
    initialize_chat,
    render_messages,
)
from ui.components.header import render_header
from ui.components.sidebar import render_sidebar
from ui.components.sources import render_sources

from src.pipeline.rag_pipeline import RAGPipeline


# ---------------------------------------------------------------------
# Streamlit Configuration
# ---------------------------------------------------------------------

st.set_page_config(
    page_title="Amazon Fashion Product Intelligence Assistant",
    page_icon="🛍️",
    layout="wide",
)


# ---------------------------------------------------------------------
# Resources
# ---------------------------------------------------------------------

@st.cache_resource
def load_pipeline() -> RAGPipeline:
    """
    Load the RAG pipeline once per Streamlit session.
    """
    return RAGPipeline()


pipeline = load_pipeline()


# ---------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------

render_header()

render_sidebar()

initialize_chat()

render_messages()


# ---------------------------------------------------------------------
# User Interaction
# ---------------------------------------------------------------------

query = get_user_query()

if query:

    # Display user message immediately
    st.session_state.messages.append(
        {
            "role": "user",
            "content": query,
        }
    )

    with st.chat_message("user"):
        st.markdown(query)

    # Generate assistant response
    with st.chat_message("assistant"):

        with st.status(
            "Running RAG Pipeline...",
            expanded=True,
        ) as status:

            response = pipeline.ask(
                query=query,
                progress_callback=status.write,
            )

            status.update(
                label="✅ Answer generated",
                state="complete",
                expanded=False,
            )

        render_answer(response.answer)

        render_sources(
            response.retrieved_chunks,
        )

    # Store assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.answer,
        }
    )

    # Store assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.answer,
        }
    )