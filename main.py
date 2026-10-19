import io
import os
import zipfile
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from utils.compressor import compress_image_to_target_kb, compress_pdf_to_target_kb
from utils.passport import create_passport_photo, create_passport_sheet, enhance_signature
from utils.pdf_tools import images_to_pdf, pdf_to_images, merge_pdfs, split_pdf
from utils.ppt_tools import images_to_pptx, pdf_to_pptx, extract_pptx_images
from utils.image_converter import convert_image_format, resize_image_dimensions, get_image_info

app = FastAPI(
    title="OmniConvert - Universal All-in-One Converter",
    description="All-in-one file converter for Passport Photo, KB Reducer, PDF, PPT, and Image formatting.",
    version="1.0.0"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Mount static directory
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    template_path = os.path.join(BASE_DIR, "templates", "index.html")
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/manifest.json")
async def get_manifest():
    return FileResponse(os.path.join(BASE_DIR, "static", "manifest.json"), media_type="application/manifest+json")

@app.get("/service-worker.js")
async def get_service_worker():
    return FileResponse(os.path.join(BASE_DIR, "static", "service-worker.js"), media_type="application/javascript")

@app.get("/favicon.ico")
async def get_favicon():
    return FileResponse(os.path.join(BASE_DIR, "static", "favicon.ico"), media_type="image/x-icon")


# ----------------- PASSPORT PHOTO & SIGNATURE -----------------

@app.post("/api/passport/single")
async def api_passport_single(
    file: UploadFile = File(...),
    preset: str = Form("india_standard"),
    add_border: bool = Form(True),
    border_color: str = Form("#000000"),
    border_width: int = Form(2),
    target_kb: int = Form(50)
):
    try:
        content = await file.read()
        res_bytes, w, h, final_kb = create_passport_photo(
            content,
            preset=preset,
            add_border=add_border,
            border_color=border_color,
            border_width=border_width,
            target_kb=target_kb
        )
        filename = f"passport_{preset}_{final_kb}kb.jpg"
        return StreamingResponse(
            io.BytesIO(res_bytes),
            media_type="image/jpeg",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "X-Final-Size-KB": str(final_kb),
                "X-Width": str(w),
                "X-Height": str(h)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/passport/sheet")
async def api_passport_sheet(
    file: UploadFile = File(...),
    sheet_type: str = Form("4x6"),
    preset: str = Form("india_standard"),
    photo_count: int = Form(8)
):
    try:
        content = await file.read()
        res_bytes, w, h = create_passport_sheet(
            content,
            sheet_type=sheet_type,
            preset=preset,
            photo_count=photo_count,
            add_cutting_guidelines=True
        )
        filename = f"passport_sheet_{sheet_type}_{photo_count}photos.jpg"
        return StreamingResponse(
            io.BytesIO(res_bytes),
            media_type="image/jpeg",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/passport/signature")
async def api_passport_signature(
    file: UploadFile = File(...),
    target_kb: int = Form(20)
):
    try:
        content = await file.read()
        res_bytes, final_kb, w, h = enhance_signature(content, target_kb=target_kb)
        filename = f"signature_enhanced_{final_kb}kb.jpg"
        return StreamingResponse(
            io.BytesIO(res_bytes),
            media_type="image/jpeg",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "X-Final-Size-KB": str(final_kb)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ----------------- COMPRESSOR (KB REDUCER) -----------------

@app.post("/api/compress/image")
async def api_compress_image(
    file: UploadFile = File(...),
    target_kb: int = Form(50),
    format: str = Form("JPEG")
):
    try:
        content = await file.read()
        res_bytes, final_kb, w, h = compress_image_to_target_kb(
            content, target_kb=target_kb, output_format=format
        )
        ext = "jpg" if format.upper() in ["JPEG", "JPG"] else format.lower()
        filename = f"compressed_{final_kb}kb.{ext}"
        return StreamingResponse(
            io.BytesIO(res_bytes),
            media_type=f"image/{ext}",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "X-Final-Size-KB": str(final_kb),
                "X-Dimensions": f"{w}x{h}"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/compress/pdf")
async def api_compress_pdf(
    file: UploadFile = File(...),
    target_kb: int = Form(300)
):
    try:
        content = await file.read()
        res_bytes, orig_kb, final_kb = compress_pdf_to_target_kb(content, target_kb=target_kb)
        filename = f"compressed_{final_kb}kb.pdf"
        return StreamingResponse(
            io.BytesIO(res_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "X-Original-Size-KB": str(orig_kb),
                "X-Final-Size-KB": str(final_kb)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ----------------- PDF TOOLS -----------------

@app.post("/api/pdf/images-to-pdf")
async def api_images_to_pdf(files: list[UploadFile] = File(...)):
    try:
        image_bytes_list = [await f.read() for f in files]
        pdf_bytes = images_to_pdf(image_bytes_list)
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": 'attachment; filename="converted_document.pdf"'}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/pdf/pdf-to-images")
async def api_pdf_to_images(
    file: UploadFile = File(...),
    dpi: int = Form(150)
):
    try:
        content = await file.read()
        extracted = pdf_to_images(content, dpi=dpi)

        if len(extracted) == 1:
            # Single page, return directly as PNG
            return StreamingResponse(
                io.BytesIO(extracted[0][1]),
                media_type="image/png",
                headers={"Content-Disposition": 'attachment; filename="page_1.png"'}
            )

        # Multi-page, zip them
        zip_buf = io.BytesIO()
        with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for page_num, img_bytes in extracted:
                zip_file.writestr(f"page_{page_num}.png", img_bytes)

        zip_buf.seek(0)
        return StreamingResponse(
            zip_buf,
            media_type="application/zip",
            headers={"Content-Disposition": 'attachment; filename="pdf_pages.zip"'}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/pdf/merge")
async def api_pdf_merge(files: list[UploadFile] = File(...)):
    try:
        pdf_bytes_list = [await f.read() for f in files]
        merged = merge_pdfs(pdf_bytes_list)
        return StreamingResponse(
            io.BytesIO(merged),
            media_type="application/pdf",
            headers={"Content-Disposition": 'attachment; filename="merged_document.pdf"'}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/pdf/split")
async def api_pdf_split(
    file: UploadFile = File(...),
    page_selection: str = Form("all")
):
    try:
        content = await file.read()
        splits = split_pdf(content, page_selection=page_selection)
        
        if len(splits) == 1:
            name, p_bytes = splits[0]
            return StreamingResponse(
                io.BytesIO(p_bytes),
                media_type="application/pdf",
                headers={"Content-Disposition": f'attachment; filename="{name}"'}
            )

        zip_buf = io.BytesIO()
        with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for name, p_bytes in splits:
                zip_file.writestr(name, p_bytes)

        zip_buf.seek(0)
        return StreamingResponse(
            zip_buf,
            media_type="application/zip",
            headers={"Content-Disposition": 'attachment; filename="split_pages.zip"'}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ----------------- PPT TOOLS -----------------

@app.post("/api/ppt/pdf-to-pptx")
async def api_pdf_to_pptx(file: UploadFile = File(...)):
    try:
        content = await file.read()
        pptx_bytes = pdf_to_pptx(content)
        return StreamingResponse(
            io.BytesIO(pptx_bytes),
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            headers={"Content-Disposition": 'attachment; filename="converted_presentation.pptx"'}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/ppt/images-to-pptx")
async def api_images_to_pptx(
    files: list[UploadFile] = File(...),
    aspect_ratio: str = Form("16:9")
):
    try:
        image_list = [await f.read() for f in files]
        pptx_bytes = images_to_pptx(image_list, aspect_ratio=aspect_ratio)
        return StreamingResponse(
            io.BytesIO(pptx_bytes),
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            headers={"Content-Disposition": 'attachment; filename="presentation.pptx"'}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ----------------- IMAGE CONVERTER & RESIZER -----------------

@app.post("/api/image/convert")
async def api_image_convert(
    file: UploadFile = File(...),
    target_format: str = Form("PNG"),
    quality: int = Form(90)
):
    try:
        content = await file.read()
        res_bytes, ext = convert_image_format(content, target_format=target_format, quality=quality)
        orig_name = os.path.splitext(file.filename)[0] or "converted"
        filename = f"{orig_name}.{ext}"
        mime = f"image/{ext}" if ext != "ico" else "image/x-icon"
        return StreamingResponse(
            io.BytesIO(res_bytes),
            media_type=mime,
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/image/resize")
async def api_image_resize(
    file: UploadFile = File(...),
    width: int = Form(None),
    height: int = Form(None),
    maintain_aspect: bool = Form(True)
):
    try:
        content = await file.read()
        res_bytes, final_w, final_h = resize_image_dimensions(
            content, target_width=width, target_height=height, maintain_aspect=maintain_aspect
        )
        filename = f"resized_{final_w}x{final_h}_{file.filename}"
        return StreamingResponse(
            io.BytesIO(res_bytes),
            media_type="image/jpeg",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
