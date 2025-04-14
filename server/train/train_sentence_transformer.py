from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import Dataset
import pandas as pd
from sklearn.model_selection import train_test_split
import torch

DATA_PATH = "data/full.csv"
MODEL_PATH = "./similarity_model"

def load_data(file_path):
    data = pd.read_csv(file_path)
    data = data.rename(columns={
        'user_answer': 'text1',
        'right_answer': 'text2',
        'Similarly': 'label'
    })
    data['label'] = data['label'].astype(float)
    return data

data = load_data(DATA_PATH)

train_data, val_data = train_test_split(data, test_size=0.2, random_state=42)

train_dataset = Dataset.from_pandas(train_data)
val_dataset = Dataset.from_pandas(val_data)

model_name = "sentence-transformers/all-mpnet-base-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=1)

def tokenize_function(examples):
    return tokenizer(examples['text1'], examples['text2'], padding='max_length', truncation=True, max_length=128)

train_dataset = train_dataset.map(tokenize_function, batched=True)
val_dataset = val_dataset.map(tokenize_function, batched=True)

data_columns = ['input_ids', 'attention_mask']
train_dataset.set_format(type='torch', columns=data_columns, output_all_columns=True)
val_dataset.set_format(type='torch', columns=data_columns, output_all_columns=True)

training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="nlp\logs",
    logging_strategy="epoch",
    save_total_limit=2,
    load_best_model_at_end=True
)
class CustomTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):
        labels = inputs.pop("labels").float().unsqueeze(1)
        outputs = model(**inputs)
        loss_fct = torch.nn.MSELoss()
        loss = loss_fct(outputs.logits, labels)
        return (loss, outputs) if return_outputs else loss

trainer = CustomTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)

trainer.train()

model.save_pretrained(MODEL_PATH)
tokenizer.save_pretrained(MODEL_PATH)
