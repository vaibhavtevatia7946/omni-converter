import io
import fitz  # PyMuPDF
from PIL import Image, ImageOps

def compress_image_to_target_kb(image_bytes: bytes, target_kb: int, output_format: str = "JPEG") -> tuple[bytes, float, int, int]:
    """
    Compresses an image to be strictly less than or equal to target_kb.
    Uses binary search for JPEG quality, and downscaling if needed.
    """
    target_bytes = target_kb * 1024
    img = Image.open(io.BytesIO(image_bytes))
    
    # Handle EXIF orientation
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass
        
    # Convert RGBA to RGB if saving as JPEG
    if output_format.upper() in ["JPEG", "JPG"]:
        if img.mode in ("RGBA", "LA", "P"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")
    elif output_format.upper() == "PNG":
        # PNG doesn't use quality param the same way, we can try optimize & resize
        pass

    current_img = img.copy()
    scale_factor = 1.0
    best_buffer = None

    # Loop to scale down if quality adjustments alone can't reach target_kb
    for _ in range(6):
        low, high = 10, 95
        best_local = None

        while low <= high:
            mid = (low + high) // 2
            buf = io.BytesIO()
            save_kwargs = {"format": output_format, "optimize": True}
            if output_format.upper() in ["JPEG", "JPG", "WEBP"]:
                save_kwargs["quality"] = mid
            
            current_img.save(buf, **save_kwargs)
            size = buf.tell()

            if size <= target_bytes:
                best_local = buf.getvalue()
                low = mid + 1  # Try higher quality
            else:
                high = mid - 1 # Reduce quality

        if best_local is not None:
            best_buffer = best_local
            break
        
        # If even quality 10 didn't make it fit, scale image down by 80%
        w, h = current_img.size
        new_w, new_h = max(int(w * 0.8), 100), max(int(h * 0.8), 100)
        if new_w == w and new_h == h:
            break
        current_img = current_img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    if best_buffer is None:
        # Fallback lowest quality
        buf = io.BytesIO()
        current_img.save(buf, format=output_format, quality=10, optimize=True)
        best_buffer = buf.getvalue()

    final_img = Image.open(io.BytesIO(best_buffer))
    final_kb = round(len(best_buffer) / 1024, 2)
    return best_buffer, final_kb, final_img.width, final_img.height

def compress_pdf(pdf_bytes: bytes, dpi: int = 120, image_quality: int = 65) -> tuple[bytes, float, float]:
    """
    Compresses a PDF document using PyMuPDF:
    - Downsamples high-resolution embedded images to given dpi & quality.
    - Cleans garbage and deduplicates objects.
    """
    original_kb = round(len(pdf_bytes) / 1024, 2)
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    # Re-compress each page's images or optimize document
    for page in doc:
        image_list = page.get_images(full=True)
        for img_info in image_list:
            xref = img_info[0]
            try:
                base_image = doc.extract_image(xref)
                if not base_image:
                    continue
                image_bytes = base_image["image"]
                pil_img = Image.open(io.BytesIO(image_bytes))
                
                # Check if it needs recompression
                if pil_img.format in ["JPEG", "PNG", "TIFF"]:
                    if pil_img.mode in ("RGBA", "P"):
                        pil_img = pil_img.convert("RGB")
                    
                    # Resize if too large
                    max_dim = int(dpi * 11)  # approx max dimension on letter/A4
                    if pil_img.width > max_dim or pil_img.height > max_dim:
                        pil_img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
                        
                    buf = io.BytesIO()
                    pil_img.save(buf, format="JPEG", quality=image_quality, optimize=True)
                    doc.update_stream(xref, buf.getvalue())
            except Exception:
                continue

    out_buf = io.BytesIO()
    # Garbage=4 cleans unused objects, deflate=True compresses streams
    doc.save(out_buf, garbage=4, deflate=True, clean=True)
    doc.close()
    
    result_bytes = out_buf.getvalue()
    # If the compressed is somehow larger than original, return original
    if len(result_bytes) > len(pdf_bytes):
        return pdf_bytes, original_kb, original_kb

    final_kb = round(len(result_bytes) / 1024, 2)
    return result_bytes, original_kb, final_kb

def compress_pdf_to_target_kb(pdf_bytes: bytes, target_kb: int) -> tuple[bytes, float, float]:
    """
    Tries to compress PDF to be under target_kb by testing presets (high, medium, low, aggressive).
    """
    original_kb = round(len(pdf_bytes) / 1024, 2)
    presets = [
        (150, 75),
        (120, 60),
        (96, 45),
        (72, 30)
    ]
    
    best_bytes = pdf_bytes
    best_kb = original_kb
    
    for dpi, quality in presets:
        res_bytes, _, kb = compress_pdf(pdf_bytes, dpi=dpi, image_quality=quality)
        if kb < best_kb:
            best_bytes = res_bytes
            best_kb = kb
        if kb <= target_kb:
            return best_bytes, original_kb, best_kb
            
    return best_bytes, original_kb, best_kb
