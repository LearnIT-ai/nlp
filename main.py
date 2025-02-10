from get_similarity import SimilarityModel

MODEL_PATH = "./similarity_model"

similarity_model = SimilarityModel(MODEL_PATH)

text1 = "A woman is dancing in the rain."
text2 = "A woman dances in the rain out side."

score = similarity_model.compute_similarity(text1, text2)
print(f"Similarity Score: {score:.2f}%")