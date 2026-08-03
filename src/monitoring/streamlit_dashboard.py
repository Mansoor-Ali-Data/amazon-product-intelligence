"""
Interactive monitoring dashboard.

Responsibilities
----------------
- Load telemetry data.
- Display monitoring KPIs.
- Render monitoring charts.
- Display recent telemetry records.

This module contains Streamlit UI orchestration only.
"""

from __future__ import annotations

import streamlit as st

from src.monitoring.charts import MonitoringCharts
from src.monitoring.telemetry_loader import TelemetryLoader


class MonitoringDashboard:
    """
    Interactive monitoring dashboard.
    """

    def __init__(
        self,
    ) -> None:

        self._loader = TelemetryLoader()

        self._charts = MonitoringCharts()

    def run(
        self,
    ) -> None:
        """
        Run the monitoring dashboard.
        """

        dataframe = self._loader.load()

        self._render_header()

        if dataframe.empty:

            st.info(
                "No telemetry available yet."
            )

            return

        self._render_metrics(
            dataframe,
        )

        st.divider()

        self._render_charts(
            dataframe,
        )

        st.divider()

        self._render_table(
            dataframe,
        )

    # ---------------------------------------------------------
    # Header
    # ---------------------------------------------------------

    def _render_header(
        self,
    ) -> None:

        st.title(
            "📊 Amazon Product Intelligence Monitoring Dashboard"
        )

        st.caption(
            "Monitor system performance, token usage, latency, costs, and user activity."
        )

    # ---------------------------------------------------------
    # KPI Cards
    # ---------------------------------------------------------

    def _render_metrics(
        self,
        dataframe,
    ) -> None:

        average_feedback = (
            dataframe["feedback_rating"].dropna().mean()
            if "feedback_rating" in dataframe.columns
            else None
        )

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:

            st.metric(
                "Queries",
                len(dataframe),
            )

        with col2:

            st.metric(
                "Avg Latency",
                f"{dataframe['total_latency_seconds'].mean():.2f}s",
            )

        with col3:

            st.metric(
                "Avg Cost",
                f"${dataframe['estimated_cost'].mean():.6f}",
            )

        with col4:

            st.metric(
                "Avg Tokens",
                int(
                    dataframe["total_tokens"].mean()
                ),
            )

        with col5:

            st.metric(
                "Avg Feedback",
                (
                    f"{average_feedback:.1f} ⭐"
                    if average_feedback is not None
                    else "N/A"
                ),
            )

    # ---------------------------------------------------------
    # Charts
    # ---------------------------------------------------------

    def _render_charts(
        self,
        dataframe,
    ) -> None:

        st.subheader(
            "📈 Pipeline Latency"
        )

        st.plotly_chart(
            self._charts.latency_chart(
                dataframe,
            ),
            use_container_width=True,
        )

        st.subheader(
            "💰 Estimated Cost"
        )

        st.plotly_chart(
            self._charts.cost_chart(
                dataframe,
            ),
            use_container_width=True,
        )

        st.subheader(
            "🪙 Token Usage"
        )

        st.plotly_chart(
            self._charts.token_usage_chart(
                dataframe,
            ),
            use_container_width=True,
        )

        st.subheader(
            "📝 Prompt Strategy Usage"
        )

        st.plotly_chart(
            self._charts.prompt_strategy_chart(
                dataframe,
            ),
            use_container_width=True,
        )

        st.subheader(
            "🔍 Most Frequent Queries"
        )

        st.plotly_chart(
            self._charts.query_frequency_chart(
                dataframe,
            ),
            use_container_width=True,
        )

    # ---------------------------------------------------------
    # Telemetry Table
    # ---------------------------------------------------------

    def _render_table(
        self,
        dataframe,
    ) -> None:

        st.subheader(
            "📋 Recent Telemetry"
        )

        st.dataframe(
            dataframe.tail(20),
            use_container_width=True,
        )


def main() -> None:

    st.set_page_config(
        page_title="Monitoring Dashboard",
        page_icon="📊",
        layout="wide",
    )

    dashboard = MonitoringDashboard()

    dashboard.run()


if __name__ == "__main__":

    main()