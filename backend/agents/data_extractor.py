# agents/data_extractor.py
from PIL import Image
import io
import os
import fitz
import easyocr


def extract_text_from_pdf(uploaded_file):
    """
    Extract text from PDF using PyMuPDF (NO POPPLER REQUIRED).
    uploaded_file can be:
       - a file path
       - an UploadedFile object (Streamlit / Django)
    """
    try:
        # If it's an UploadedFile object, read bytes
        if hasattr(uploaded_file, "read"):
            pdf_bytes = uploaded_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        else:
            doc = fitz.open(uploaded_file)

        text = ""
        for page in doc:
            text += page.get_text()

        return text.strip()

    except Exception as e:
        raise RuntimeError(f"PDF Extraction Error: {e}")

reader = easyocr.Reader(['en'])


def extract_text_from_image(uploaded_file):
    """
    Extract text from images using EasyOCR.
    Supports UploadedFile objects and file paths.
    """
    try:
        if hasattr(uploaded_file, "read"):
            # UploadedFile object → convert to bytes → Pillow image
            import numpy as np
            from PIL import Image
            file_bytes = uploaded_file.read()
            image = Image.open(io.BytesIO(file_bytes))
            image_np = np.array(image)
        else:
            image_np = uploaded_file  # file path or numpy array

        result = reader.readtext(image_np, detail=0)
        return "\n".join(result)

    except Exception as e:
        raise RuntimeError(f"Image OCR Error: {e}")
    


