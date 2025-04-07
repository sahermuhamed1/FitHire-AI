import pdfminer.high_level
import docx2txt
import os

class ResumeParser:
    @staticmethod
    def extract_text(file_path):
        file_extension = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_extension == '.pdf':
                return pdfminer.high_level.extract_text(file_path)
            elif file_extension == '.docx':
                return docx2txt.process(file_path)
            elif file_extension == '.txt':
                with open(file_path, 'r', encoding='utf-8') as file:
                    return file.read()
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
        except Exception as e:
            raise Exception(f"Error extracting text from file: {str(e)}")