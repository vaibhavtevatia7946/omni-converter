import io
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from PIL import Image
import fitz

def images_to_pptx(images: list[bytes], aspect_ratio: str = "16:9") -> bytes:
    """
    Creates a clean modern PowerPoint (.pptx) presentation from a list of images.
    Each image becomes a high-res full slide.
    """
    prs = Presentation()
    
    # 16:9 widescreen: 13.33 x 7.5 inches
    # 4:3 standard: 10.0 x 7.5 inches
    if aspect_ratio == "16:9":
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
    else:
        prs.slide_width = Inches(10.0)
        prs.slide_height = Inches(7.5)

    blank_slide_layout = prs.slide_layouts[6]  # Blank slide

    for img_bytes in images:
        slide = prs.slides.add_slide(blank_slide_layout)
        
        # Calculate aspect ratio to fit slide cleanly
        img = Image.open(io.BytesIO(img_bytes))
        img_w, img_h = img.size
        slide_w, slide_h = prs.slide_width, prs.slide_height

        img_ratio = img_w / img_h
        slide_ratio = slide_w / slide_h

        if img_ratio > slide_ratio:
            # Fit by width
            target_w = slide_w
            target_h = int(slide_w / img_ratio)
            left = Inches(0)
            top = int((slide_h - target_h) / 2)
        else:
            # Fit by height
            target_h = slide_h
            target_w = int(slide_h * img_ratio)
            top = Inches(0)
            left = int((slide_w - target_w) / 2)

        image_stream = io.BytesIO(img_bytes)
        slide.shapes.add_picture(image_stream, left, top, target_w, target_h)

    out_buf = io.BytesIO()
    prs.save(out_buf)
    return out_buf.getvalue()

def pdf_to_pptx(pdf_bytes: bytes, dpi: int = 150) -> bytes:
    """
    Converts a PDF document to an editable PPTX presentation
    by rendering high-res pages and laying them into PPTX slides.
    """
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)
    images = []

    for page in doc:
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        images.append(pix.tobytes(output="png"))

    doc.close()
    return images_to_pptx(images)

def extract_pptx_images(pptx_bytes: bytes) -> list[tuple[str, bytes]]:
    """
    Extracts all embedded images from a PPTX file.
    Returns list of (filename, bytes).
    """
    prs = Presentation(io.BytesIO(pptx_bytes))
    extracted = []
    img_counter = 1

    for s_idx, slide in enumerate(prs.slides):
        for shape in slide.shapes:
            if shape.shape_type == 13:  # Picture
                image = shape.image
                ext = image.ext
                extracted.append((f"slide_{s_idx + 1}_img_{img_counter}.{ext}", image.blob))
                img_counter += 1

    return extracted
