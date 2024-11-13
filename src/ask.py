from mistralai import Mistral

from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate

from langchain_community.embeddings import HuggingFaceEmbeddings

from dotenv import load_dotenv
import os

import argparse

load_dotenv()

CHROMA_PATH = 'chroma'

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

api_key = os.getenv("MISTRAL_API_KEY")


client = Mistral(api_key=api_key)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    query_model(query_text=query_text)

embed_model = HuggingFaceEmbeddings(model_name="thenlper/gte-base")

def run_mistral(user_message, model="mistral-small"):
    messages = [
        {
            "role": "user", "content": user_message
        }
    ]
    chat_response = client.chat.complete(
        model=model,
        messages=messages
    )
    return (chat_response.choices[0].message.content)

def query_model(query_text: str):
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embed_model)

    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    response_text = run_mistral(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\n\nSources: {sources}"
    print(formatted_response)
    return response_text


if __name__ == "__main__":
    main()