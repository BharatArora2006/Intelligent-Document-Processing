
from pathlib import Path

from services.document_service.app.services.document_preprocessing_service import (
    preprocess_document
)
from services.document_service.app.services.document_processing_service import (
    process_document
)
from services.document_service.app.services.submission_result_service import (save_submission_result
)

PROJECT_ROOT = Path(__file__).resolve().parents[4]
DOCUMENTS_PATH = PROJECT_ROOT / "storage" / "documents"


def process_submission(submission_id: str):

    submission_folder = DOCUMENTS_PATH / submission_id

    if not submission_folder.exists():
        raise FileNotFoundError(
            f"Submission not found: {submission_id}"
        )

    supported_extensions = {".pdf", ".jpg", ".jpeg", ".png"}

    document_results = []

    uploaded_documents = [
        file_path
        for file_path in submission_folder.iterdir()
        if file_path.is_file()
        and file_path.suffix.lower() in supported_extensions
    ]

    if not uploaded_documents:
        raise ValueError("No supported documents found in submission.")

    # Process each uploaded document independently
    for document_path in uploaded_documents:

        # Step 1: Preprocess document
        preprocessing_result = preprocess_document(
            str(document_path)
        )

        # Step 2: Collect all processed page images
        image_paths = [
            page["processed_image"]
            for page in preprocessing_result["pages"]
        ]

        # Step 3: Run OCR, classification and extraction
        processing_result = process_document(image_paths)

        document_results.append({
            "document_id": document_path.stem,
            "original_filename": document_path.name,
            "total_pages": preprocessing_result["total_pages"],
            "preprocessing": preprocessing_result,
            "processing": processing_result
        })

    result = {
        "submission_id": submission_id,
        "submission_status": "SUCCESS",
        "total_documents": len(document_results),
        "documents": document_results
    }

    # Save complete processing result
    saved_result_path = save_submission_result(
        submission_id,
        result
    )

    result["result_file"] = saved_result_path

    return result
