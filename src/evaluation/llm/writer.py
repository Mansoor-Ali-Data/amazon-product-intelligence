"""
Writes retrieval evaluation reports to disk.
"""

from __future__ import annotations

from pathlib import Path


class EvaluationWriter:
    """
    Persists evaluation reports.
    """

    REPORT_DIR = Path("outputs/evaluation")

    def __init__(self) -> None:

        self.REPORT_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

    def write_report(
        self,
        report: str,
        file_name: str = "llm_evaluation_report",
    ) -> Path:
        """
        Write the evaluation report.

        Returns
        -------
        Path
            Path of the written report.
        """

        path = self.REPORT_DIR / f"{file_name}.md"

        path.write_text(
            report,
            encoding="utf-8",
        )

        return path