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

def clear_km_data(data_path: str):
    all_items = os.listdir(data_path)

    data = []

    for files in all_items:
        with pdfplumber.open(f"{data_path}/{files}") as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                
                if text:
                    text = re.sub(r"\s+", " ", text).strip()

                    chunks = [text[i:i + len(text) // 3] for i in range(0, len(text), len(text) // 3)]
                
                    for chunk in chunks:
                        if (len(chunk) > 10):
                            data.append({"text": chunk})

    df = pd.DataFrame(data)

    df = df.drop_duplicates()

    df.to_json('KM_data/km_data.json', orient='records', force_ascii=False, indent=4)
    print('Completed!')

# clear_cs_data('computer_science_synthetic_dataset.csv')
# clear_psy_data('Psychology-10K.json')
clear_km_data('Критичне_Мислення')