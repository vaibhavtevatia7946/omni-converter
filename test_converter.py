import io
import os
import unittest
from PIL import Image
import fitz

from utils.compressor import compress_image_to_target_kb, compress_pdf_to_target_kb
from utils.passport import create_passport_photo, create_passport_sheet, enhance_signature
from utils.pdf_tools import images_to_pdf, pdf_to_images, merge_pdfs, split_pdf
from utils.ppt_tools import images_to_pptx, pdf_to_pptx
from utils.image_converter import convert_image_format

class TestOmniConverter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a sample test image in memory
        img = Image.new("RGB", (800, 1000), color=(120, 180, 240))
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=95)
        cls.test_img_bytes = buf.getvalue()

        # Create a sample test PDF in memory
        doc = fitz.open()
        p1 = doc.new_page()
        p1.insert_text((50, 72), "OmniConvert Sample Test Page 1")
        p2 = doc.new_page()
        p2.insert_text((50, 72), "OmniConvert Sample Test Page 2")
        pdf_buf = io.BytesIO()
        doc.save(pdf_buf)
        doc.close()
        cls.test_pdf_bytes = pdf_buf.getvalue()

    def test_image_compression(self):
        target = 40
        out_bytes, final_kb, w, h = compress_image_to_target_kb(self.test_img_bytes, target_kb=target)
        self.assertLessEqual(final_kb, target)
        self.assertGreater(final_kb, 0)
        print(f"✓ Image compression test passed: {final_kb} KB <= {target} KB")

    def test_passport_photo(self):
        target_kb = 35
        out_bytes, w, h, final_kb = create_passport_photo(
            self.test_img_bytes, preset="india_standard", target_kb=target_kb
        )
        self.assertEqual(w, 413)
        self.assertEqual(h, 531)
        self.assertLessEqual(final_kb, target_kb)
        print(f"✓ Passport photo test passed: {w}x{h} px, {final_kb} KB")

    def test_passport_sheet(self):
        sheet_bytes, sw, sh = create_passport_sheet(self.test_img_bytes, sheet_type="4x6", photo_count=8)
        self.assertEqual(sw, 1800)
        self.assertEqual(sh, 1200)
        self.assertGreater(len(sheet_bytes), 1000)
        print(f"✓ Passport sheet test passed: {sw}x{sh} px sheet created")

    def test_signature_enhancer(self):
        sig_bytes, kb, w, h = enhance_signature(self.test_img_bytes, target_kb=15)
        self.assertLessEqual(kb, 15)
        print(f"✓ Signature enhancer test passed: {kb} KB <= 15 KB")

    def test_pdf_tools(self):
        # Images to PDF
        pdf_bytes = images_to_pdf([self.test_img_bytes])
        self.assertGreater(len(pdf_bytes), 100)

        # PDF to images
        extracted_pages = pdf_to_images(self.test_pdf_bytes)
        self.assertEqual(len(extracted_pages), 2)

        # PDF merge
        merged = merge_pdfs([self.test_pdf_bytes, pdf_bytes])
        merged_doc = fitz.open(stream=merged, filetype="pdf")
        self.assertEqual(len(merged_doc), 3)

        # PDF split
        splits = split_pdf(self.test_pdf_bytes, page_selection="1")
        self.assertEqual(len(splits), 1)
        print("✓ All PDF manipulation tests passed")

    def test_ppt_tools(self):
        # PDF to PPTX
        pptx_bytes = pdf_to_pptx(self.test_pdf_bytes)
        self.assertGreater(len(pptx_bytes), 1000)

        # Images to PPTX
        img_pptx = images_to_pptx([self.test_img_bytes])
        self.assertGreater(len(img_pptx), 1000)
        print("✓ All PPT manipulation tests passed")

    def test_format_convert(self):
        png_bytes, ext = convert_image_format(self.test_img_bytes, target_format="PNG")
        self.assertEqual(ext, "png")
        self.assertGreater(len(png_bytes), 1000)
        print("✓ Image format conversion test passed")

if __name__ == "__main__":
    unittest.main()
