
import g4f

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
        