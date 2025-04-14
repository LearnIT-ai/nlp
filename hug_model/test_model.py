from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

# Завантаження моделі T5
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-xl")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-xl").to("cuda")

# Завантаження моделі перекладу M2M100
model_name_translate = "facebook/m2m100_418M"
tokenizer_translate = M2M100Tokenizer.from_pretrained(model_name_translate)
model_translate = M2M100ForConditionalGeneration.from_pretrained(model_name_translate).to("cuda")

# Функція перекладу
def translate_m2m(text, source_lang, target_lang):
    tokenizer_translate.src_lang = source_lang
    encoded_text = tokenizer_translate(text, return_tensors="pt", padding=True, truncation=True).to("cuda")
    generated_tokens = model_translate.generate(**encoded_text, forced_bos_token_id=tokenizer_translate.get_lang_id(target_lang))
    return tokenizer_translate.decode(generated_tokens[0], skip_special_tokens=True)

# Переклад українського запиту на англійську
input_text = "Що таке революція?"
en_text = translate_m2m(input_text, source_lang="uk", target_lang="en")
print("Translated to English:", en_text)

# Генерація відповіді англійською мовою
input_ids = tokenizer(en_text, return_tensors="pt", padding=True, truncation=True).input_ids.to("cuda")
outputs = model.generate(input_ids, max_length=512)
decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("Model response:", decoded_output)

# Переклад англійської відповіді на українську
uk_answer = translate_m2m(decoded_output, source_lang="en", target_lang="uk")
print("Translated back to Ukrainian:", uk_answer)
