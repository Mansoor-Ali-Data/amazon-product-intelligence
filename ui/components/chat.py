"""
Chat component for the Streamlit application.

Responsible for managing the chat interface, conversation
history, and user input.

This module contains no retrieval or LLM logic.
"""

from __future__ import annotations

import streamlit as st


def initialize_chat() -> None:
    """
    Initialize the conversation history.
    """

    if "messages" not in st.session_state:
        st.session_state.messages = []


def render_messages() -> None:
    """
    Render the conversation history.
    """

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def get_user_query() -> str | None:
    """
    Display the chat input box.

    Returns
    -------
    str | None
        User query if submitted, otherwise None.
    """

    return st.chat_input(
        "Ask a question about Amazon Fashion products..."
    )