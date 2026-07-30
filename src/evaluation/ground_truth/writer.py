"""
Writes ground truth reports to disk.
"""

from __future__ import annotations

from pathlib import Path


class GroundTruthWriter:
    """Writes human-readable candidate reports."""

    REPORT_DIR = Path("outputs/ground_truth/reports")

    def __init__(self) -> None:
        self.REPORT_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

    def write_report(
        self,
        file_name: str,
        report: str,
    ) -> None:

        path = self.REPORT_DIR / f"{file_name}.md"

        path.write_text(
            report,
            encoding="utf-8",
        )