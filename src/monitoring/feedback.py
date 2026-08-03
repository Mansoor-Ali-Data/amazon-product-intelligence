"""
Feedback collector.

Responsibilities
----------------
- Build feedback records from user input.
- Remain independent of storage and UI.

This module performs no file I/O.
"""

from __future__ import annotations

from datetime import UTC, datetime

from src.monitoring.models import FeedbackRecord


class FeedbackCollector:
    """
    Builds user feedback records.
    """

    def collect(
        self,
        query: str,
        helpful: bool,
        comment: str | None = None,
    ) -> FeedbackRecord:
        """
        Build a feedback record.

        Args:
            query:
                User query associated with the feedback.

            helpful:
                Whether the generated answer was helpful.

            comment:
                Optional user comment.

        Returns:
            FeedbackRecord.
        """

        return FeedbackRecord(
            timestamp=datetime.now(UTC).isoformat(),
            query=query,
            helpful=helpful,
            comment=comment,
        )