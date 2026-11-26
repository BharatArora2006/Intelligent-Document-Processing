
from pathlib import Path
import fitz
from PIL import Image, ImageOps, ImageStat


# Output directory for processed page images
PROJECT_ROOT = Path(__file__).resolve().parents[4]

PROCESSED_PATH = PROJECT_ROOT / "storage" / "processed"


def preprocess_document(file_path: str):

    source_path = Path(file_path)

    if not source_path.exists():
        raise FileNotFoundError(f"Document not found: {source_path}")

    PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

    extension = source_path.suffix.lower()

    output_folder = PROCESSED_PATH / source_path.stem
    output_folder.mkdir(parents=True, exist_ok=True)

    processed_pages = []

    # ------------------------------------------------
    # CASE 1: PDF DOCUMENT
    # ------------------------------------------------

    if extension == ".pdf":

        pdf_document = fitz.open(source_path)

        for page_number, page in enumerate(pdf_document, start=1):

            # Convert PDF page into an image at 200 DPI
            pixmap = page.get_pixmap(
                dpi=200,
                colorspace=fitz.csRGB,
                alpha=False
            )

            image_path = output_folder / f"page_{page_number}.png"

            pixmap.save(image_path)

            processed_pages.append(image_path)

        pdf_document.close()

    # ------------------------------------------------
    # CASE 2: IMAGE DOCUMENT
    # ------------------------------------------------

    elif extension in [".jpg", ".jpeg", ".png"]:

        with Image.open(source_path) as image:

            # Correct orientation using EXIF metadata
            image = ImageOps.exif_transpose(image)

            # Convert to RGB for consistent processing
            image = image.convert("RGB")

            image_path = output_folder / "page_1.png"

            image.save(image_path, format="PNG")

            processed_pages.append(image_path)

    else:

        raise ValueError(f"Unsupported file format: {extension}")

    # ------------------------------------------------
    # IMAGE QUALITY ASSESSMENT
    # ------------------------------------------------

    results = []

    for page_number, image_path in enumerate(processed_pages, start=1):

        with Image.open(image_path) as image:

            grayscale = ImageOps.grayscale(image)

            statistics = ImageStat.Stat(grayscale)

            brightness = round(statistics.mean[0], 2)

            width, height = image.size

            # Basic image resolution check
            if width < 1000 or height < 1000:
                resolution_status = "LOW_RESOLUTION"
            else:
                resolution_status = "ACCEPTABLE"

            # Basic brightness check
            if brightness < 40:
                brightness_status = "TOO_DARK"
            elif brightness > 220:
                brightness_status = "TOO_BRIGHT"
            else:
                brightness_status = "ACCEPTABLE"

            results.append({
                "page_number": page_number,
                "processed_image": str(image_path),
                "width": width,
                "height": height,
                "brightness": brightness,
                "resolution_status": resolution_status,
                "brightness_status": brightness_status
            })

    return {
        "source_document": source_path.name,
        "total_pages": len(results),
        "preprocessing_status": "SUCCESS",
        "pages": results
    }
