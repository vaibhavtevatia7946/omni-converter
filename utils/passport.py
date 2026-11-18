import io
from PIL import Image, ImageOps, ImageDraw, ImageEnhance

# Standard DPI for printing
DPI = 300

# Preset sizes in pixels at 300 DPI
PRESET_SIZES = {
    "india_standard": (413, 531),    # 35mm x 45mm
    "us_standard": (600, 600),       # 2 x 2 inch (51mm x 51mm)
    "pan_card": (295, 413),          # 25mm x 35mm
    "signature": (560, 240),         # 140 x 60 scaled 4x for high-res
}

def create_passport_photo(
    image_bytes: bytes,
    preset: str = "india_standard",
    custom_w_mm: float = None,
    custom_h_mm: float = None,
    add_border: bool = True,
    border_color: str = "#000000",
    border_width: int = 2,
    target_kb: int = 50
) -> tuple[bytes, int, int, float]:
    """
    Crops, centers, adds border, and sizes a photo to exact passport dimensions.
    """
    img = Image.open(io.BytesIO(image_bytes))
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass

    if img.mode != "RGB":
        img = img.convert("RGB")

    # Determine target dimensions in pixels
    if custom_w_mm and custom_h_mm:
        target_w = int((custom_w_mm / 25.4) * DPI)
        target_h = int((custom_h_mm / 25.4) * DPI)
    else:
        target_w, target_h = PRESET_SIZES.get(preset, (413, 531))

    # Center crop with target aspect ratio
    src_w, src_h = img.size
    target_aspect = target_w / target_h
    src_aspect = src_w / src_h

    if src_aspect > target_aspect:
        # Source is wider than target: crop left and right
        new_w = int(src_h * target_aspect)
        offset_x = (src_w - new_w) // 2
        crop_box = (offset_x, 0, offset_x + new_w, src_h)
    else:
        # Source is taller than target: crop top and bottom
        new_h = int(src_w / target_aspect)
        offset_y = (src_h - new_h) // 2
        crop_box = (0, offset_y, src_w, offset_y + new_h)

    cropped = img.crop(crop_box)
    resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)

    # Add border if requested
    if add_border and border_width > 0:
        draw = ImageDraw.Draw(resized)
        for i in range(border_width):
            draw.rectangle(
                [i, i, target_w - 1 - i, target_h - 1 - i],
                outline=border_color
            )

    # Save and compress if target_kb is specified
    buf = io.BytesIO()
    if target_kb and target_kb > 0:
        target_bytes = target_kb * 1024
        # Binary search quality
        low, high = 15, 95
        best = None
        while low <= high:
            mid = (low + high) // 2
            temp_buf = io.BytesIO()
            resized.save(temp_buf, format="JPEG", quality=mid, optimize=True)
            if temp_buf.tell() <= target_bytes:
                best = temp_buf.getvalue()
                low = mid + 1
            else:
                high = mid - 1
        if best:
            buf = io.BytesIO(best)
        else:
            resized.save(buf, format="JPEG", quality=15, optimize=True)
    else:
        resized.save(buf, format="JPEG", quality=92, optimize=True)

    result_bytes = buf.getvalue()
    final_kb = round(len(result_bytes) / 1024, 2)
    return result_bytes, target_w, target_h, final_kb

