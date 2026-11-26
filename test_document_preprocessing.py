
from services.document_service.app.services.document_preprocessing_service import (
    preprocess_document
)

document_path = (
    "storage/documents/"
    "SUB-01FC161884DD/"
    "DOC-790A628DEFDE.jpg"
)

result = preprocess_document(document_path)

print("\nDOCUMENT PREPROCESSING RESULT")
print("--------------------------------")

print("Source:", result["source_document"])
print("Total pages:", result["total_pages"])
print("Status:", result["preprocessing_status"])

for page in result["pages"]:

    print("\nPage:", page["page_number"])
    print("Image:", page["processed_image"])
    print("Dimensions:", page["width"], "x", page["height"])
    print("Brightness:", page["brightness"])
    print("Resolution:", page["resolution_status"])
    print("Brightness status:", page["brightness_status"])
