from mistralai import Mistral

from langchain.vectorstores.chroma import Chroma
 
from dotenv import load_dotenv
import os

import argparse

load_dotenv()

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

def get_text_embedding(query_text: str):
    embeddings_batch_response = client.embeddings.create(
        model="mistral-embed",
        inputs=query_text
    ) 
    return embeddings_batch_response.data[0].embedding

def query_model(query_text: str):
    pass
    

if __name__ == "__main__":
    main()