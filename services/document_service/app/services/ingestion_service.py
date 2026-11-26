
import hashlib
import uuid

from pathlib import Path

STORAGE_PATH = (
    Path(__file__).resolve().parents[4]
    / "storage"
    / "documents"
)

ALLOWED_EXTENSIONS = {
    ".pdf": "application/pdf",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_FILES = 10


def validate_file_signature(extension: str, content: bytes):

    signatures = {
        ".pdf": content.startswith(b"%PDF-"),
        ".jpg": content.startswith(b"\xff\xd8\xff"),
        ".jpeg": content.startswith(b"\xff\xd8\xff"),
        ".png": content.startswith(
            b"\x89PNG\r\n\x1a\n"
        ),
    }

    return signatures.get(extension, False)


async def ingest_documents(
    employee_id: str,
    dependent_name: str,
    relationship: str,
    files
):

    if not files:
        raise ValueError("Please upload at least one document.")

    if len(files) > MAX_FILES:
        raise ValueError("Maximum 10 files allowed per submission.")

    submission_id = f"SUB-{uuid.uuid4().hex[:12].upper()}"

    submission_folder = STORAGE_PATH / submission_id
    submission_folder.mkdir(parents=True, exist_ok=True)

    uploaded_documents = []
    seen_hashes = set()

    try:

        for file in files:

            original_filename = file.filename or ""

            extension = Path(original_filename).suffix.lower()

            if extension not in ALLOWED_EXTENSIONS:
                raise ValueError(
                    f"Unsupported file type: {original_filename}"
                )

            content = await file.read(MAX_FILE_SIZE + 1)

            if not content:
                raise ValueError(
                    f"Empty file: {original_filename}"
                )

            if len(content) > MAX_FILE_SIZE:
                raise ValueError(
                    f"File exceeds 10 MB: {original_filename}"
                )

            if not validate_file_signature(extension, content):
                raise ValueError(
                    f"File content does not match its extension: "
                    f"{original_filename}"
                )

            file_hash = hashlib.sha256(content).hexdigest()

            if file_hash in seen_hashes:
                raise ValueError(
                    f"Duplicate file within submission: "
                    f"{original_filename}"
                )

            seen_hashes.add(file_hash)

            document_id = f"DOC-{uuid.uuid4().hex[:12].upper()}"

            stored_filename = (
                f"{document_id}{extension}"
            )

            storage_location = (
                submission_folder / stored_filename
            )

            storage_location.write_bytes(content)

            uploaded_documents.append({
                "document_id": document_id,
                "original_filename": original_filename,
                "stored_filename": stored_filename,
                "file_extension": extension,
                "mime_type": ALLOWED_EXTENSIONS[extension],
                "file_size_bytes": len(content),
                "sha256_hash": file_hash,
                "processing_status": "UPLOADED"
            })

        return {
            "submission_id": submission_id,
            "employee_id": employee_id,
            "dependent_name": dependent_name,
            "relationship": relationship,
            "total_documents": len(uploaded_documents),
            "documents": uploaded_documents
        }

    except Exception:
        # Remove partially uploaded files if any file fails.
        import shutil

        shutil.rmtree(submission_folder, ignore_errors=True)
        raise
