"""
Monitoring dashboard visualizations.

Responsibilities
----------------
- Create interactive Plotly charts from telemetry data.
- Return Plotly figures for Streamlit rendering.

This module contains visualization logic only.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class MonitoringCharts:
    """
    Creates interactive monitoring charts.
    """

    def _prepare_dataframe(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Prepare telemetry for visualization.
        """

        dataframe = dataframe.copy()

        if dataframe.empty:
            return dataframe

        if "timestamp" in dataframe.columns:
            dataframe = dataframe.sort_values(
                by="timestamp",
            )

        dataframe["query_label"] = dataframe["query"].apply(
            lambda query: (
                query
                if len(query) <= 30
                else f"{query[:27]}..."
            )
        )

        return dataframe

    def _apply_layout(
        self,
        figure: go.Figure,
        title: str,
    ) -> go.Figure:
        """
        Apply a consistent dashboard style.
        """

        figure.update_layout(
            title=title,
            template="plotly_white",
            hovermode="x unified",
            margin=dict(
                l=40,
                r=40,
                t=60,
                b=80,
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
            ),
        )

        return figure

    def _empty_chart(
        self,
        title: str,
    ) -> go.Figure:
        """
        Create an empty placeholder figure.
        """

        figure = go.Figure()

        figure.add_annotation(
            text="No telemetry available.",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=18),
        )

        return self._apply_layout(
            figure,
            title,
        )

    # ---------------------------------------------------------
    # Pipeline Latency
    # ---------------------------------------------------------

    def latency_chart(
        self,
        dataframe: pd.DataFrame,
    ) -> go.Figure:

        if dataframe.empty:
            return self._empty_chart(
                "Pipeline Latency",
            )

        dataframe = self._prepare_dataframe(
            dataframe,
        )

        figure = px.bar(
            dataframe,
            x="query_label",
            y="total_latency_seconds",
            hover_data={
                "prompt_tokens": True,
                "completion_tokens": True,
                "estimated_cost": ":.6f",
                "prompt_strategy": True,
            },
            labels={
                "query_label": "Query",
                "total_latency_seconds": "Latency (seconds)",
            },
        )

        return self._apply_layout(
            figure,
            "Pipeline Latency per Query",
        )

    # ---------------------------------------------------------
    # Estimated Cost
    # ---------------------------------------------------------

    def cost_chart(
        self,
        dataframe: pd.DataFrame,
    ) -> go.Figure:

        if dataframe.empty:
            return self._empty_chart(
                "Estimated Cost",
            )

        dataframe = self._prepare_dataframe(
            dataframe,
        )

        figure = px.bar(
            dataframe,
            x="query_label",
            y="estimated_cost",
            hover_data={
                "total_tokens": True,
                "prompt_strategy": True,
            },
            labels={
                "query_label": "Query",
                "estimated_cost": "Cost (USD)",
            },
        )

        return self._apply_layout(
            figure,
            "Estimated Cost per Query",
        )

    # ---------------------------------------------------------
    # Token Usage
    # ---------------------------------------------------------

    def token_usage_chart(
        self,
        dataframe: pd.DataFrame,
    ) -> go.Figure:

        if dataframe.empty:
            return self._empty_chart(
                "Token Usage",
            )

        dataframe = self._prepare_dataframe(
            dataframe,
        )

        figure = go.Figure()

        figure.add_bar(
            name="Prompt Tokens",
            x=dataframe["query_label"],
            y=dataframe["prompt_tokens"],
        )

        figure.add_bar(
            name="Completion Tokens",
            x=dataframe["query_label"],
            y=dataframe["completion_tokens"],
        )

        figure.update_layout(
            barmode="stack",
            xaxis_title="Query",
            yaxis_title="Tokens",
        )

        return self._apply_layout(
            figure,
            "Token Usage per Query",
        )

    # ---------------------------------------------------------
    # Prompt Strategy Usage
    # ---------------------------------------------------------

    def prompt_strategy_chart(
        self,
        dataframe: pd.DataFrame,
    ) -> go.Figure:

        if dataframe.empty:
            return self._empty_chart(
                "Prompt Strategy Usage",
            )

        counts = (
            dataframe["prompt_strategy"]
            .value_counts()
            .rename_axis("prompt_strategy")
            .reset_index(name="count")
        )

        figure = px.bar(
            counts,
            x="prompt_strategy",
            y="count",
            text="count",
            labels={
                "prompt_strategy": "Prompt Strategy",
                "count": "Queries",
            },
        )

        return self._apply_layout(
            figure,
            "Prompt Strategy Usage",
        )

    # ---------------------------------------------------------
    # Most Frequent Queries
    # ---------------------------------------------------------

    def query_frequency_chart(
        self,
        dataframe: pd.DataFrame,
        top_n: int = 10,
    ) -> go.Figure:

        if dataframe.empty:
            return self._empty_chart(
                "Most Frequent Queries",
            )

        counts = (
            dataframe["query"]
            .value_counts()
            .head(top_n)
            .sort_values()
            .rename_axis("query")
            .reset_index(name="count")
        )

        figure = px.bar(
            counts,
            x="count",
            y="query",
            orientation="h",
            text="count",
            labels={
                "count": "Frequency",
                "query": "Query",
            },
        )

        return self._apply_layout(
            figure,
            f"Top {top_n} Most Frequent Queries",
        )