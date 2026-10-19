// OmniConvert World-Class Client Application

let currentPassportMode = 'single'; // 'single' | 'sheet' | 'signature'
let currentPdfMode = 'img2pdf';      // 'img2pdf' | 'pdf2img' | 'merge' | 'split'
let currentPptMode = 'pdf2ppt';      // 'pdf2ppt' | 'img2ppt'

// --- TOAST NOTIFICATIONS ---
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  const bgColors = {
    success: 'bg-emerald-600 text-white',
    error: 'bg-rose-600 text-white',
    info: 'bg-slate-900 text-white'
  };

  const icons = {
    success: '✓',
    error: '✕',
    info: 'ℹ'
  };

  toast.className = `toast flex items-center gap-2.5 px-4 py-2.5 rounded-xl shadow-lg text-xs sm:text-sm font-semibold ${bgColors[type] || bgColors.info}`;
  toast.innerHTML = `<span class="w-4 h-4 rounded-full bg-white/20 flex items-center justify-center font-bold text-[11px]">${icons[type] || 'ℹ'}</span><span>${message}</span>`;

  container.appendChild(toast);

  setTimeout(() => {
    toast.classList.add('toast-out');
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// --- QUICK JUMP FROM HERO CARDS ---
function quickJump(tabId, submode) {
  switchTab(tabId);
  if (tabId === 'passport' && submode) {
    setPassportMode(submode);
  } else if (tabId === 'pdf' && submode) {
    setPdfSubMode(submode);
  } else if (tabId === 'ppt' && submode) {
    setPptMode(submode);
  }

  const workspace = document.getElementById('tools-section');
  if (workspace) {
    workspace.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

// --- APPLY EXAM PRESET FROM CHEAT SHEET TABLE ---
function applyExamPreset(preset, targetKb) {
  quickJump('passport', 'single');
  const presetSelect = document.getElementById('passport-preset');
  const kbInput = document.getElementById('passport-target-kb');
  if (presetSelect) presetSelect.value = preset;
  if (kbInput) {
    kbInput.value = targetKb;
    setPassportKB(targetKb);
  }
  showToast(`Exam preset loaded: ${preset} (${targetKb} KB)`, 'success');
}

// --- TAB SWITCHING ---
function switchTab(tabId) {
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.classList.remove('active', 'bg-white', 'text-sky-700', 'shadow-sm');
    btn.classList.add('text-slate-600');
    if (btn.dataset.tab === tabId) {
      btn.classList.add('active', 'bg-white', 'text-sky-700', 'shadow-sm');
      btn.classList.remove('text-slate-600');
    }
  });

  document.querySelectorAll('.tab-content').forEach(panel => {
    panel.classList.add('hidden');
    panel.classList.remove('block');
  });

  const activePanel = document.getElementById(`tab-${tabId}`);
  if (activePanel) {
    activePanel.classList.remove('hidden');
    activePanel.classList.add('block');
  }

  hideResult();
}

// --- SUB-MODE TOGGLES ---
function setPassportMode(mode) {
  currentPassportMode = mode;
  ['single', 'sheet', 'sig'].forEach(m => {
    const btn = document.getElementById(`p-mode-${m}`);
    if (btn) {
      btn.classList.remove('bg-white', 'shadow-xs', 'text-sky-700');
      btn.classList.add('text-slate-600');
    }
  });

  const activeId = mode === 'signature' ? 'p-mode-sig' : `p-mode-${mode}`;
  const activeBtn = document.getElementById(activeId);
  if (activeBtn) {
    activeBtn.classList.add('bg-white', 'shadow-xs', 'text-sky-700');
    activeBtn.classList.remove('text-slate-600');
  }

  const presetGrp = document.getElementById('passport-preset-group');
  const kbGrp = document.getElementById('passport-kb-group');
  const sheetGrp = document.getElementById('passport-sheet-group');
  const btnText = document.getElementById('btn-passport-text');

  if (mode === 'single') {
    presetGrp.classList.remove('hidden');
    kbGrp.classList.remove('hidden');
    sheetGrp.classList.add('hidden');
    btnText.innerText = 'Generate Passport Photo';
  } else if (mode === 'sheet') {
    presetGrp.classList.remove('hidden');
    kbGrp.classList.add('hidden');
    sheetGrp.classList.remove('hidden');
    btnText.innerText = 'Generate Printable Photo Sheet';
  } else if (mode === 'signature') {
    presetGrp.classList.add('hidden');
    kbGrp.classList.remove('hidden');
    sheetGrp.classList.add('hidden');
    btnText.innerText = 'Clean & Sharpen Signature';
  }
}

function setPassportKB(kb) {
  const input = document.getElementById('passport-target-kb');
  const display = document.getElementById('passport-kb-display');
  if (input) input.value = kb;
  if (display) display.innerText = `${kb} KB`;
}

function setCompressKB(kb) {
  const input = document.getElementById('compress-target-kb');
  const display = document.getElementById('compress-kb-indicator');
  if (input) input.value = kb;
  if (display) display.innerText = `${kb} KB`;
}

function setPdfSubMode(mode) {
  currentPdfMode = mode;
  ['img2pdf', 'pdf2img', 'merge', 'split'].forEach(m => {
    const btn = document.getElementById(`pdf-m-${m}`);
    if (btn) {
      btn.classList.remove('bg-white', 'shadow-xs', 'text-sky-700');
      btn.classList.add('text-slate-600');
    }
  });

  const activeBtn = document.getElementById(`pdf-m-${mode}`);
  if (activeBtn) {
    activeBtn.classList.add('bg-white', 'shadow-xs', 'text-sky-700');
    activeBtn.classList.remove('text-slate-600');
  }

  const fileInput = document.getElementById('pdf-file-input');
  const fileLabel = document.getElementById('pdf-file-label');
  const fileSub = document.getElementById('pdf-file-subtext');
  const splitOpts = document.getElementById('pdf-split-options');
  const btnText = document.getElementById('btn-pdf-text');

  splitOpts.classList.add('hidden');

  if (mode === 'img2pdf') {
    fileInput.accept = 'image/*';
    fileInput.multiple = true;
    fileLabel.innerText = 'Select Images for PDF';
    fileSub.innerText = 'Select one or more images (JPG, PNG, WEBP)';
    btnText.innerText = 'Convert Images to PDF';
  } else if (mode === 'pdf2img') {
    fileInput.accept = 'application/pdf';
    fileInput.multiple = false;
    fileLabel.innerText = 'Upload PDF Document';
    fileSub.innerText = 'Extract all pages as high-resolution PNG images';
    btnText.innerText = 'Extract Pages as Images';
  } else if (mode === 'merge') {
    fileInput.accept = 'application/pdf';
    fileInput.multiple = true;
    fileLabel.innerText = 'Select Multiple PDFs to Merge';
    fileSub.innerText = 'Combine multiple PDF documents into one';
    btnText.innerText = 'Merge PDFs into Single File';
  } else if (mode === 'split') {
    fileInput.accept = 'application/pdf';
    fileInput.multiple = false;
    fileLabel.innerText = 'Upload PDF to Split';
    fileSub.innerText = 'Extract specific pages or all pages';
    splitOpts.classList.remove('hidden');
    btnText.innerText = 'Split PDF Document';
  }
}

function setPptMode(mode) {
  currentPptMode = mode;
  ['pdf2ppt', 'img2ppt'].forEach(m => {
    const btn = document.getElementById(`ppt-m-${m}`);
    if (btn) {
      btn.classList.remove('bg-white', 'shadow-xs', 'text-orange-600');
      btn.classList.add('text-slate-600');
    }
  });

  const activeBtn = document.getElementById(`ppt-m-${mode}`);
  if (activeBtn) {
    activeBtn.classList.add('bg-white', 'shadow-xs', 'text-orange-600');
    activeBtn.classList.remove('text-slate-600');
  }

  const fileInput = document.getElementById('ppt-file-input');
  const fileLabel = document.getElementById('ppt-file-label');
  const btnText = document.getElementById('btn-ppt-text');

  if (mode === 'pdf2ppt') {
    fileInput.accept = 'application/pdf';
    fileInput.multiple = false;
    fileLabel.innerText = 'Upload PDF Document';
    btnText.innerText = 'Convert PDF to PPTX';
  } else {
    fileInput.accept = 'image/*';
    fileInput.multiple = true;
    fileLabel.innerText = 'Select Images for Slides';
    btnText.innerText = 'Create PPTX from Images';
  }
}

// --- FILE CLEAR HELPERS ---
function clearPassportFile(e) {
  e.stopPropagation();
  const input = document.getElementById('passport-file-input');
  input.value = '';
  document.getElementById('passport-upload-empty').classList.remove('hidden');
  document.getElementById('passport-upload-loaded').classList.add('hidden');
}

function clearCompressFile(e) {
  e.stopPropagation();
  const input = document.getElementById('compress-file-input');
  input.value = '';
  document.getElementById('compress-upload-empty').classList.remove('hidden');
  document.getElementById('compress-upload-loaded').classList.add('hidden');
}

function clearPdfFiles(e) {
  e.stopPropagation();
  const input = document.getElementById('pdf-file-input');
  input.value = '';
  document.getElementById('pdf-upload-empty').classList.remove('hidden');
  document.getElementById('pdf-upload-loaded').classList.add('hidden');
}

function clearPptFiles(e) {
  e.stopPropagation();
  const input = document.getElementById('ppt-file-input');
  input.value = '';
  document.getElementById('ppt-upload-empty').classList.remove('hidden');
  document.getElementById('ppt-upload-loaded').classList.add('hidden');
}

function clearImageFile(e) {
  e.stopPropagation();
  const input = document.getElementById('image-file-input');
  input.value = '';
  document.getElementById('image-upload-empty').classList.remove('hidden');
  document.getElementById('image-upload-loaded').classList.add('hidden');
}

// --- DROPZONE SETUP WITH THUMBNAIL PREVIEWS ---
function setupAdvancedDropzone(zoneId, inputId, emptyId, loadedId, nameId, sizeId, thumbId) {
  const zone = document.getElementById(zoneId);
  const input = document.getElementById(inputId);
  if (!zone || !input) return;

  zone.addEventListener('click', () => input.click());

  zone.addEventListener('dragover', (e) => {
    e.preventDefault();
    zone.classList.add('dragover');
  });

  zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));

  zone.addEventListener('drop', (e) => {
    e.preventDefault();
    zone.classList.remove('dragover');
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      input.files = e.dataTransfer.files;
      renderFileStatus(input, emptyId, loadedId, nameId, sizeId, thumbId);
    }
  });

  input.addEventListener('change', () => {
    renderFileStatus(input, emptyId, loadedId, nameId, sizeId, thumbId);
  });
}

