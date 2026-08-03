"""
Monitoring dashboard data loader.

Responsibilities
----------------
- Read persisted telemetry records.
- Convert telemetry into a pandas DataFrame.
- Provide telemetry data for dashboard visualizations.

This module contains no visualization logic.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from config.logging import get_logger
from src.monitoring.paths import TELEMETRY_FILE

logger = get_logger(__name__)


class TelemetryLoader:
    """
    Loads monitoring telemetry for dashboard visualization.
    """

    def load(
        self,
    ) -> pd.DataFrame:
        """
        Load telemetry records into a pandas DataFrame.

        Returns
        -------
        pd.DataFrame
            DataFrame containing telemetry records.
            Returns an empty DataFrame if no telemetry exists.
        """

        logger.info(
            "Loading monitoring telemetry."
        )

        if not TELEMETRY_FILE.exists():

            logger.info(
                "No telemetry file found."
            )

            return pd.DataFrame()

        records: list[dict] = []

        with TELEMETRY_FILE.open(
            "r",
            encoding="utf-8",
        ) as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                records.append(
                    json.loads(line)
                )

        dataframe = pd.DataFrame(records)

        logger.info(
            "Loaded %d telemetry records.",
            len(dataframe),
        )

        return dataframe