import pdfplumber
from docx import Document
from io import BytesIO

def extract_text_from_file(file_bytes, filename):
    """
    Extract text from uploaded file (PDF, DOCX, TXT)
    file_bytes: BytesIO object
    filename: original filename to determine type
    """
    import os
    ext = os.path.splitext(filename)[1].lower()
    text = ""
    
    if ext == ".pdf":
        try:
            with pdfplumber.open(file_bytes) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"PDF extraction error: {e}")
            return None
    elif ext in [".docx"]:
        try:
            doc = Document(file_bytes)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            print(f"DOCX extraction error: {e}")
            return None
    elif ext in [".txt"]:
        try:
            text = file_bytes.getvalue().decode("utf-8")
        except Exception as e:
            print(f"TXT extraction error: {e}")
            return None
    else:
        return None  # unsupported file type

    return text
