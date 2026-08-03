"""
Sidebar component for the Streamlit application.

Responsible for rendering navigation, project information,
example questions, and application controls.
"""

from __future__ import annotations

import streamlit as st
from src.monitoring.feedback import FeedbackCollector
from src.monitoring.writer import MonitoringWriter


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

        st.subheader("🛠️ Controls")

        if st.button(
            "🗑 Clear Conversation",
            use_container_width=True,
        ):
            st.session_state.pop("messages", None)
            st.rerun()

        st.divider()

        st.caption("Version 1.0")

        st.divider()

        st.subheader("💬 Feedback")

        if "last_query" in st.session_state:

            rating = st.radio(
                "Was the last answer helpful?",
                [
                    "👍 Helpful",
                    "👎 Not Helpful",
                ],
                horizontal=True,
            )

            comment = st.text_area(
                "Comments (optional)",
                placeholder="Tell us what could be improved...",
            )

            if st.button(
                "Submit Feedback",
                use_container_width=True,
            ):

                collector = FeedbackCollector()

                record = collector.collect(
                    query=st.session_state.last_query,
                    helpful=rating.startswith("👍"),
                    comment=comment,
                )

                writer = MonitoringWriter()

                writer.write_feedback(record)

                st.toast("✅ Feedback submitted!")
        else:

            st.caption(
                "Ask a question to enable feedback."
            )