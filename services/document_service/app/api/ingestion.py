
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.document_service.app.services.submission_processing_service import (process_submission
)
from services.document_service.app.services.ingestion_service import (ingest_documents)
from services.document_service.app.services.submission_history_service import (get_submission_history
)
from services.document_service.app.services.submission_result_service import (get_submission_result
)
router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Document Ingestion"]
)


@router.post("/upload")
async def upload_documents(
    employee_id: str = Form(...),
    dependent_name: str = Form(...),
    relationship: str = Form(...),
    files: list[UploadFile] = File(...)
):

    try:

        result = await ingest_documents(
            employee_id=employee_id,
            dependent_name=dependent_name,
            relationship=relationship,
            files=files
        )

        return {
            "success": True,
            "message": "Documents uploaded successfully.",
            "data": result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.post("/{submission_id}/process")
async def process_uploaded_submission(submission_id: str):
    try:
        result = process_submission(submission_id)

        return {
            "success": True,
            "message": "Submission processed successfully.",
            "data": result
        }

    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

@router.get("/history")
async def submission_history():

    try:
        result = get_submission_history()

        return {
            "success": True,
            "total_submissions": len(result),
            "data": result
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

@router.get("/{submission_id}/result")
async def get_processed_submission_result(submission_id: str):
    try:
        result = get_submission_result(submission_id)

        return {
            "success": True,
            "message": "Processing result retrieved successfully.",
            "data": result
        }

    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))