
import json

from services.document_service.app.services.document_processing_service import (
    process_document
)


image_path = [
     "storage/processed/DOC-790A628DEFDE/page_1.png"
]

result = process_document(image_path)

print("\nCOMPLETE DOCUMENT PROCESSING RESULT")
print("-----------------------------------")

print(json.dumps(
    result,
    indent=4,
    ensure_ascii=False
))
