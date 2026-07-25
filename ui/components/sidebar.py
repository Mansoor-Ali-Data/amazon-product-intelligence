"""
Sidebar component for the Streamlit application.

Responsible for rendering navigation, project information,
example questions, and application controls.
"""

from __future__ import annotations

import streamlit as st


def render_sidebar() -> None:
    """
    Render the application sidebar.
    """

    with st.sidebar:

        st.header("📚 About")

        st.markdown(
            """
            This assistant uses a **Retrieval-Augmented Generation (RAG)**
            pipeline to answer questions about products from an
            **Amazon Fashion** dataset.

            Answers are generated using retrieved product information
            and customer reviews instead of relying solely on the LLM's
            internal knowledge.
            """
        )

        st.divider()

        st.subheader("💡 Example Questions")

        st.markdown(
            """
            - Recommend a men's polo shirt under $25
            - Compare two golf polo shirts
            - Which polo shirt has the best rating?
            - Which shirts are moisture wicking?
            - Summarize customer reviews for this product
            """
        )

        st.divider()

        st.subheader("🛠️ Controls")

        if st.button(
            "🗑️ Clear Conversation",
            use_container_width=True,
        ):
            # st.session_state.messages = []
            st.rerun()

        st.divider()

        st.caption("Version 1.0")