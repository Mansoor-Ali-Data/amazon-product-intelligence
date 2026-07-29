"""
Writes ground truth reports to disk.
"""

from __future__ import annotations

from pathlib import Path


class GroundTruthWriter:

    REPORT_DIR = Path("outputs/ground_truth/reports")
    TEMPLATE_DIR = Path("outputs/ground_truth/templates")

    def __init__(self) -> None:

        self.REPORT_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.TEMPLATE_DIR.mkdir(
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

    def write_template(
        self,
        file_name: str,
        template: str,
    ) -> None:

        path = self.TEMPLATE_DIR / f"{file_name}.py"

        path.write_text(
            template,
            encoding="utf-8",
        )