function renderFileStatus(input, emptyId, loadedId, nameId, sizeId, thumbId) {
  const emptyEl = document.getElementById(emptyId);
  const loadedEl = document.getElementById(loadedId);
  const nameEl = document.getElementById(nameId);
  const sizeEl = document.getElementById(sizeId);
  const thumbEl = thumbId ? document.getElementById(thumbId) : null;

  if (!input.files || input.files.length === 0) {
    if (emptyEl) emptyEl.classList.remove('hidden');
    if (loadedEl) loadedEl.classList.add('hidden');
    return;
  }

  const f = input.files[0];
  const sizeKb = Math.round(f.size / 1024);
  const sizeStr = sizeKb > 1024 ? `${(sizeKb / 1024).toFixed(1)} MB` : `${sizeKb} KB`;

  if (nameEl) {
    nameEl.innerText = input.files.length === 1 ? f.name : `${input.files.length} files selected`;
  }
  if (sizeEl) sizeEl.innerText = sizeStr;

  if (thumbEl && f.type.startsWith('image/')) {
    const reader = new FileReader();
    reader.onload = (e) => { thumbEl.src = e.target.result; };
    reader.readAsDataURL(f);
  }

  if (emptyEl) emptyEl.classList.add('hidden');
  if (loadedEl) loadedEl.classList.remove('hidden');
}

