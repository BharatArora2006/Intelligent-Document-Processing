import json

from services.document_service.app.services.submission_history_service import (
    get_submission_history
)

result = get_submission_history()

print(json.dumps(result, indent=4))