def create_passport_sheet(
    image_bytes: bytes,
    sheet_type: str = "4x6",  # "4x6" or "A4"
    preset: str = "india_standard",
    photo_count: int = 8,
    add_cutting_guidelines: bool = True
) -> tuple[bytes, int, int]:
    """
    Creates a printable photo grid sheet (e.g. 6 or 8 photos on 4x6, or 12/16/32 on A4).
    """
    # 1. Get single passport photo
    single_photo_bytes, pw, ph, _ = create_passport_photo(
        image_bytes, preset=preset, add_border=True, border_color="#cccccc", border_width=1, target_kb=0
    )
    photo_img = Image.open(io.BytesIO(single_photo_bytes))

    # Sheet dimensions (at 300 DPI)
    if sheet_type == "4x6":
        # 4x6 inch = 1200 x 1800 (or landscape 1800 x 1200)
        sheet_w, sheet_h = 1800, 1200
        # Standard 4x6 can comfortably fit 2 rows x 4 cols (8 photos) or 2 x 3 (6 photos)
        if photo_count <= 6:
            rows, cols = 2, 3
        else:
            rows, cols = 2, 4
    else:
        # A4 size = 2480 x 3508 px (portrait)
        sheet_w, sheet_h = 2480, 3508
        if photo_count <= 12:
            rows, cols = 4, 3
        elif photo_count <= 16:
            rows, cols = 4, 4
        elif photo_count <= 24:
            rows, cols = 6, 4
        else:
            rows, cols = 8, 4

    # Create white canvas
    sheet = Image.new("RGB", (sheet_w, sheet_h), (255, 255, 255))
    draw = ImageDraw.Draw(sheet)

    # Scale photo slightly if it exceeds cell bounds
    total_padding_x = int(sheet_w * 0.08)
    total_padding_y = int(sheet_h * 0.08)
    usable_w = sheet_w - total_padding_x
    usable_h = sheet_h - total_padding_y

    cell_w = usable_w // cols
    cell_h = usable_h // rows

    # Scale photo to fit comfortably with margin inside cell
    max_p_w = int(cell_w * 0.88)
    max_p_h = int(cell_h * 0.88)
    scale = min(max_p_w / pw, max_p_h / ph, 1.0)
    cur_pw, cur_ph = int(pw * scale), int(ph * scale)
    scaled_photo = photo_img.resize((cur_pw, cur_ph), Image.Resampling.LANCZOS)

    count = 0
    start_x = (sheet_w - (cols * cell_w)) // 2
    start_y = (sheet_h - (rows * cell_h)) // 2

    for r in range(rows):
        for c in range(cols):
            if count >= photo_count:
                break
            # Center in cell
            cell_x = start_x + c * cell_w
            cell_y = start_y + r * cell_h
            px = cell_x + (cell_w - cur_pw) // 2
            py = cell_y + (cell_h - cur_ph) // 2

            sheet.paste(scaled_photo, (px, py))

            # Draw dashed/subtle cutting lines around cell if requested
            if add_cutting_guidelines:
                draw.rectangle([px - 2, py - 2, px + cur_pw + 1, py + cur_ph + 1], outline="#d0d0d0", width=1)

            count += 1

    out_buf = io.BytesIO()
    sheet.save(out_buf, format="JPEG", quality=95, dpi=(DPI, DPI))
    return out_buf.getvalue(), sheet_w, sheet_h

def enhance_signature(image_bytes: bytes, target_kb: int = 20) -> tuple[bytes, float, int, int]:
    """
    Cleans background of signature photo (turns yellowish/shadowed paper to pure white)
    and sharpens ink (dark blue/black), then compresses to target KB (ideal for government forms: 10-20KB).
    """
    img = Image.open(io.BytesIO(image_bytes))
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass

    # Convert to grayscale
    gray = img.convert("L")

    # Increase contrast
    contrast = ImageEnhance.Contrast(gray)
    enhanced = contrast.enhance(2.2)

    # Thresholding: map light tones to pure white (255)
    def clean_pixel(p):
        if p > 175:
            return 255
        elif p < 90:
            return 0
        else:
            return int((p - 90) * (255 / (175 - 90)))

    cleaned = enhanced.point(clean_pixel)
    rgb_cleaned = cleaned.convert("RGB")

    # Target signature standard dimensions (approx 560 x 240 max)
    w, h = rgb_cleaned.size
    if w > 800 or h > 400:
        rgb_cleaned.thumbnail((800, 400), Image.Resampling.LANCZOS)

    # Compress to target_kb
    target_bytes = target_kb * 1024
    low, high = 15, 95
    best = None
    while low <= high:
        mid = (low + high) // 2
        buf = io.BytesIO()
        rgb_cleaned.save(buf, format="JPEG", quality=mid, optimize=True)
        if buf.tell() <= target_bytes:
            best = buf.getvalue()
            low = mid + 1
        else:
            high = mid - 1

    if not best:
        buf = io.BytesIO()
        rgb_cleaned.save(buf, format="JPEG", quality=15, optimize=True)
        best = buf.getvalue()

    final_img = Image.open(io.BytesIO(best))
    final_kb = round(len(best) / 1024, 2)
    return best, final_kb, final_img.width, final_img.height
