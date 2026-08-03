"""
Monitoring writer.

Responsibilities
----------------
- Persist telemetry records.
- Persist user feedback records.
- Append records as JSON Lines (JSONL).

This module performs no metric collection,
validation, or dashboard visualization.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from config.logging import get_logger
from src.monitoring.models import (
    FeedbackRecord,
    TelemetryRecord,
)

from src.monitoring.paths import (
    FEEDBACK_FILE,
    TELEMETRY_FILE,
)

logger = get_logger(__name__)



class MonitoringWriter:
    """
    Writes monitoring records to disk.
    """

    def __init__(
        self,
        output_dir: str = "outputs/monitoring",
    ) -> None:
        """
        Initialize monitoring writer.

        Args:
            output_dir:
                Directory used to store monitoring logs.
        """

        self._telemetry_file = TELEMETRY_FILE
        self._feedback_file = FEEDBACK_FILE

    def write_telemetry(
        self,
        record: TelemetryRecord,
    ) -> None:
        """
        Append one telemetry record.

        Args:
            record:
                Pipeline telemetry.
        """

        self._append(
            self._telemetry_file,
            record,
        )

        logger.info(
            "Telemetry written successfully."
        )

    def write_feedback(
        self,
        record: FeedbackRecord,
    ) -> None:
        """
        Append one feedback record.

        Args:
            record:
                User feedback.
        """
        logger.info("Writing feedback...")

        self._append(
            self._feedback_file,
            record,
        )

        logger.info(
            "Feedback written successfully."
        )

    @staticmethod
    def _append(
        path: Path,
        record: TelemetryRecord | FeedbackRecord,
    ) -> None:
        """
        Append a monitoring record as one JSON line.
        """

        with path.open(
            "a",
            encoding="utf-8",
        ) as file:

            json.dump(
                asdict(record),
                file,
                ensure_ascii=False,
            )

            file.write("\n")
            print(path)