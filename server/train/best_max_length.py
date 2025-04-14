import matplotlib.pyplot as plt
from datasets import load_dataset
from transformers import AutoTokenizer
import numpy as np

model_name = "mistralai/Mistral-7B-Instruct-v0.3"
tokenizer = AutoTokenizer.from_pretrained(model_name)

dataset = load_dataset("json", data_files="computer_science_data.json")

lengths = [len(tokenizer.encode(text)) for text in dataset['train']['text']]

plt.hist(lengths, bins=50, edgecolor='black')
plt.title("Distribution of Text Lengths")
plt.xlabel("Length in tokens")
plt.ylabel("Frequency")
plt.show()

percentile_90 = np.percentile(lengths, 90)
print(f"90th percentile: {percentile_90}")
