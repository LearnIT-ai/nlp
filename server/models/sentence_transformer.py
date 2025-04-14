from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class SentenceSimilarity:
    @staticmethod
    def find_similarity(data: dict) -> float:
        user_answer = data.get("user_answer", "").strip()
        right_answer = data.get("right_answer", "").strip()

        if not user_answer or not right_answer:
            raise ValueError("Both user_answer and right_answer must be provided")

        model = SentenceTransformer('sentence-transformers/sentence-t5-large')

        user_embedding = model.encode([user_answer])
        right_embedding = model.encode([right_answer])

        similarity_score = cosine_similarity(user_embedding, right_embedding)[0][0] * 100

        return round(similarity_score, 2)  