// Initialize all dropzones
setupAdvancedDropzone('passport-dropzone', 'passport-file-input', 'passport-upload-empty', 'passport-upload-loaded', 'passport-loaded-name', 'passport-loaded-size', 'passport-input-thumb');
setupAdvancedDropzone('compress-dropzone', 'compress-file-input', 'compress-upload-empty', 'compress-upload-loaded', 'compress-loaded-name', 'compress-loaded-size');
setupAdvancedDropzone('pdf-dropzone', 'pdf-file-input', 'pdf-upload-empty', 'pdf-upload-loaded', 'pdf-loaded-name', 'pdf-loaded-size');
setupAdvancedDropzone('ppt-dropzone', 'ppt-file-input', 'ppt-upload-empty', 'ppt-upload-loaded', 'ppt-loaded-name', 'ppt-loaded-size');
setupAdvancedDropzone('image-dropzone', 'image-file-input', 'image-upload-empty', 'image-upload-loaded', 'image-loaded-name', 'image-loaded-size', 'image-input-thumb');

// --- RESULT & LOADING HELPERS ---
function showLoading(msg = 'Processing your file...') {
  document.getElementById('loading-text').innerText = msg;
  document.getElementById('loading-overlay').classList.remove('hidden');
  document.getElementById('result-card').classList.add('hidden');
}

