import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os

class SimilarityModel:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), "model_for_similarity")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.eval()
    
    def compute_similarity(self, text_data):
        text1 = text_data["user_answer"]
        text2 = text_data["right_answer"]

        inputs = self.tokenizer(text1, text2, return_tensors="pt", padding=True, truncation=True, max_length=128)

        with torch.no_grad():
            outputs = self.model(**inputs)

        similarity_score = torch.sigmoid(outputs.logits).squeeze().item() * 100
        return similarity_score