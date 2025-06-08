
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
    
#     const syllabus = {
#         subject: "Назва дисципліни",
#         educational_program: "освітня програма",
#         specialty: "спеціальність",
#         level_of_education: "рівень освіти",
#         language: "мова викладання",
#         abstract: "Анотація дисципліни",
#         goal: "Мета навчальної дисципліни",
#         competencies: "Загальні та фахові компетентності",
#         outcomes: "Результати навчання",
#         content: "Зміст курсу з поділом на лекції та лабораторні заняття (теми)",
#         methods: "Методи навчання",
#         evaluation: "Оцінювання (баланс по модулях, практичні, контроль)",
#         literature: "Рекомендована література",
#     };


    def generate_syllabus_by_answers(self, body) -> str:
        prompt = (
            f"Згенеруй силабус у форматі HTML для курсу '{body.get("subject")}'. "
            f"Використовуй теги HTML: <h1>, <h2>, <p>, <ul>, <li>, <b>. "
            f"Не додавай стилів CSS, лише структуру документа. "
            f"Розділи: Назва, Програма, Мета, Компетенції, Теми, Методи, Оцінювання, Література, Політики тощо."
            f"Обов’язково включи наступні розділи:\n"
            f"- Назва дисципліни: {body.get("subject")}\n"
            f"- Освітня програма: {body.get("educational_program")}\n"
            f"- Cпеціальність: {body.get("specialty")}\n" 
            f"- Рівень освіти: {body.get("level_of_education")}\n"
            f"- Мова викладання: {body.get("language")}\n"
            f"- Анотація дисципліни: {body.get("abstract")}\n"
            f"- Мета навчальної дисципліни: {body.get("goal")}\n"
            f"- Загальні та фахові компетентності: {body.get("competencies")}\n"
            f"- Результати навчання: {body.get("outcomes")}\n"
            f"- Зміст курсу з поділом на лекції та лабораторні заняття (теми): {body.get("content")}\n"
            f"- Методи навчання: {body.get("methods")}\n"
            f"- Оцінювання (баланс по модулях, практичні, контроль): {body.get("evaluation")}\n"
            f"- Рекомендована література: {body.get("literature")}\n"
            f"Використай структуру та стиль, аналогічний типовим силабусам українських університетів.\n"
            f"Пиши українською мовою, акуратно структуровано. Не використовуй списки 'Item 1, Item 2' — пиши як у справжньому навчальному документі."
        )

        return self.send_something(prompt)

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