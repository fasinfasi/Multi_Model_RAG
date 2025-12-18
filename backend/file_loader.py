import os
import pdfplumber
import camelot
import logging
import fitz
# from pdf2image import convert_from_path
# import pytesseract

logging.getLogger("pdfminer").setLevel(logging.ERROR) # avoid warning

document = 'qatar_test_doc.pdf'

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
print(BASE_DIR)

pdf_path = os.path.join(BASE_DIR, document)

#================= Text Extraction ===================
def extract_text(pdf_path):
    print('text extracting')
    text_blocks = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_no, page in enumerate(pdf.pages):
            text_blocks.append(
                {
                    "page": page_no,
                    "type": "text",
                    "content": page.extract_text()
                }
            )
    return text_blocks

# print(f"{extract_text(pdf_path)}\n\n")

#================ Table Extraction =============
def extract_tables(pdf_path):
    print('table extracting')
    tables = camelot.read_pdf(pdf_path, pages='all')
    results = []

    for i, table in enumerate(tables):
        results.append(
            {
                "type": "table",
                "page": table.page,
                "content": table.df.to_dict()
            }
        )
    return results

# print(f"{extract_tables(pdf_path)}\n\n")

#================== Image Extraction ===============
def extract_images(pdf_path):
    print('image extracting')
    doc = fitz.open(pdf_path)
    images = []

    for page_index in range(len(doc)):
        page = doc[page_index]
        for img in page.get_images(full=True):
            xref = img[0]
            image = doc.extract_image(xref)

            images.append({
                "page": page_index,
                "type": "image",
                "image_bytes": image["image"],
                "format": image["ext"]
            })
    return images

# print(extract_images(pdf_path))

#===================== OCR Text Extraction =====================
# poppler_path = r"C:\Program Files\poppler-25.12.0\Library\bin"
# pytesseract.pytesseract.tesseract_cmd = r"C:\Users\HP\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# def extract_ocr(pdf_path):
#     pages = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)
#     ocr_text = []

#     for i, page in enumerate(pages):
#         text = pytesseract.image_to_string(page)
#         if text.strip():
#             ocr_text.append({
#                 "page": i,
#                 "type": "ocr_text",
#                 "content": text
#             })

#     return ocr_text

# print(extract_ocr(pdf_path))

