import pdfplumber


def parse_pdf(file):
    """
    Opens a PDF and extracts text from every page.

    Args:
        file: Uploaded file object from Streamlit's st.file_uploader.

    Returns:
        List of dicts with 'page' (1-based) and 'text' keys.
        Empty pages or image-only pages are silently skipped.
    """
    pages = []
    with pdfplumber.open(file) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text and text.strip():
                pages.append({"page": i + 1, "text": text})
    return pages
