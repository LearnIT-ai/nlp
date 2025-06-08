from models.gpt import GPT
from utils.extract_text_from_file import ExtractTextFromFile
from utils.pdf_generator import PDFGeneratorHtml
from models.similarity_model import SimilarityModel
from deep_translator import GoogleTranslator
from fastapi import HTTPException
from langdetect import detect
from googletrans import Translator
import string
import random
from dotenv import load_dotenv
import os

HTML_HEADER = """
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {
      font-family: 'DejaVu Sans', sans-serif;
      margin: 40px;
      line-height: 1.6;
    }
    h1, h2 {
      font-weight: bold;
      text-align: center;
      margin-top: 24px;
      margin-bottom: 16px;
    }
    h1 {
      font-size: 24pt;
    }
    h2 {
      font-size: 16pt;
      text-align: left;
    }
    p {
      text-align: justify;
      margin: 10px 0;
    }
    ul {
      margin-left: 20px;
    }
    li {
      margin-bottom: 6px;
    }
    b {
      font-weight: bold;
    }
  </style>
</head>
<body>
"""

HTML_FOOTER = "</body></html>"
class AiController:
    @staticmethod
    def detect_language(text):
        try:
            return detect(text)
        except Exception:
            raise HTTPException(detail="Error: Unable to detect language.",status_code=400)
    
    @staticmethod
    def translate_text(text, source_lang, target_lang):
        if source_lang == target_lang:
            return text
        return GoogleTranslator(source=source_lang, target=target_lang).translate(text)
    
    def general_chat(self, user_message):
        detected_lang = self.detect_language(user_message)
        if detected_lang not in ["en", "uk"]:
            raise HTTPException(detail="Error: Support only English and Ukrainian language.",status_code=400)

        gpt_instance = GPT()
        stabilizator = (
            "I am a student of computer science. Answer in Ukrainian or English only. "
            "The answer should be as detailed as possible, everything should be written step by step, "
            "and each step should be explained. So my question is: "
        )

        user_message = self.translate_text(user_message, detected_lang, "en")
        stabilize_user_message = stabilizator + user_message + "?"
        response = gpt_instance.send_something(stabilize_user_message)
        response_lang = self.detect_language(response)

        response = self.translate_text(response, response_lang, "uk")
        return response.replace("\n", "")

    def check_homework_file(self, homework_file):
        ext = homework_file.filename.split(".")[-1].lower()
        text = ExtractTextFromFile.multi_file(homework_file, ext)
        
        detected_lang = self.detect_language(text)
        if detected_lang not in ["en", "uk"]:
            raise HTTPException(detail="Error: Wrong language in the file. Use only English or Ukrainian.",status_code=400)
        
        text = self.translate_text(text, detected_lang, "en")
        request_to_ai = (
            "This is my homework. Your task is to read the task and provide a solution. "
            "Do not change or correct my answer, just solve the task. The answer must be in the original language. "
            "Keep the structure of the file (e.g., task: answer:). Here is the task: " + text
        )
        
        gpt_instance = GPT()
        model_response = gpt_instance.send_something(request_to_ai)
        model_response = self.translate_text(model_response, "en", detected_lang)
        
        similarity_score = SimilarityModel().compute_similarity({
            "user_answer": text,
            "right_answer": model_response
        })
        
        return "Your homework is correct" if similarity_score > 85 else "Your homework is incorrect"

    def check_homework_text(self, task, answer):
        task_lang = self.detect_language(task)
        answer_lang = self.detect_language(answer)
        
        if task_lang not in ["en", "uk"] or answer_lang not in ["en", "uk"]:
            raise HTTPException(detail="Error: Use only English or Ukrainian.",status_code=400)
        
        task = self.translate_text(task, task_lang, "en")
        request_to_ai = (
            "This is my homework. Your task is to read the task and provide a solution. "
            "The answer must be in the original language. Here is the task: " + task
        )
        
        gpt_instance = GPT()
        model_response = gpt_instance.send_something(request_to_ai)
        model_response = self.translate_text(model_response, "en", task_lang)
        
        similarity_score = SimilarityModel().compute_similarity({
            "user_answer": answer,
            "right_answer": model_response
        })

        request_to_ai = (
                "This was a task: " + task + 
                "And this is your answer to the task: " + model_response + 
                "And this is answer of the student: " + answer
            )

        if (similarity_score > 85):
            request_to_ai += "And student's solution is correct, but can you give " \
            "him some recommendations for the improvement in the original language."
            model_response = gpt_instance.send_something(request_to_ai)
        else:
            request_to_ai += "And student's solution is incorrect, can you give " \
            "him some recommendations to complete this task correctly in the original language."
            model_response = gpt_instance.send_something(request_to_ai)
            
        return model_response
    
    def get_homework_feedback(self, task, answer):
        task_lang = self.detect_language(task)
        answer_lang = self.detect_language(answer)
        
        if task_lang not in ["en", "uk"] or answer_lang not in ["en", "uk"]:
            raise HTTPException(detail="Error: Use only English or Ukrainian.",status_code=400)
        
        task = self.translate_text(task, task_lang, "en")
        request_to_ai = (
            "This is my homework. Your task is to read the task and provide a solution. "
            "The answer must be in the original language. Here is the task: " + task
        )
        
        gpt_instance = GPT()
        model_response = gpt_instance.send_something(request_to_ai)
        model_response = self.translate_text(model_response, "en", task_lang)
        
        similarity_score = SimilarityModel().compute_similarity({
            "user_answer": answer,
            "right_answer": model_response
        })

        request_to_ai = (
                "This was a task: " + task + 
                "And this is your answer to the task: " + model_response + 
                "And this is answer of the student: " + answer
            )

        if (similarity_score > 85):
            request_to_ai += "And student's solution is correct, but can you give " \
            "him some recommendations for the improvement in the original language."
            model_response = gpt_instance.send_something(request_to_ai)
        else:
            request_to_ai += "And student's solution is incorrect, can you give " \
            "him some recommendations to complete this task correctly in the original language."
            model_response = gpt_instance.send_something(request_to_ai)
            
        return model_response


    def get_texts_similarity(user_answer, model_answer):
        similarity_model = SimilarityModel()

        text_data = {
            "user_answer": user_answer,
            "right_answer": model_answer
        }

        score = similarity_model.compute_similarity(text_data)
        return f"Homework similiraty score is {score:.2f}%"
    
    
    def get_files_similarity(user_file, model_file):
        # parse user file
        user_extenstion = user_file.filename.split(".")[-1].lower()
        user_text = ExtractTextFromFile.multi_file(user_file, user_extenstion)
        
        # parse model file
        model_extenstion = model_file.filename.split(".")[-1].lower()
        model_text = ExtractTextFromFile.multi_file(model_file, model_extenstion)
        
        similarity_model = SimilarityModel()
        
        text_data = {
            "user_answer": user_text,
            "right_answer": model_text
        }

        score = similarity_model.compute_similarity(text_data)
        return f"Homework similiraty score is {score:.2f}%"
        

    def chunk_text(self,text, max_size=3000):
        chunks = []
        start = 0
        while start < len(text):
            end = start + max_size
            chunks.append(text[start:end])
            start = end
        return chunks

    def translate_in_chunks(self,translator, text, src, dest, chunk_size=1000):
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start = end
        
        translated_text = ""
        for chunk in chunks:
            translation = translator.translate(chunk, src=src, dest=dest)
            translated_text += translation.text
        return translated_text
    
    def safe_translate_to_english(self,text: str) -> str:
        if not text.strip():
            raise HTTPException("File is empty.",400)


        src_lang = detect(text)
        if src_lang == "en":
            return text  
        elif src_lang == "uk":
            translator = Translator()
            return self.translate_in_chunks(translator, text, src='uk', dest='en', chunk_size=1000)
        else:
            raise HTTPException("File text language not supported. Only English and Ukrainian are allowed.",400)
        
    def safe_translate_question_to_english(self, question: str) -> str:
        if not question.strip():
            raise HTTPException("Question is empty.",400)

        q_lang = detect(question)
        if q_lang == "en":
            return question
        elif q_lang == "uk":
            translator = Translator()
            return self.translate_in_chunks(translator, question, src='uk', dest='en', chunk_size=1000)
        else:
            raise HTTPException("Question language not supported. Only English and Ukrainian are allowed.",400)


    def answer_by_file(self,user_file,user_question: str):
        ext = user_file.filename.split(".")[-1].lower()
        file_content = ExtractTextFromFile.multi_file(user_file, ext)

        file_content_en = self.safe_translate_to_english(file_content)

        user_question_en = self.safe_translate_question_to_english(user_question)

        gpt_instance = GPT()

        chunks = self.chunk_text(file_content_en, max_size=3000)
        relevant_parts = []

        for i, chunk in enumerate(chunks):
            prompt = f"""
            Below is a part of a text. The user question is: "{user_question_en}"

            Text chunk #{i}:
            \"\"\"
            {chunk}
            \"\"\"

            Please extract only information relevant or potentially useful to answer the question, in concise form.
            """

            chunk_answer = gpt_instance.send_something(prompt)
            relevant_parts.append(chunk_answer)

        final_prompt = f"""
        I have gathered some relevant information from different chunks of a larger text (see below).
        Please use the information to answer the question: "{user_question_en}"

        Information extracted:
        \"\"\"
        {''.join(relevant_parts)}
        \"\"\"

        Provide a concise and direct answer to the question.
        """

        final_answer_en = gpt_instance.send_something(final_prompt)

        translator = Translator()
        final_answer_uk = translator.translate(final_answer_en, src='en', dest='uk').text

        return final_answer_uk
    
    
    def generate_survey_syllabus(body):
        load_dotenv()
        port = os.getenv("GATEWAY_PORT")
        host = os.getenv("GATEWAY_HOST")
        gpt_instance = GPT()
        gpt_response = gpt_instance.generate_syllabus_by_answers(body)

        suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        filename = f"{body.get("subject").replace(' ', '_').lower()}_{suffix}.pdf"
        html_result = HTML_HEADER + gpt_response + HTML_FOOTER
        PDFGeneratorHtml().save_html_as_pdf(html_result, filename)
        return f"http://{host}:{port}/default/get_silabus?filename={filename}"


    def generate_simple_silabus(subject):
        load_dotenv()
        port = os.getenv("GATEWAY_PORT")
        host = os.getenv("GATEWAY_HOST")
        gpt_instance = GPT()
        gpt_response = gpt_instance.generate_syllabus_by_subject(subject)

        suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        filename = f"{subject.replace(' ', '_').lower()}_{suffix}.pdf"
        html_result = HTML_HEADER + gpt_response + HTML_FOOTER
        PDFGeneratorHtml().save_html_as_pdf(html_result, filename)
        return f"http://{host}:{port}/default/get_silabus?filename={filename}"
