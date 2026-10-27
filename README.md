mm<div align="center">

# ⚡ OmniConvert
### Universal All-in-One File, Document & Passport Photo Studio

[![Live Website](https://img.shields.io/badge/Live%20Website-omni--converter--web.vercel.app-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://omni-converter-web.vercel.app)

<br/>

[![CI Test Suite](https://github.com/vaibhavtevatia7946/omni-converter/actions/workflows/ci.yml/badge.svg)](https://github.com/vaibhavtevatia7946/omni-converter/actions)
[![Python Version](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![PWA Ready](https://img.shields.io/badge/PWA-Installable-blueviolet?style=flat&logo=pwa&logoColor=white)](https://web.dev/progressive-web-apps/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Fast, secure, and privacy-first web application designed for students, cyber cafes, job applicants, and professionals.**  
Convert documents, generate passport photo sheets, clean signatures, compress images/PDFs to exact KB sizes, and convert PDFs to PowerPoint presentations.

[Features](#-key-features) • [Exam Specs](#-government-exam-presets) • [PWA App](#-mobile--pwa-installation) • [Contributing](CONTRIBUTING.md)

</div>

---

## 🌟 Key Features

### 1. 📸 Passport Photo & Signature Studio
* **Single Passport Photo:** Standard Indian (3.5cm × 4.5cm), US Visa / DS-160 (2×2 inch / 600×600 px), and PAN Card dimensions.
* **Exact KB Control:** Guarantees final photo size is strictly under official limits (e.g. `20 KB`, `50 KB`, `100 KB`).
* **Printable Studio Sheets:** Arranges photos automatically onto standard **4×6 inch photo paper** (6 or 8 photos) or **A4 sheets** (12, 16, 24 photos) with dashed cutting guidelines.
* **Direct Print Button:** Prints crisp sheets directly to any attached printer with dedicated `@media print` layout.
* **Signature Cleaner:** Turns discolored/shadowed paper to pure white and enhances ink contrast for government portal approval (10–20KB).

### 2. 🗜️ Smart Exact KB Reducer (Binary Search Compression)
* **Zero Guesswork:** Achieves exact target file sizes without manual trial & error.
* **Image & PDF Compression:** Supports JPG, PNG, WEBP, and multi-page PDF documents.
* **Auto Dimension Downscaling:** Gracefully downsamples ultra-high resolution camera photos (50MP) if quality reduction alone exceeds the target KB.

### 3. 📄 Comprehensive PDF Tools
* **Images ➔ PDF:** Combines one or multiple photos into a clean, unified PDF.
* **PDF ➔ Images:** Renders all PDF pages as high-resolution PNG images (instant 1-click ZIP download).
* **Merge PDF:** Combines multiple PDFs into a single file with stream deduplication.
* **Split PDF:** Extracts page ranges (e.g., `1-3, 5`) or splits all pages into separate files.

### 4. 📊 PowerPoint (PPTX) Studio
* **PDF ➔ PPTX:** Converts PDF slides into Microsoft PowerPoint (`.pptx`) presentations.
* **Images ➔ PPTX:** Creates a widescreen (16:9) presentation slide deck from image batches.

### 5. 🔄 Image Format Converter & Resizer
* Instant conversions between **JPG, PNG, WEBP, ICO (Favicon), and BMP**.
* Custom quality and dimension resizing with aspect-ratio preservation.

---

## 📋 Government Exam Presets

OmniConvert includes built-in 1-click preset loaders for major Indian and international entrance/job forms:

| Exam / Agency | Photo Dimensions | Photo File Size | Signature Specs |
| :--- | :---: | :---: | :---: |
| **UPSC (CSE / NDA / CDS)** | 3.5cm × 4.5cm | 20 KB – 50 KB | 10 KB – 20 KB |
| **SSC (CGL / CHSL / MTS / GD)** | 3.5cm × 4.5cm | 20 KB – 50 KB | 10 KB – 20 KB |
| **IBPS / SBI (PO & Clerk)** | 200 × 230 px | 20 KB – 50 KB | 10 KB – 20 KB |
| **NTA (NEET UG / JEE Main)** | 3.5cm × 4.5cm | 10 KB – 200 KB | 4 KB – 30 KB |
| **US Visa / DS-160** | 2 × 2 inch (600×600 px) | Under 240 KB | N/A |

---

## 🏗️ Architecture & Project Structure

```
omni-converter/
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI workflow
├── api/
│   └── index.py                 # Vercel Serverless Function entry point
├── static/
│   ├── css/
│   │   └── style.css            # Custom animations, toasts & print styles
│   ├── icons/                   # PWA app icons (192x192, 512x512)
│   ├── js/
│   │   └── app.js               # Frontend controller, drag & drop, PWA installer
│   ├── manifest.json            # Web App Manifest for mobile/desktop install
│   └── service-worker.js        # Offline caching and performance optimization
├── templates/
│   └── index.html               # Responsive Tailwind CSS single-page interface
├── utils/
│   ├── compressor.py            # Binary search KB compression (Images & PDFs)
│   ├── passport.py              # Passport crop, 4x6/A4 photo sheets, signature enhancer
│   ├── pdf_tools.py             # PyMuPDF-powered PDF merge, split, extract
│   ├── ppt_tools.py             # python-pptx conversion engine
│   └── image_converter.py       # Multi-format conversion & resizer
├── launch_desktop.py            # 1-Click standalone native desktop app launcher
├── main.py                      # FastAPI web server and routing
├── requirements.txt             # Project dependencies
├── test_converter.py            # Automated unit test suite
└── vercel.json                  # Serverless deployment configuration
```

---

## 🌐 Live Website & Online Access

You can use OmniConvert directly on the web on any device (phone, tablet, PC):  
👉 **[https://omni-converter-web.vercel.app](https://omni-converter-web.vercel.app)**

* **No setup required:** Open the URL in any browser.
* **100% Free Forever:** Zero subscriptions, zero ads, zero watermarks.
* **Privacy First:** Documents and photos are processed in memory and never permanently stored.

---

## 💻 Standalone Desktop Mode

Run OmniConvert as a dedicated borderless desktop application (no browser address bar):
```bash
python launch_desktop.py
```

---

## 📱 Mobile & PWA Installation

* **Android (Chrome):** Visit the site and tap **"📲 Install App"** in the top navigation bar or select **Add to Home screen** from the browser menu.
* **iPhone / iPad (Safari):** Tap the **Share (⎙)** button and select **Add to Home Screen**.

---

## ☁️ Deployment

### Deploy to Vercel
The repository includes a production-ready `vercel.json` and `api/index.py`:
1. Push your code to GitHub.
2. Import the repository into [Vercel](https://vercel.com/new).
3. Click **Deploy**. Vercel will automatically build and deploy the serverless app.

---

## 🔒 Privacy & Security

* **In-Memory Processing:** All image cropping, PDF manipulation, and conversions are handled directly in memory buffers (`io.BytesIO`).
* **Zero Long-Term Storage:** Files are never written to permanent disk storage or shared with third parties.
* **100% Free & Open Source:** No subscription, no logins, and no watermarks.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) - feel free to use, modify, and distribute it for personal and commercial projects.