function hideLoading() {
  document.getElementById('loading-overlay').classList.add('hidden');
}

function hideResult() {
  document.getElementById('result-card').classList.add('hidden');
}

function showResult(blob, filename, title = 'Done!', details = '', origBytes = null) {
  hideLoading();
  const resultCard = document.getElementById('result-card');
  const dlBtn = document.getElementById('result-download-btn');
  const printBtn = document.getElementById('result-print-btn');
  const titleEl = document.getElementById('result-title');
  const detailsEl = document.getElementById('result-details');
  const previewContainer = document.getElementById('result-preview-container');
  const previewImg = document.getElementById('result-preview-img');
  const savingsBadge = document.getElementById('result-savings-badge');

  const fileUrl = URL.createObjectURL(blob);
  dlBtn.href = fileUrl;
  dlBtn.download = filename;
  titleEl.innerText = title;
  detailsEl.innerText = details || `File size: ${Math.round(blob.size / 1024)} KB`;

  // Savings calculation
  if (origBytes && origBytes > blob.size) {
    const savedPct = Math.round((1 - (blob.size / origBytes)) * 100);
    savingsBadge.innerText = `-${savedPct}% Smaller`;
    savingsBadge.classList.remove('hidden');
  } else {
    savingsBadge.classList.add('hidden');
  }

  // If image or sheet, show preview and enable print
  if (blob.type.startsWith('image/')) {
    previewImg.src = fileUrl;
    previewContainer.classList.remove('hidden');
    printBtn.classList.remove('hidden');
  } else {
    previewContainer.classList.add('hidden');
    printBtn.classList.add('hidden');
  }

  resultCard.classList.remove('hidden');
  resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  showToast(title, 'success');
}

function printOutput() {
  window.print();
}

function getFilenameFromHeaders(response, fallback) {
  const disposition = response.headers.get('Content-Disposition');
  if (disposition && disposition.includes('filename=')) {
    const match = disposition.match(/filename="?([^";]+)"?/);
    if (match && match[1]) return match[1];
  }
  return fallback;
}

// --- API ACTIONS ---

