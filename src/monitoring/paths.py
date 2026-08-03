"""
Shared monitoring paths.
"""

from pathlib import Path

OUTPUT_DIR = Path("outputs/monitoring")

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

TELEMETRY_FILE = OUTPUT_DIR / "telemetry.jsonl"

FEEDBACK_FILE = OUTPUT_DIR / "feedback.jsonl"