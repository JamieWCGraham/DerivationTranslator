"""PDF text extraction using PyMuPDF."""

from __future__ import annotations

import io

import pymupdf


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract text from an uploaded PDF file.

    Args:
        uploaded_file: A file-like object (e.g. Streamlit UploadedFile) with .read() and .name.

    Returns:
        Concatenated text from all pages, with spacing preserved for readability.

    Raises:
        ValueError: If the file cannot be opened or parsed as a PDF.
    """
    if uploaded_file is None:
        raise ValueError("No file provided.")

    raw = uploaded_file.read()
    if not raw:
        raise ValueError("The uploaded file is empty.")

    try:
        doc = pymupdf.open(stream=raw, filetype="pdf")
    except Exception as e:
        raise ValueError(f"Cannot open PDF: {e}") from e

    try:
        parts = []
        for page in doc:
            text = page.get_text()
            if text.strip():
                parts.append(text)
            # Preserve page separation with a newline for readability
            parts.append("\n")
        doc.close()
        result = "\n".join(p.strip() for p in parts if p.strip()) if parts else ""
        return result.strip() or "(No text extracted from PDF.)"
    except Exception as e:
        if "doc" in dir():
            doc.close()
        raise ValueError(f"Error extracting text from PDF: {e}") from e
