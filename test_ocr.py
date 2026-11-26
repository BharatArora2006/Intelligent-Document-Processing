
from services.document_service.app.services.ocr_service import (
    extract_text
)


image_path = (
    "storage/processed/"
    "DOC-790A628DEFDE/"
    "page_1.png"
)


result = extract_text(image_path)


print("\nOCR EXTRACTION RESULT")
print("---------------------")

print("Source:", result["source_image"])
print("Status:", result["ocr_status"])
print("Total pages:", result["total_pages"])

for page in result["pages"]:

    print("\nPAGE:", page["page_number"])

    print("\nEXTRACTED TEXT:")
    print(page["full_text"])

    print("\nCONFIDENCE SCORES:")

    for block in page["text_blocks"]:

        print(
            block["text"],
            "=>",
            block["confidence"]
        )

print("\nJSON saved at:")
print(result["output_file"])
