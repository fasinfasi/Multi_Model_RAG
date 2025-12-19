"""Create embeddings from extracted document content.

Notes:
- This module expects `backend.file_loader.assign_doc()` to have been
  called (so `backend.file_loader.pdf_path` is set) before importing in
  typical usage from the frontend UI.
- The module loads a SentenceTransformer model and computes embeddings
  for all extracted chunks at import time. Keep in mind this may be
  expensive for large documents.
"""

import file_loader as loader
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

# Lightweight embedding model used by the project
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

pdf_path = loader.pdf_path

text_blocks = loader.extract_text(pdf_path)
table_blocks = loader.extract_tables(pdf_path)
image_blocks = loader.extract_images(pdf_path)
ocr_blocks = loader.extract_ocr(pdf_path)

chunks = text_blocks + table_blocks + image_blocks + ocr_blocks

def chunk_to_text(chunk):
    if chunk['type'] in ['text', 'table', 'ocr_text']:
        return chunk['content']
    elif chunk['type'] == 'image':
        return f"[Figure at page {chunk['page']}]"
    else:
        return ""
    
texts_for_index = [chunk_to_text(chunk) for chunk in chunks]

def get_embeddings(text):
    return model.encode(text)

embeddings = [get_embeddings(text) for text in texts_for_index]

# Map index back to original chunk for retrieval
index_to_chunk = {i: chunks[i] for i in range(len(chunks))}

