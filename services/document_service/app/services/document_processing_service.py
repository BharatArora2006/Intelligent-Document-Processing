
from services.document_service.app.services.ocr_service import extract_text
from services.document_service.app.services.document_classification_service import classify_document
from services.document_service.app.services.field_extraction_service import extract_adoption_fields
from services.document_service.app.services.ai_extraction_service import extract_adoption_fields_with_ai


def process_document(image_paths: list[str]):
    """
    Process all pages belonging to one document.
    """

    all_ocr_pages = []

    # Step 1: Run OCR on every page
    for image_path in image_paths:
        ocr_result = extract_text(image_path)
        all_ocr_pages.extend(ocr_result["pages"])

    # Step 2: Classify the complete document
    classification_result = classify_document(all_ocr_pages)
    document_type = classification_result["document_type"]

    # Step 3: Extract fields based on document type
    if document_type == "ADOPTION_JUDGMENT":

        try:
            # Primary extraction: Groq AI
            extraction_result = extract_adoption_fields_with_ai(
                all_ocr_pages
            )

            extraction_result["extraction_method"] = "GROQ_AI"

        except Exception as error:

            # Fallback extraction: Existing rule-based method
            extraction_result = extract_adoption_fields(
                all_ocr_pages
            )

            extraction_result["extraction_method"] = (
                "RULE_BASED_FALLBACK"
            )

            extraction_result["ai_error"] = str(error)

    else:
        extraction_result = {
            "extraction_status": "NOT_SUPPORTED",
            "extracted_fields": {},
            "missing_fields": [],
            "extraction_method": "NOT_APPLICABLE"
        }

    # Step 4: Return complete document result
    return {
        "processing_status": "SUCCESS",
        "document_type": document_type,
        "total_pages": len(all_ocr_pages),
        "ocr_pages": all_ocr_pages,
        "classification": classification_result,
        "extraction": extraction_result
    }
