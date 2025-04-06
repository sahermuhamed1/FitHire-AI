import os
from pdfminer.high_level import extract_text as extract_text_pdf
import docx2txt

def extract_text_from_pdf(file_path):
    """Extract text from PDF files using pdfminer.six"""
    try:
        return extract_text_pdf(file_path)
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def extract_text_from_docx(file_path):
    """Extract text from DOCX files using docx2txt"""
    try:
        return docx2txt.process(file_path)
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return ""
        
def extract_text(file_path):
    """Extract text from a file based on its extension"""
    _, ext = os.path.splitext(file_path)
    
    if ext.lower() == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext.lower() == '.docx':
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")