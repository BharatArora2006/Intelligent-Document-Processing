
import re


def extract_adoption_fields(ocr_pages):

    # Combine OCR text from all pages
    full_text = "\n".join(
        page.get("full_text", "")
        for page in ocr_pages
    )

    # Normalize spaces while preserving line breaks
    normalised_text = re.sub(
        r"[ \t]+",
        " ",
        full_text
    )

    text_upper = normalised_text.upper()

    # Identify document type
    if (
        "FINAL JUDGMENT OF ADOPTION" in text_upper
        or "PETITION FOR ADOPTION" in text_upper
    ):
        document_type = "ADOPTION_JUDGMENT"
    else:
        document_type = "UNKNOWN"

    # ----------------------------------
    # 1. Extract County
    # ----------------------------------

    county = None

    county_patterns = [
        r"(?im)^\s*County\s*\n\s*([A-Za-z][A-Za-z .'-]*County)\s*$",
        r"PROBATE COURT OF\s+(.+?)\s+COUNTY,\s*ALABAMA"
    ]

    for pattern in county_patterns:
        match = re.search(
            pattern,
            normalised_text,
            re.IGNORECASE | re.MULTILINE | re.DOTALL
        )

        if match:
            county = match.group(1).strip()
            break

    # ----------------------------------
    # 2. Extract Case Number
    # ----------------------------------

    case_number = None

    case_match = re.search(
        r"(?im)^\s*(?:Training\s+)?Case\s*(?:Number|No\.?)"
        r"\s*[:#-]?\s*([A-Z0-9][A-Z0-9/-]*)\s*$",
        normalised_text
    )

    if case_match:
        case_number = case_match.group(1).strip()

    # ----------------------------------
    # 3. Extract Child Name
    # ----------------------------------

    child_name = None

    child_patterns = [
        r"(?im)^\s*Child'?s?\s+Name\s*\n\s*"
        r"([A-Za-z][A-Za-z .'-]+)\s*$",

        r"IN THE MATTER OF THE ADOPTION OF\s*\n\s*"
        r"([A-Z][A-Z .'-]+)\s*(?:\n|$)",

        r"name of the adoptee in this matter is hereby changed to"
        r"\s+([^,\n]+)"
    ]

    for pattern in child_patterns:
        match = re.search(
            pattern,
            normalised_text,
            re.IGNORECASE | re.MULTILINE
        )

        if match:
            child_name = match.group(1).strip()
            break

    # ----------------------------------
    # 4. Extract Adoption Date
    # ----------------------------------

    adoption_date = None

    date_patterns = [
        r"(?im)^\s*Date of Adoption\s*\n\s*"
        r"([A-Za-z]+\s+\d{1,2},?\s+\d{4})\s*$",

        r"adoption date of\s+"
        r"([A-Za-z]+\s+\d{1,2},?\s+\d{4})",

        r"Done this\s+(\d{1,2})\s+day of\s+"
        r"([A-Za-z]+),?\s+(\d{4})"
    ]

    for pattern in date_patterns:
        match = re.search(
            pattern,
            normalised_text,
            re.IGNORECASE | re.MULTILINE
        )

        if match:
            adoption_date = " ".join(
                group for group in match.groups() if group
            ).strip()
            break

    # ----------------------------------
    # 5. Identify Authority and State
    # ----------------------------------

    issuing_authority = (
        "Probate Court"
        if "PROBATE COURT" in text_upper
        else None
    )

    state = (
        "Alabama"
        if "ALABAMA" in text_upper
        else None
    )

    # ----------------------------------
    # 6. Build Extracted Fields
    # ----------------------------------

    fields = {
        "document_type": document_type,
        "issuing_authority": issuing_authority,
        "state": state,
        "county": county,
        "case_number": case_number,
        "child_name": child_name,
        "adoption_date": adoption_date
    }

    # Identify missing fields
    missing_fields = [
        field_name
        for field_name, value in fields.items()
        if value is None
    ]

    # Determine extraction status
    extraction_status = (
        "SUCCESS"
        if not missing_fields
        else "PARTIAL"
    )

    return {
        "extraction_status": extraction_status,
        "extracted_fields": fields,
        "missing_fields": missing_fields
    }
