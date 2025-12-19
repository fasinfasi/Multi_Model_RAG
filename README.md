# Multi-Model RAG System

A comprehensive Retrieval-Augmented Generation (RAG) system that extracts and processes multiple content types from PDF documents (text, tables, images, and OCR text) to provide accurate, context-aware answers using advanced embedding techniques and vector similarity search.

## Project Overview

The Multi-Model RAG System is designed to intelligently process PDF documents by extracting various content types including:
- **Text content** from PDF pages
- **Tables** with structured data
- **Images** embedded in documents
- **OCR text** from scanned pages

The system uses sentence transformers to create embeddings, builds a FAISS vector index for efficient similarity search, and leverages OpenAI's GPT models to generate contextually grounded answers based on retrieved document chunks.

## Installation Instructions

### Prerequisites

- **Python 3.9+** (Python 3.12 recommended)
- **Windows OS** (current implementation optimized for Windows)
- **System Dependencies:**
  - [Poppler](https://github.com/oschwartz10612/poppler-windows/releases/) - Required for PDF to image conversion
  - [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) - Required for OCR text extraction
  - OpenAI API key

### Step-by-Step Setup

1. **Clone the repository**
   ```powershell
   git clone https://github.com/fasinfasi/Multi_Model_RAG.git
   cd Multi_Model_RAG
   ```

2. **Create and activate virtual environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install Python dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure system dependencies**
   
   Edit `backend/file_loader.py` and update the paths if your installations differ:
   ```python
   poppler_path = r"C:\Program Files\poppler-25.12.0\Library\bin"
   pytesseract.pytesseract.tesseract_cmd = r"C:\Users\HP\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
   ```

5. **Set environment variables**
   
   **PowerShell:**
   ```powershell
   $env:OPENAI_API_KEY = "your_openai_api_key_here"
   ```
   
   **Command Prompt:**
   ```cmd
   set OPENAI_API_KEY=your_openai_api_key_here
   ```
   
   **Alternative:** Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage Guide

### Running the Streamlit UI (Recommended)

The easiest way to interact with the system is through the web-based Streamlit interface:

```powershell
streamlit run frontend/ui.py
```

The application will open in your default browser (typically at `http://localhost:8501`).

**Usage Steps:**
1. Upload a PDF document using the file uploader
2. Enter your question in the text input field
3. Click the "Ask" button
4. Wait for the system to process and analyze the document
5. Review the generated answer

### Command-Line Interface

For programmatic or interactive use, you can run the response module directly:

```powershell
python -m backend.response
```

This launches an interactive CLI where you can:
- Enter queries directly
- Type `exit` to quit
- Receive answers based on the currently loaded document

## Folder & File Structure

```
Multi_Model_RAG/
│
├── backend/                    # Core processing modules
│   ├── __init__.py            # Package initializer
│   ├── file_loader.py         # PDF extraction (text, tables, images, OCR)
│   ├── embedding.py           # Sentence transformer embeddings
│   ├── vector_store.py        # FAISS index creation and management
│   └── response.py            # RAG query processing and OpenAI integration
│
├── frontend/                   # User interface
│   ├── __init__.py            # Package initializer
│   └── ui.py                  # Streamlit web application
│
├── uploads/                   # Directory for uploaded PDF files
│
├── venv/                      # Virtual environment (gitignored)
│
├── requirements.txt           # Python package dependencies
└── README.md                  # Project documentation
```

### Key Files Description

- **`backend/file_loader.py`**: Handles PDF document ingestion and multi-modal content extraction (text, tables, images, OCR). Manages file uploads and sets global document paths.

- **`backend/embedding.py`**: Creates embeddings using SentenceTransformer (`paraphrase-MiniLM-L6-v2`). Processes all extracted chunks and prepares them for vector indexing.

- **`backend/vector_store.py`**: Builds and manages the FAISS (Facebook AI Similarity Search) index for efficient k-nearest neighbor search over document embeddings.

- **`backend/response.py`**: Implements the RAG pipeline: converts queries to embeddings, retrieves relevant chunks, constructs context, and queries OpenAI GPT-4.1-mini for answer generation.

- **`frontend/ui.py`**: Streamlit-based web interface for document upload and query interaction. Handles file management and module reloading for dynamic document processing.

## Dependencies

### Python Packages

All dependencies are listed in `requirements.txt`:

```
pdfplumber==0.11.8          # PDF text extraction
camelot-py==1.0.9           # Table extraction from PDFs
pymupdf==1.26.7             # PDF image extraction (PyMuPDF)
pdf2image==1.17.0           # PDF to image conversion
pytesseract==0.3.13         # OCR text extraction
pandas                      # Data manipulation (used by Camelot)
python-dotenv               # Environment variable management
openai                      # OpenAI API client
sentence_transformers       # Embedding model framework
faiss-cpu                   # Vector similarity search index
numpy                       # Numerical operations
streamlit                   # Web UI framework
```

### System Dependencies

- **Poppler**: PDF rendering library (Windows binaries available)
- **Tesseract OCR**: Optical Character Recognition engine
- **OpenAI API Access**: Valid API key with GPT-4.1-mini access

## Additional Notes

### Environment Variables

- **`OPENAI_API_KEY`**: Required. Your OpenAI API key for GPT model access. Set via environment variable or `.env` file.

### Configuration

**Windows Path Configuration:**
- Update `poppler_path` in `backend/file_loader.py` (line ~131) to match your Poppler installation
- Update `pytesseract.pytesseract.tesseract_cmd` in `backend/file_loader.py` (line ~133) to match your Tesseract installation

### Performance Considerations

- **Large Documents**: The current implementation processes embeddings at import time. For very large PDFs (>100 pages), consider:
  - Implementing lazy loading for embeddings
  - Using background processing for extraction
  - Implementing chunking strategies for memory management

- **Model Loading**: The SentenceTransformer model (`paraphrase-MiniLM-L6-v2`) is loaded once per session. First query may take longer due to model initialization.

- **API Costs**: Each query uses OpenAI's API. Monitor usage to manage costs, especially with high-volume queries.

### Best Practices

1. **Document Preparation**: Ensure PDFs are readable and not corrupted for best extraction results
2. **Query Formulation**: Ask specific, clear questions for more accurate answers
3. **File Management**: Regularly clean the `uploads/` directory to manage disk space
4. **API Key Security**: Never commit API keys to version control. Use environment variables or `.env` files (add `.env` to `.gitignore`)

### Troubleshooting

**Common Issues:**

- **"Module not found" errors**: Ensure virtual environment is activated and dependencies are installed
- **Poppler/Tesseract errors**: Verify paths in `backend/file_loader.py` match your installations
- **OpenAI API errors**: Check API key is set correctly and account has sufficient credits
- **Memory errors**: Reduce document size or implement chunking for very large PDFs

### Development Notes

- The frontend dynamically reloads backend modules when new documents are uploaded
- Embeddings are computed synchronously; consider async processing for production use
- FAISS index is built in-memory; for persistent storage, implement index serialization

## Contributing

Contributions are welcome! Please ensure:
- Code follows existing style and structure
- New features maintain modularity (ingestion, retrieval, answer generation)
- Tests are added for new functionality
- Documentation is updated accordingly