// 1. Passport Actions
async function processPassport() {
  const fileInput = document.getElementById('passport-file-input');
  if (!fileInput.files || fileInput.files.length === 0) {
    showToast('Kripya pehle photo select karein!', 'error');
    return;
  }

  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append('file', file);

  let endpoint = '/api/passport/single';
  let defaultFilename = 'passport_photo.jpg';

  if (currentPassportMode === 'single') {
    const preset = document.getElementById('passport-preset').value;
    const targetKb = document.getElementById('passport-target-kb').value;
    formData.append('preset', preset);
    formData.append('target_kb', targetKb);
    formData.append('add_border', 'true');
    formData.append('border_color', '#000000');
    formData.append('border_width', '2');
    showLoading('Cropping & sizing passport photo to exact KB...');
  } else if (currentPassportMode === 'sheet') {
    endpoint = '/api/passport/sheet';
    const sheetType = document.getElementById('passport-sheet-type').value;
    const preset = document.getElementById('passport-preset').value;
    const count = document.getElementById('passport-sheet-count').value;
    formData.append('sheet_type', sheetType);
    formData.append('preset', preset);
    formData.append('photo_count', count);
    defaultFilename = `passport_sheet_${count}photos.jpg`;
    showLoading(`Arranging ${count} passport photos on ${sheetType} sheet...`);
  } else if (currentPassportMode === 'signature') {
    endpoint = '/api/passport/signature';
    const targetKb = document.getElementById('passport-target-kb').value;
    formData.append('target_kb', targetKb);
    defaultFilename = 'cleaned_signature.jpg';
    showLoading('Cleaning paper background & sharpening ink...');
  }

  try {
    const res = await fetch(endpoint, { method: 'POST', body: formData });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Processing failed');
    }
    const blob = await res.blob();
    const finalKb = res.headers.get('X-Final-Size-KB') || Math.round(blob.size / 1024);
    const filename = getFilenameFromHeaders(res, defaultFilename);
    showResult(blob, filename, 'Passport Photo Ready!', `Processed size: ${finalKb} KB. Formatted for official forms.`, file.size);
  } catch (e) {
    hideLoading();
    showToast('Error: ' + e.message, 'error');
  }
}

// 2. Exact KB Compressor Action
async function processCompress() {
  const fileInput = document.getElementById('compress-file-input');
  if (!fileInput.files || fileInput.files.length === 0) {
    showToast('Kripya image ya PDF file upload karein!', 'error');
    return;
  }

  const file = fileInput.files[0];
  const targetKb = document.getElementById('compress-target-kb').value;
  const formData = new FormData();
  formData.append('file', file);
  formData.append('target_kb', targetKb);

  const isPdf = file.type === 'application/pdf' || file.name.endsWith('.pdf');
  const endpoint = isPdf ? '/api/compress/pdf' : '/api/compress/image';

  showLoading(`Compressing to under ${targetKb} KB...`);

  try {
    const res = await fetch(endpoint, { method: 'POST', body: formData });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Compression failed');
    }
    const blob = await res.blob();
    const finalKb = res.headers.get('X-Final-Size-KB') || Math.round(blob.size / 1024);
    const origKb = Math.round(file.size / 1024);
    const filename = getFilenameFromHeaders(res, `compressed_${finalKb}kb_${file.name}`);
    
    showResult(blob, filename, 'Compression Successful!', `Original: ${origKb} KB ➔ Compressed: ${finalKb} KB (Target: ${targetKb} KB)`, file.size);
  } catch (e) {
    hideLoading();
    showToast('Error: ' + e.message, 'error');
  }
}

// 3. PDF Tools Action
async function processPdf() {
  const fileInput = document.getElementById('pdf-file-input');
  if (!fileInput.files || fileInput.files.length === 0) {
    showToast('Kripya files select karein!', 'error');
    return;
  }

  const formData = new FormData();
  let endpoint = '';
  let defaultFilename = 'document.pdf';

  if (currentPdfMode === 'img2pdf') {
    endpoint = '/api/pdf/images-to-pdf';
    for (let f of fileInput.files) {
      formData.append('files', f);
    }
    defaultFilename = 'converted_document.pdf';
    showLoading(`Converting ${fileInput.files.length} images to unified PDF...`);
  } else if (currentPdfMode === 'pdf2img') {
    endpoint = '/api/pdf/pdf-to-images';
    formData.append('file', fileInput.files[0]);
    formData.append('dpi', '150');
    defaultFilename = 'pdf_pages.zip';
    showLoading('Rendering and extracting pages as PNG images...');
  } else if (currentPdfMode === 'merge') {
    endpoint = '/api/pdf/merge';
    for (let f of fileInput.files) {
      formData.append('files', f);
    }
    defaultFilename = 'merged_document.pdf';
    showLoading(`Merging ${fileInput.files.length} PDF files...`);
  } else if (currentPdfMode === 'split') {
    endpoint = '/api/pdf/split';
    formData.append('file', fileInput.files[0]);
    const range = document.getElementById('pdf-split-range').value;
    formData.append('page_selection', range);
    defaultFilename = 'split_pages.zip';
    showLoading('Splitting PDF pages...');
  }

  try {
    const res = await fetch(endpoint, { method: 'POST', body: formData });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'PDF processing failed');
    }
    const blob = await res.blob();
    const filename = getFilenameFromHeaders(res, defaultFilename);
    showResult(blob, filename, 'PDF Processing Complete!', `Saved as ${filename}`);
  } catch (e) {
    hideLoading();
    showToast('Error: ' + e.message, 'error');
  }
}

