
import json

from services.document_service.app.services.submission_processing_service import (
    process_submission
)

# Use an existing submission folder from storage/documents
submission_id = "SUB-01FC161884DD"

result = process_submission(submission_id)

print("\nSUBMISSION PROCESSING RESULT")
print("=" * 50)
print(json.dumps(result, indent=4, ensure_ascii=False))
