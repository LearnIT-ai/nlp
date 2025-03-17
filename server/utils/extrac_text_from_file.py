from fastapi import  UploadFile
from docx import Document
import win32com.client
import fitz
from fastapi import HTTPException, UploadFile
import fitz  # PyMuPDF
from docx import Document
import win32com.client
from transformers import pipeline
from googletrans import Translator

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
        

class FileQuestionAnswering:

    def __init__(self):
        self.qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
        self.translator = Translator()

    def translate_text(self, text: str, src_lang: str, target_lang: str) -> str:
        text_json = {"text": text}
        if src_lang != target_lang:
            return self.translator.translate(text_json['text'], src=src_lang, dest=target_lang).text
        return text

    def answer_by_file(self, file, question: str):
        ext = file.filename.split(".")[-1].lower()
        if ext == "pdf":
            text = ExtractTextFromFile.pdf(file)
        elif ext == "docx":
            text = ExtractTextFromFile.docx(file)
        elif ext == "doc":
            text = ExtractTextFromFile.doc(file)
        else:
            raise HTTPException(status_code=400, detail="Error: Unsupported file format.")
        text_json = {"text": text}
        detected_lang = self.translator.detect(text).lang
        text = self.translate_text(text, detected_lang, 'en')

        question_en = self.translate_text(question, detected_lang, 'en')

        answer = self.qa_pipeline(question=question_en, context=text)
        answer_uk = self.translate_text(answer['answer'], 'en', 'uk')

        return answer_uk

