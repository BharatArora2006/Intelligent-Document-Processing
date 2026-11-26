import json
from pathlib import Path

from services.document_service.app.services.ai_extraction_service import (
    extract_adoption_fields_with_ai
)


PROJECT_ROOT = Path(__file__).resolve().parent

OCR_FILE = (
    PROJECT_ROOT
    / "storage"
    / "ocr_results"
    /"DOC-E48BC8C2FF66"
    / "page_1_ocr.json"
)
    

with open(OCR_FILE, "r", encoding="utf-8") as file:
    ocr_pages = json.load(file)

result = extract_adoption_fields_with_ai(ocr_pages)

print("\nAI EXTRACTION RESULT")
print("--------------------")

print(json.dumps(result, indent=4, ensure_ascii=False))