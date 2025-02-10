import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class SimilarityModel:
    def __init__(self, model_path):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.eval()
    
    def compute_similarity(self, text1, text2):
        inputs = self.tokenizer(text1, text2, return_tensors="pt", padding=True, truncation=True, max_length=128)

        with torch.no_grad():
            outputs = self.model(**inputs)

        similarity_score = torch.sigmoid(outputs.logits).squeeze().item() * 100
        return similarity_score