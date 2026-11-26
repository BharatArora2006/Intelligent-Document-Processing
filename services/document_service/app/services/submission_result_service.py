
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]

RESULTS_PATH = PROJECT_ROOT / "storage" / "processing_results"


def validate_submission_id(submission_id: str):
    """Validate submission ID before using it in a file path."""
    if not re.fullmatch(r"SUB-[A-Za-z0-9-]+", submission_id):
        raise ValueError("Invalid submission ID.")


def save_submission_result(submission_id: str, result: dict):
    """Save the complete processing result as a JSON file."""

    validate_submission_id(submission_id)

    RESULTS_PATH.mkdir(parents=True, exist_ok=True)

    output_file = RESULTS_PATH / f"{submission_id}_result.json"
    temporary_file = RESULTS_PATH / f"{submission_id}_result.tmp"

    with open(temporary_file, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    temporary_file.replace(output_file)

    return str(output_file)


def get_submission_result(submission_id: str):
    """Retrieve a previously saved processing result."""

    validate_submission_id(submission_id)

    result_file = RESULTS_PATH / f"{submission_id}_result.json"

    if not result_file.exists():
        raise FileNotFoundError(
            f"Processing result not found for submission: {submission_id}"
        )

    with open(result_file, "r", encoding="utf-8") as file:
        return json.load(file)
