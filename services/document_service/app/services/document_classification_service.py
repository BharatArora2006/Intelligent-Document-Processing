
import re


DOCUMENT_KEYWORDS = {
    "ADOPTION_JUDGMENT": [
        "FINAL JUDGMENT OF ADOPTION",
        "PETITION FOR ADOPTION",
        "LEGALLY ADOPTED"
    ],

    "BIRTH_CERTIFICATE": [
        "CERTIFICATE OF LIVE BIRTH",
        "BIRTH CERTIFICATE",
        "DATE OF BIRTH",
        "PLACE OF BIRTH"
    ],

    "MARRIAGE_CERTIFICATE": [
        "MARRIAGE CERTIFICATE",
        "CERTIFICATE OF MARRIAGE",
        "DATE OF MARRIAGE"
    ],

    "DRIVING_LICENSE": [
        "DRIVER LICENSE",
        "DRIVING LICENCE",
        "DRIVER'S LICENSE",
        "DATE OF EXPIRATION"
    ],

    "DEPENDENT_VERIFICATION_FORM": [
        "DEPENDENT VERIFICATION",
        "DEPENDENT INFORMATION",
        "EMPLOYEE INFORMATION"
    ]
}


def classify_document(ocr_pages):

    full_text = "\n".join(
        page.get("full_text", "")
        for page in ocr_pages
    )

    normalised_text = re.sub(
        r"\s+",
        " ",
        full_text
    ).upper()

    scores = {}

    for document_type, keywords in DOCUMENT_KEYWORDS.items():

        score = sum(
            1 for keyword in keywords
            if keyword in normalised_text
        )

        scores[document_type] = score

    best_type = max(scores, key=scores.get)
    best_score = scores[best_type]

    if best_score == 0:
        return {
            "classification_status": "UNCLASSIFIED",
            "document_type": "UNKNOWN",
            "matched_keywords": [],
            "classification_scores": scores
        }

    matched_keywords = [
        keyword
        for keyword in DOCUMENT_KEYWORDS[best_type]
        if keyword in normalised_text
    ]

    return {
        "classification_status": "CLASSIFIED",
        "document_type": best_type,
        "matched_keywords": matched_keywords,
        "classification_scores": scores
    }
