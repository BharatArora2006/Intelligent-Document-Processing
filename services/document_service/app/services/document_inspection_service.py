
from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image


def inspect_document(file_path: str):

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")

    extension = path.suffix.lower()

    result = {
        "filename": path.name,
        "file_extension": extension,
        "file_size_bytes": path.stat().st_size,
        "inspection_status": "SUCCESS"
    }

    # PDF inspection
    if extension == ".pdf":

        pdf_document = fitz.open(path)

        total_pages = len(pdf_document)
        extracted_text = ""

        page_details = []

        for page_number, page in enumerate(pdf_document, start=1):

            page_text = page.get_text("text")
            extracted_text += page_text

            page_details.append({
                "page_number": page_number,
                "width": round(page.rect.width, 2),
                "height": round(page.rect.height, 2),
                "text_characters": len(page_text.strip())
            })

        text_characters = len(extracted_text.strip())

        if text_characters == 0:
            pdf_type = "SCANNED_OR_IMAGE_BASED_PDF"
        else:
            pdf_type = "DIGITAL_OR_TEXT_BASED_PDF"

        result.update({
            "document_type": "PDF",
            "total_pages": total_pages,
            "pdf_content_type": pdf_type,
            "extractable_text_characters": text_characters,
            "pages": page_details
        })

        pdf_document.close()

    # Image inspection
    elif extension in [".jpg", ".jpeg", ".png"]:

        with Image.open(path) as image:

            result.update({
                "document_type": "IMAGE",
                "image_format": image.format,
                "image_width": image.width,
                "image_height": image.height,
                "image_mode": image.mode
            })

    else:
        raise ValueError(f"Unsupported document format: {extension}")

    return result
