from fastapi import  UploadFile
from docx import Document
import win32com.client

import fitz

class ExtractTextFromFile:

    def pdf(file: UploadFile) -> str:
        text = ""
        try:
            with fitz.open(stream=file.file.read(), filetype="pdf") as doc:
                for page in doc:
                    text += page.get_text("text") + "\n"
        except Exception as e:
            raise Exception("Problem during extracting text from pdf file") 
        return text.strip()

    def docx(file) -> str:
        try:
            file.file.seek(0)  
            doc = Document(file.file)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text.strip()
        except Exception as e:
            raise Exception(f"Error during extracting text from .docx: {str(e)}")

    def doc(file) -> str:
        try:
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = False
            doc = word.Documents.Open(file.file.name) 
            text = doc.Content.Text
            doc.Close()
            word.Quit()
            return text.strip()
        except Exception as e:
            raise Exception(f"Error during extracting text from .doc: {str(e)}")