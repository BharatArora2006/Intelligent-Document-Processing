
import json
from pathlib import Path

from paddleocr import PaddleOCR


PROJECT_ROOT = Path(__file__).resolve().parents[4]

OCR_OUTPUT_PATH = PROJECT_ROOT / "storage" / "ocr_results"

# Load the OCR model only once.
_ocr_engine = None


def get_ocr_engine():

    global _ocr_engine

    if _ocr_engine is None:

        _ocr_engine = PaddleOCR(
            lang="en",
            device="cpu",
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False
        )

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

    # Get OCR engine
    ocr_engine = get_ocr_engine()

    # Run OCR
    prediction_results = ocr_engine.predict(
        input=str(source_path)
    )

    extracted_pages = []

    for page_number, prediction in enumerate(
        prediction_results,
        start=1
    ):

        # Get structured OCR result
        result_data = prediction.json

        if "res" in result_data:
            result_data = result_data["res"]

        recognized_texts = result_data.get(
            "rec_texts", []
        )

        confidence_scores = result_data.get(
            "rec_scores", []
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

        extracted_pages.append({
            "page_number": page_number,
            "total_text_blocks": len(text_blocks),
            "full_text": full_text,
            "text_blocks": text_blocks
        })

    document_ocr_folder = OCR_OUTPUT_PATH / source_path.parent.name
    document_ocr_folder.mkdir(parents=True, exist_ok=True)

    output_file = document_ocr_folder / f"{source_path.stem}_ocr.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(extracted_pages, file, indent=4, ensure_ascii=False)

    return {
        "source_image": source_path.name,
        "ocr_status": "SUCCESS",
        "total_pages": len(extracted_pages),
        "output_file": str(output_file),
        "pages": extracted_pages
    }