// 4. PPT Tools Action
async function processPpt() {
  const fileInput = document.getElementById('ppt-file-input');
  if (!fileInput.files || fileInput.files.length === 0) {
    showToast('Kripya file select karein!', 'error');
    return;
  }

  const formData = new FormData();
  let endpoint = '';
  let defaultFilename = 'presentation.pptx';

  if (currentPptMode === 'pdf2ppt') {
    endpoint = '/api/ppt/pdf-to-pptx';
    formData.append('file', fileInput.files[0]);
    showLoading('Converting PDF pages to PowerPoint slides...');
  } else {
    endpoint = '/api/ppt/images-to-pptx';
    for (let f of fileInput.files) {
      formData.append('files', f);
    }
    formData.append('aspect_ratio', '16:9');
    showLoading(`Building PPTX presentation from ${fileInput.files.length} images...`);
  }

  try {
    const res = await fetch(endpoint, { method: 'POST', body: formData });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'PPT conversion failed');
    }
    const blob = await res.blob();
    const filename = getFilenameFromHeaders(res, defaultFilename);
    showResult(blob, filename, 'PowerPoint Presentation Ready!', `Presentation generated: ${filename}`);
  } catch (e) {
    hideLoading();
    showToast('Error: ' + e.message, 'error');
  }
}

// 5. Image Format Convert
async function processImageConvert() {
  const fileInput = document.getElementById('image-file-input');
  if (!fileInput.files || fileInput.files.length === 0) {
    showToast('Kripya image select karein!', 'error');
    return;
  }

  const file = fileInput.files[0];
  const targetFmt = document.getElementById('image-target-format').value;
  const quality = document.getElementById('image-quality').value;

  const formData = new FormData();
  formData.append('file', file);
  formData.append('target_format', targetFmt);
  formData.append('quality', quality);

  showLoading(`Converting image to ${targetFmt}...`);

  try {
    const res = await fetch('/api/image/convert', { method: 'POST', body: formData });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Conversion failed');
    }
    const blob = await res.blob();
    const filename = getFilenameFromHeaders(res, `converted.${targetFmt.toLowerCase()}`);
    showResult(blob, filename, 'Image Converted!', `Format: ${targetFmt.toUpperCase()} (${Math.round(blob.size / 1024)} KB)`, file.size);
  } catch (e) {
    hideLoading();
    showToast('Error: ' + e.message, 'error');
  }
}

// --- PWA INSTALLATION & SERVICE WORKER ---
let deferredPrompt = null;
const pwaBtn = document.getElementById('pwa-install-btn');

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/service-worker.js')
      .then((reg) => console.log('PWA ServiceWorker registered:', reg.scope))
      .catch((err) => console.log('ServiceWorker registration failed:', err));
  });
}

window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  if (pwaBtn) {
    pwaBtn.classList.remove('hidden');
    pwaBtn.classList.add('inline-flex');
  }
});

if (pwaBtn) {
  pwaBtn.addEventListener('click', async () => {
    if (deferredPrompt) {
      deferredPrompt.prompt();
      const { outcome } = await deferredPrompt.userChoice;
      console.log(`User response to install prompt: ${outcome}`);
      deferredPrompt = null;
      pwaBtn.classList.add('hidden');
    } else {
      showToast('To install: On Android tap 3 dots ➔ "Install App". On iPhone tap Share ➔ "Add to Home Screen"', 'info');
    }
  });
}

window.addEventListener('appinstalled', () => {
  showToast('OmniConvert installed successfully!', 'success');
  if (pwaBtn) pwaBtn.classList.add('hidden');
});
