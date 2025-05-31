
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
    
    def generate_syllabus_by_subject(self, subject: str) -> str:
        prompt = (
            f"Згенеруй силабус у форматі HTML для курсу '{subject}'. "
            f"Використовуй теги HTML: <h1>, <h2>, <p>, <ul>, <li>, <b>. "
            f"Не додавай стилів CSS, лише структуру документа. "
            f"Розділи: Назва, Програма, Мета, Компетенції, Теми, Методи, Оцінювання, Література, Політики тощо."
            f"Обов’язково включи наступні розділи:\n"
            f"- Назва дисципліни, освітня програма, спеціальність, рівень освіти, мова викладання\n"
            f"- Анотація дисципліни\n"
            f"- Мета навчальної дисципліни\n"
            f"- Загальні та фахові компетентності\n"
            f"- Результати навчання\n"
            f"- Зміст курсу з поділом на лекції та лабораторні заняття (теми)\n"
            f"- Методи навчання\n"
            f"- Оцінювання (баланс по модулях, практичні, контроль)\n"
            f"- Рекомендована література\n"
            f"Використай структуру та стиль, аналогічний типовим силабусам українських університетів.\n"
            f"Пиши українською мовою, акуратно структуровано. Не використовуй списки 'Item 1, Item 2' — пиши як у справжньому навчальному документі."
        )

        return self.send_something(prompt)
