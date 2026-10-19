import io
import fitz  # PyMuPDF
from PIL import Image, ImageOps

def images_to_pdf(image_list: list[bytes]) -> bytes:
    """
    Converts one or multiple images into a single clean PDF document.
    """
    pil_images = []
    for img_bytes in image_list:
        im = Image.open(io.BytesIO(img_bytes))
        try:
            im = ImageOps.exif_transpose(im)
        except Exception:
            pass

        if im.mode in ("RGBA", "LA", "P"):
            bg = Image.new("RGB", im.size, (255, 255, 255))
            if im.mode == "P":
                im = im.convert("RGBA")
            bg.paste(im, mask=im.split()[-1] if im.mode == "RGBA" else None)
            im = bg
        elif im.mode != "RGB":
            im = im.convert("RGB")

        pil_images.append(im)

    if not pil_images:
        raise ValueError("No images provided")

    out_buf = io.BytesIO()
    first_image = pil_images[0]
    rest = pil_images[1:] if len(pil_images) > 1 else []
    first_image.save(out_buf, format="PDF", save_all=True, append_images=rest, resolution=100.0)
    return out_buf.getvalue()

def pdf_to_images(pdf_bytes: bytes, dpi: int = 150) -> list[tuple[int, bytes]]:
    """
    Extracts all pages from a PDF as PNG image bytes.
    Returns list of (page_number_1_indexed, image_bytes).
    """
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    results = []

    # Matrix for desired DPI (72 is standard base PDF DPI)
    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)

    for i, page in enumerate(doc):
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        img_bytes = pix.tobytes(output="png")
        results.append((i + 1, img_bytes))

    doc.close()
    return results

def merge_pdfs(pdf_list: list[bytes]) -> bytes:
    """
    Combines multiple PDF files into a single unified PDF.
    """
    merged_doc = fitz.open()
    for p_bytes in pdf_list:
        sub_doc = fitz.open(stream=p_bytes, filetype="pdf")
        merged_doc.insert_pdf(sub_doc)
        sub_doc.close()

    out_buf = io.BytesIO()
    merged_doc.save(out_buf, garbage=4, deflate=True)
    merged_doc.close()
    return out_buf.getvalue()

def split_pdf(pdf_bytes: bytes, page_selection: str = "all") -> list[tuple[str, bytes]]:
    """
    Splits a PDF into individual pages or extracts specific pages/ranges.
    e.g., page_selection = '1-3, 5' or 'all'
    Returns list of (filename, bytes).
    """
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    total_pages = len(doc)
    selected_indices = set()

    if not page_selection or page_selection.strip().lower() == "all":
        selected_indices = set(range(total_pages))
    else:
        parts = page_selection.split(",")
        for part in parts:
            part = part.strip()
            if "-" in part:
                sub = part.split("-")
                start = max(1, int(sub[0].strip()))
                end = min(total_pages, int(sub[1].strip()))
                for p in range(start, end + 1):
                    selected_indices.add(p - 1)
            elif part.isdigit():
                p = int(part)
                if 1 <= p <= total_pages:
                    selected_indices.add(p - 1)

    results = []
    for idx in sorted(selected_indices):
        new_doc = fitz.open()
        new_doc.insert_pdf(doc, from_page=idx, to_page=idx)
        out_buf = io.BytesIO()
        new_doc.save(out_buf, garbage=4, deflate=True)
        new_doc.close()
        results.append((f"page_{idx + 1}.pdf", out_buf.getvalue()))

    doc.close()
    return results
