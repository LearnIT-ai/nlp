
import time
import g4f

class Claude:
    def __init__(self) -> None:
        pass
    
    
class GPT:
    def __init__(self , context:str=None, instruction:str=None,max_tokens:int=None) -> None:
        self.model = 'gpt-4'
        self.instruction = instruction if instruction else None
        self.context = context if context else None
        self.max_tokens = max_tokens if max_tokens and max_tokens > 10 else None  
        self.client = g4f.client.Client()
    
    def template_send(self):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                "role": "user",
                "content": self.instruction
            }]        
        )
        return response.choices[0].message.content
        
    def send_something(self,message):
        self.instruction = message 
        response = self.template_send()
        return response
        
    def connection(self):
        start_time = time.time()
        self.context = "Answer as I am a doctor"
        self.instruction = "if the request was successful and everything works fine, answer me with the phrase 'gpt connected', if you feel that something is wrong, then do not answer at all"
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                # {"role": "system",
                # "content": self.context},
                {
                "role": "user",
                "content": self.instruction
            }]
        )
        end_time = time.time()
        execution_time = end_time - start_time

        return response.choices[0].message.content , execution_time 
    
    def hello_message(self, speciality):
        self.instruction = f""