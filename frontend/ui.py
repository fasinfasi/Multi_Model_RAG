import streamlit as st
import sys
import os

folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"../backend"))
sys.path.append(folder_path)

import importlib
from file_loader import assign_doc

st.set_page_config(layout='centered', page_title='Multi-Model RAG')

st.title("📝Multi-Model RAG System💻")
document = st.file_uploader("Drop your pdf doc here!", type='pdf')
query = st.text_input("Ask Your questions here...")
btn = st.button("Ask")

if btn:
    if document and query:
        st.info("Document under analysing process, ⏱️Please wait...")

        # Save uploaded file to project-level directory
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        uploads_dir = os.path.join(project_root, "uploads")
        os.makedirs(uploads_dir, exist_ok=True)

        filename = getattr(document, "name", "uploaded_document.pdf")
        upload_path = os.path.join(uploads_dir, filename)
        with open(upload_path, "wb") as f:
            f.write(document.read())

        # Tell backend `file_loader` which file to use (it will read from uploads)
        assign_doc(filename)

        # Clear cached backend modules so they re-import with the new document
        # (keep `file_loader` loaded so its `pdf_path` remains set)
        for m in ("response", "embedding", "vector_store"):
            if m in sys.modules:
                del sys.modules[m]

        response = importlib.import_module("response")
        res = response.query_rag(query)
        st.subheader("✅Answer:")
        st.write(res)
        
        
