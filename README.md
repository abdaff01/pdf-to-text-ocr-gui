# PDF-to-Text OCR Converter (GUI)

Tkinter GUI that converts a PDF into a `.txt` file by rendering PDF pages to images
and extracting text via Tesseract OCR.

## Features
- Select a source PDF
- Select a destination folder
- Converts PDF pages to text and saves a `.txt` file

## Requirements
- Python 3.9+ recommended
- Tesseract OCR installed
- Poppler installed (needed by pdf2image)

## Install (Python deps)
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
