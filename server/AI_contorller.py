from models.gpt import GPT


class AiController:
    def general_chat(user_message):
        gpt_instance = GPT()
        stabilizator = "I am a student of computer science. Answer in Ukrainian or English only. The answer should be as detailed as possible, everything should be written step by step, and each step should be explained. So my question is:"
        stabilize_user_message = stabilizator + user_message + "?"
        response = gpt_instance.send_something(stabilize_user_message)
        formatted_response = response.replace("\n", "")  

        return formatted_response
    
    