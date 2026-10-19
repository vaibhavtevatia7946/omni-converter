import io
from PIL import Image, ImageOps

SUPPORTED_FORMATS = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "webp": "WEBP",
    "bmp": "BMP",
    "tiff": "TIFF",
    "ico": "ICO",
    "gif": "GIF"
}

def get_image_info(image_bytes: bytes) -> dict:
    img = Image.open(io.BytesIO(image_bytes))
    return {
        "width": img.width,
        "height": img.height,
        "format": img.format or "UNKNOWN",
        "mode": img.mode,
        "size_kb": round(len(image_bytes) / 1024, 2)
    }

def convert_image_format(
    image_bytes: bytes,
    target_format: str = "PNG",
    quality: int = 90
) -> tuple[bytes, str]:
    """
    Converts image to target format (JPG, PNG, WEBP, BMP, TIFF, ICO).
    Handles color modes (e.g. RGBA to RGB for JPEG).
    """
    img = Image.open(io.BytesIO(image_bytes))
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass

    fmt = SUPPORTED_FORMATS.get(target_format.lower(), target_format.upper())

    if fmt == "JPEG":
        if img.mode in ("RGBA", "LA", "P"):
            bg = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            bg.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
            img = bg
        elif img.mode != "RGB":
            img = img.convert("RGB")
    elif fmt == "ICO":
        # ICO needs small square or thumbnail
        img = img.convert("RGBA")
        img.thumbnail((256, 256), Image.Resampling.LANCZOS)
    elif fmt in ["PNG", "WEBP"]:
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA")

    out_buf = io.BytesIO()
    save_args = {"format": fmt}
    if fmt in ["JPEG", "WEBP"]:
        save_args["quality"] = quality
        save_args["optimize"] = True

    img.save(out_buf, **save_args)
    return out_buf.getvalue(), fmt.lower()

def resize_image_dimensions(
    image_bytes: bytes,
    target_width: int = None,
    target_height: int = None,
    maintain_aspect: bool = True
) -> tuple[bytes, int, int]:
    img = Image.open(io.BytesIO(image_bytes))
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass

    orig_w, orig_h = img.size

    if maintain_aspect:
        if target_width and not target_height:
            target_height = int(orig_h * (target_width / orig_w))
        elif target_height and not target_width:
            target_width = int(orig_w * (target_height / orig_h))
        elif target_width and target_height:
            img.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
            out_buf = io.BytesIO()
            img.save(out_buf, format=img.format or "JPEG", quality=92)
            return out_buf.getvalue(), img.width, img.height
    else:
        target_width = target_width or orig_w
        target_height = target_height or orig_h

    resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    out_buf = io.BytesIO()
    resized.save(out_buf, format=img.format or "JPEG", quality=92)
    return out_buf.getvalue(), target_width, target_height
