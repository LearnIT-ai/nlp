from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import Dataset
import torch
import json

model_name = "mistralai/Mistral-7B-Instruct-v0.3"
tokenizer = AutoTokenizer.from_pretrained(model_name)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token  

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16  
).to(device) 

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return Dataset.from_dict({"text": [item["text"] for item in data]})

dataset = load_data("computer_science_data.json")

def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        truncation=True,
        padding="max_length",
        max_length=256,
        add_special_tokens=True 
    )

dataset = dataset.map(tokenize_function, batched=True)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

training_args = TrainingArguments(
    output_dir="./mistral-finetuned",  
    evaluation_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=2,  
    per_device_eval_batch_size=2,
    gradient_accumulation_steps=8,  
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_strategy="epoch",
    save_total_limit=2,
    load_best_model_at_end=True,
    fp16=True,  
    dataloader_pin_memory=True, 
    report_to="none"  
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    eval_dataset=dataset,
    data_collator=data_collator,
)

trainer.train()

model.save_pretrained("./mistral-finetuned")
tokenizer.save_pretrained("./mistral-finetuned")
