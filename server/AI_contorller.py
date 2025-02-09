from models.gpt import GPT
from utils.extrac_text_from_file import ExtractTextFromFile
from models.sentence_transformer import SentenceSimilarity


class AiController:
    def general_chat(user_message):
        gpt_instance = GPT()
        stabilizator = "I am a student of computer science. Answer in Ukrainian or English only. The answer should be as detailed as possible, everything should be written step by step, and each step should be explained. So my question is:"
        stabilize_user_message = stabilizator + user_message + "?"
        response = gpt_instance.send_something(stabilize_user_message)
        formatted_response = response.replace("\n", "")  

        return formatted_response
    
    def check_homework_file(homework_file):
        ext = homework_file.filename.split(".")[-1].lower()
        if ext == "pdf":
            homework_file.file.seek(0)
            text = ExtractTextFromFile.pdf(homework_file)
        elif ext == "docx":
            homework_file.file.seek(0)
            text = ExtractTextFromFile.docx(homework_file)
        elif ext == "doc":
            homework_file.file.seek(0)
            text = ExtractTextFromFile.doc(homework_file)
        else:
            raise Exception("Wrong format of file")

        request_to_AI = "This is my homework. Your task is to read the task and provide a solution, do not change or correct my answer to the task. Just solve the task. The answer must be in the language in which my solution is written. The answer should not contain a well-done task according to these criteria, only the task itself and your answer to the task and nothing more. The structure should be the same as in the file I sent you (for example, task: answer:). Here is the task: " + text
        # TEMPORARY CHANGE OT OUR MODEL
        gpt_instance = GPT()
        model_response = gpt_instance.send_something(request_to_AI)
        text_for_similarity = {
            "user_answer": text,
            "right_answer": model_response
        }
        # TEMOPORARY CHANGE TO OUR MODEL
        # FIND THE BETTER WAY TO READ CONTEXT OF ANSWERS
        response_for_user = SentenceSimilarity.find_similarity(text_for_similarity)

        if response_for_user > 85:
            return "Your homework is correct"
        else:
            return "Your homework is incorrect"
        

    def check_homework_text(task, answer):
        request_to_ai = "This is my homework. Your task is to read the task and provide a solution. Just solve the task. The answer must be in the language in which my solution is written. The answer does not have to contain a well-executed task according to these criteria, only your answer to the task and nothing more. Here is the task: " + task
        # TEMPORARY CHANGE OT OUR MODEL
        gpt_instance = GPT()
        model_response = gpt_instance.send_something(request_to_ai)

        text_for_similarity = {
            "user_answer": answer,
            "right_answer": model_response
        }
        # TEMOPORARY CHANGE TO OUR MODEL
        # FIND THE BETTER WAY TO READ CONTEXT OF ANSWERS
        response_for_user = SentenceSimilarity.find_similarity(text_for_similarity)
        if response_for_user > 85:
            return "Your homework is correct"
        else:
            return "Your homework is incorrect"