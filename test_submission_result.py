
from services.document_service.app.services.submission_result_service import (
    save_submission_result,
    get_submission_result
)

sample_result = {
    "submission_id": "SUB-TEST123",
    "submission_status": "SUCCESS",
    "total_documents": 1,
    "documents": [
        {
            "document_id": "DOC-TEST123",
            "document_type": "MARRIAGE_CERTIFICATE"
        }
    ]
}

# Save result
saved_path = save_submission_result(
    "SUB-TEST123",
    sample_result
)

print("Saved file:", saved_path)

# Retrieve result
retrieved_result = get_submission_result("SUB-TEST123")

print("\nRetrieved result:")
print(retrieved_result)

# Verify
assert retrieved_result == sample_result

print("\nTEST PASSED")
