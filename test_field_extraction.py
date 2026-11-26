
import json

from services.document_service.app.services.field_extraction_service import (
    extract_adoption_fields
)


ocr_file = "storage/ocr_results/page_1_ocr.json"

with open(ocr_file, "r", encoding="utf-8") as file:
    ocr_pages = json.load(file)


result = extract_adoption_fields(ocr_pages)


print("\nSTRUCTURED EXTRACTION RESULT")
print("----------------------------")

print(json.dumps(
    result,
    indent=4,
    ensure_ascii=False
))
