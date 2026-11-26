
import json

from services.document_service.app.services.document_classification_service import (
    classify_document
)


ocr_file = "storage/ocr_results/page_1_ocr.json"

with open(ocr_file, "r", encoding="utf-8") as file:
    ocr_pages = json.load(file)


result = classify_document(ocr_pages)

print("\nDOCUMENT CLASSIFICATION RESULT")
print("--------------------------------")

print(json.dumps(
    result,
    indent=4
))
