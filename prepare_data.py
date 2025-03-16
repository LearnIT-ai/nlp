from datasets import Dataset
import pandas as pd
import pdfplumber
import os
import re

def clear_cs_data(data_path: str):
    df = pd.read_csv(data_path)

    df = df.drop(['id', 'input'],axis=1)

    df = df.rename(columns={'output':"text"})

    df.to_json('CS_data/computer_science_data.json', orient='records', force_ascii=False, indent=4)

    df_json = pd.read_json('CS_data/computer_science_data.json')
    chunk_size = 10000

    # divide our dataset on 3 chunk
    for i, start in enumerate(range(0, len(df_json), chunk_size)):
        df_chunk = df_json.iloc[start:start + chunk_size]  # select some part of the rows
        df_chunk.to_json(f'CS_data/cs_part_{i+1}.json', orient='records', force_ascii=False, indent=4)

    print("Completed!")

def clear_psy_data(data_path: str):
    df_psy = pd.read_json(data_path)

    df_psy = df_psy.drop(['instruction', 'input'],axis=1)

    df_psy = df_psy.rename(columns={'output':"text"})

    df_psy.to_json('Psychology_data/Psychology_data.json', orient='records', force_ascii=False, indent=4)
    print('Completed!')

def is_valid_line(text: str):
    phone_pattern = r"\+?\d{1,3}[-.\s]?\(?\d{2,3}\)?[-.\s]?\d{2,3}[-.\s]?\d{2,3}[-.\s]?\d{2,4}"
    url_pattern = r"https?://\S+|www\.\S+|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" 
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    address_pattern = r"\b\d{1,4}\s+\w+\s+\w+\b"
    garbage_pattern = r"(?:\b\w{1,2}\b\s*){3,}"

    invalid_elements = ['.com', '.org', '.net', '.gov', '.edu', 'www', '@', 'http', 'https', '©', "вул.", "м.", "просп.", "Ум.", "шт.", "офіс"]
    
    for element in invalid_elements:
        if element in text:
            return False

    if re.search(phone_pattern, text) or re.search(url_pattern, text) or \
       re.search(email_pattern, text) or re.search(address_pattern, text) \
        or re.search(garbage_pattern, text):
        return False  
    return True 

def clear_km_data(data_path: str):
    all_items = os.listdir(data_path)

    data = [{"text": "Критичне Мислення"}]

    for files in all_items:
        with pdfplumber.open(f"{data_path}/{files}") as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                text_array = re.split(r"(?<=\.)\s*", text)
                for elem in text_array:
                    elem = re.sub(r"[\n\t]+", " ", elem).strip()
                    elem = re.sub(r'\b[A-ZА-ЯІЇЄҐ]{2,}\b', lambda x: x.group(0).lower(), elem)
                    if len(elem) < 10:
                        data[-1]["text"] += elem
                    else:
                        data.append({"text": elem})
    
    data = [elem for elem in data if is_valid_line(elem["text"])]

    df = pd.DataFrame(data)

    df = df.drop_duplicates()

    df.to_json('KM_data/km_data_dot.json', orient='records', force_ascii=False, indent=4)
    print('Completed!')

# clear_cs_data('computer_science_synthetic_dataset.csv')
# clear_psy_data('Psychology-10K.json')
clear_km_data('Критичне_Мислення')