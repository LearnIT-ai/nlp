from mistralai import Mistral

from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")

client = Mistral(api_key=api_key)

chat_response = client.chat.complete(
    model = "mistral-small",
    messages=[
        {
            "role": "user",
            "content": "Tell me something about France"
        }
    ]
)

print(chat_response.choices[0].message.content)