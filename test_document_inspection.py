
from services.document_service.app.services.document_inspection_service import (
    inspect_document
)

document_path = (
    "storage/documents/"
    "SUB-01FC161884DD/"
    "DOC-790A628DEFDE.jpg"
)

result = inspect_document(document_path)

print("\nDOCUMENT INSPECTION RESULT")
print("--------------------------")

for key, value in result.items():
    print(f"{key}: {value}")
