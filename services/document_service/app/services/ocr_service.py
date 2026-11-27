
import json
from pathlib import Path

from rapidocr import RapidOCR


PROJECT_ROOT = Path(__file__).resolve().parents[4]

OCR_OUTPUT_PATH = PROJECT_ROOT / "storage" / "ocr_results"

# Load the OCR engine only once.
_ocr_engine = None


def get_ocr_engine():

    global _ocr_engine

    if _ocr_engine is None:
        _ocr_engine = RapidOCR()

    return _ocr_engine


def extract_text(image_path: str):

    source_path = Path(image_path)

    if not source_path.exists():
        raise FileNotFoundError(
            f"Image not found: {source_path}"
        )

    OCR_OUTPUT_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    ocr_engine = get_ocr_engine()

    # Run OCR
    prediction = ocr_engine(str(source_path))

    recognized_texts = (
        prediction.txts if prediction else []
    )

    confidence_scores = (
        prediction.scores if prediction else []
    )

    text_blocks = []

    for index, text in enumerate(recognized_texts):

        score = (
            float(confidence_scores[index])
            if index < len(confidence_scores)
            else None
        )

        text_blocks.append({
            "text": text,
            "confidence": round(score, 4)
            if score is not None else None
        })

    full_text = "\n".join(
        block["text"]
        for block in text_blocks
    )

    extracted_pages = [{
        "page_number": 1,
        "total_text_blocks": len(text_blocks),
        "full_text": full_text,
        "text_blocks": text_blocks
    }]

    document_ocr_folder = (
        OCR_OUTPUT_PATH / source_path.parent.name
    )

    document_ocr_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        document_ocr_folder /
        f"{source_path.stem}_ocr.json"
    )

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(
            extracted_pages,
            file,
            indent=4,
            ensure_ascii=False
        )

    return {
        "source_image": source_path.name,
        "ocr_status": "SUCCESS",
        "total_pages": len(extracted_pages),
        "output_file": str(output_file),
        "pages": extracted_pages
    }
