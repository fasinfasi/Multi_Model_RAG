import os
import pdfplumber
import camelot
import logging
import fitz
from pdf2image import convert_from_path
import pytesseract

logging.getLogger("pdfminer").setLevel(logging.ERROR) # avoid warning

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
print(BASE_DIR)

# Module-level document filename and full path. These are set by `assign_doc()`
# after a user uploads a file from the UI. They remain `None` until assignment.
document = None
pdf_path = None


def assign_doc(uploaded_file):
    """
    Save the uploaded file to the backend directory and set the module-level
    `document` (filename) and `pdf_path` (absolute path).

    `uploaded_file` can be a Streamlit `UploadedFile` (has `.read()` and
    `.name`) or a filesystem path string. The function returns the saved
    `pdf_path`.
    """
    global document, pdf_path

    uploads_dir = os.path.join(BASE_DIR, "uploads")
    os.makedirs(uploads_dir, exist_ok=True)

    # If an UploadedFile-like object is passed, save it into uploads
    if hasattr(uploaded_file, "read"):
        filename = getattr(uploaded_file, "name", "uploaded_document.pdf")
        target_path = os.path.join(uploads_dir, filename)
        with open(target_path, "wb") as f:
            f.write(uploaded_file.read())

    else:
        # Assume a filename or path string was provided. If it's a bare
        # filename, assume it's located inside uploads_dir; if it's a
        # path, use it (copy into uploads if it's outside uploads_dir).
        provided = str(uploaded_file)
        provided_path = os.path.abspath(provided)
        if os.path.dirname(provided_path) == uploads_dir:
            target_path = provided_path
            filename = os.path.basename(provided_path)
        else:
            # Copy into uploads_dir
            import shutil
            filename = os.path.basename(provided_path)
            target_path = os.path.join(uploads_dir, filename)
            shutil.copy(provided_path, target_path)

    document = filename
    pdf_path = target_path

    return pdf_path

#================= Text Extraction ===================
def extract_text(pdf_path):
    print('text extracting...')
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
    print('table extracting...')
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
    print('image extracting...')
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
poppler_path = r"C:\Program Files\poppler-25.12.0\Library\bin"
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\HP\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def extract_ocr(pdf_path):
    print("OCR extracting...")
    pages = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)
    ocr_text = []

    for i, page in enumerate(pages):
        text = pytesseract.image_to_string(page)
        if text.strip():
            ocr_text.append({
                "page": i,
                "type": "ocr_text",
                "content": text
            })

    return ocr_text

# print(extract_ocr(pdf_path))
