# ⚡ OmniConvert - Universal All-in-One File & Document Converter

OmniConvert ek complete web application hai jo daily aur government job form requirements ko ek hi jagah solve karta hai.

---

## 🌟 Features Included

### 1. 📸 Passport Photo & Signature Maker
- **Single Passport Photo:** Standard Indian (3.5cm x 4.5cm), US Visa (2x2 inch), aur PAN Card sizes with borders.
- **Exact KB Control:** Photo ka size form requirements ke mutabik (e.g. under 20KB, 50KB, 100KB) adjust hota hai.
- **Printable Photo Sheets:** 4x6 inch studio paper ya A4 sheet par 6, 8, 12, 16, 24 photos with cutting guidelines.
- **Signature Cleaner:** Signature photo ka background pure white karta hai aur ink ko crisp dark black/blue banata hai (10-20KB limit).

### 2. 🗜️ Exact KB Reducer / Compressor
- Images (JPG, PNG, WEBP) aur PDF files ko exact target size (e.g. 20KB, 50KB, 100KB, 200KB, 500KB) mein compress karta hai bina visual quality lose kiye.

### 3. 📄 PDF Tools
- **Images ➔ PDF:** Multiple photos ko ek clean PDF document banayein.
- **PDF ➔ Images:** PDF ke saare pages high-resolution PNG format mein extract karein (ZIP download).
- **Merge PDF:** Multiple PDFs ko ek single file mein jodein.
- **Split PDF:** Specific pages ya saare pages alag karein.

### 4. 📊 PowerPoint (PPT) Converter
- **PDF ➔ PPTX:** PDF documents ko PowerPoint presentation slides mein convert karein.
- **Images ➔ PPTX:** Photos se widescreen (16:9) slide deck banayein.

### 5. 🔄 Image Format & Resizer
- JPG ⇄ PNG ⇄ WEBP ⇄ ICO ⇄ BMP conversions with custom quality settings.

---

## 🚀 How to Run

1. Open Terminal and go to the directory:
   ```bash
   cd /Users/vaibhav/.gemini/antigravity/scratch/omni-converter
   ```

2. Run the start script:
   ```bash
   ./run.sh
   ```
   *Ya seedha command:*
   ```bash
   ./venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

3. Open your browser at:
   **http://127.0.0.1:8000**
