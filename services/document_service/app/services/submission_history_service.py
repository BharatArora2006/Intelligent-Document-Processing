
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).resolve().parents[4]
DOCUMENTS_PATH = PROJECT_ROOT / "storage" / "documents"

SUPPORTED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}


def get_submission_history():

    if not DOCUMENTS_PATH.exists():
        return []

    submissions = []

    for folder in DOCUMENTS_PATH.iterdir():

        if not folder.is_dir():
            continue

        documents = [
            file for file in folder.iterdir()
            if file.is_file()
            and file.suffix.lower() in SUPPORTED_EXTENSIONS
        ]

        if not documents:
            continue

        submissions.append({
            "submission_id": folder.name,
            "total_documents": len(documents),
            "document_names": [
                file.name for file in documents
            ],
            "created_at": datetime.fromtimestamp(
                folder.stat().st_ctime,
                tz=timezone.utc
            ).isoformat()
        })

    submissions.sort(
        key=lambda item: item["created_at"],
        reverse=True
    )

    return submissions
