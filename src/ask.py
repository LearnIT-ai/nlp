from mistralai import Mistral

from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate

from langchain_community.embeddings import HuggingFaceEmbeddings

from dotenv import load_dotenv
import os

import argparse
from colorama import Fore,Style
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer


load_dotenv()

CHROMA_PATH = 'chroma'

PROMPT_TEMPLATE_WITH_CONTEXT = """Відповідай на запитання, спираючись лише на наступний контекст:{context} Відповідай на запитання на основі вищезгаданого контексту: {question}"""
PROMPT_TEMPLATE_WITHOUT_CONTEXT = """Відповідай на запитання на основі вищезгаданого контексту: {question}"""
api_key = os.getenv("MISTRAL_API_KEY")


client = Mistral(api_key=api_key)

tokenizer_nlp = T5Tokenizer.from_pretrained("google/flan-t5-xl")
model_nlp = T5ForConditionalGeneration.from_pretrained("google/flan-t5-xl").to("cuda")

model_name_translate = "facebook/m2m100_418M"
tokenizer_translate = M2M100Tokenizer.from_pretrained(model_name_translate)
model_translate = M2M100ForConditionalGeneration.from_pretrained(model_name_translate).to("cuda")



embed_model = HuggingFaceEmbeddings(model_name="thenlper/gte-base")

def main_flan_t5():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    query_model_flan_t5(query_text=query_text)


def translate_m2m(text, source_lang, target_lang):
    tokenizer_translate.src_lang = source_lang
    encoded_text = tokenizer_translate(text, return_tensors="pt", padding=True, truncation=True).to("cuda")
    generated_tokens = model_translate.generate(**encoded_text, forced_bos_token_id=tokenizer_translate.get_lang_id(target_lang))
    return tokenizer_translate.decode(generated_tokens[0], skip_special_tokens=True)

def run_flat_t5(user_message):
    input_text = user_message
    clean_query_text = input_text.replace("Human:", "").strip()

    print(f"{Fore.GREEN} INPUT TEXT : {clean_query_text} {Style.RESET_ALL}")
    en_text = translate_m2m(clean_query_text, source_lang="uk", target_lang="en")
    print(f"{Fore.YELLOW}Translated to English: {en_text} {Style.RESET_ALL}")

    input_ids = tokenizer_nlp(en_text, return_tensors="pt", padding=True, truncation=True).input_ids.to("cuda")
    outputs = model_nlp.generate(input_ids, max_length=512)
    decoded_output = tokenizer_nlp.decode(outputs[0], skip_special_tokens=True)
    print(f"{Fore.CYAN} Model response: {decoded_output} {Style.RESET_ALL}")

    uk_answer = translate_m2m(decoded_output, source_lang="en", target_lang="uk")
    print(f"{Fore.RED}Translated back to Ukrainian: {uk_answer} {Style.RESET_ALL}")
    return uk_answer

def query_model_flan_t5(query_text: str):
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embed_model)
    
    results = db.similarity_search_with_score(query_text, k=5)
    if results:
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_WITH_CONTEXT)
    else:
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_WITHOUT_CONTEXT)
        context_text = ""
    
    prompt = prompt_template.format(context=context_text, question=query_text)
    response_text = run_flat_t5(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\n\nSources: {sources}"
    print(formatted_response)
    return response_text



if __name__ == "__main__":
    main_flan_t5()