from sentence_transformers import SentenceTransformer, util

# Load the pre-trained model
model_name = "sentence-transformers/paraphrase-MiniLM-L6-v2"
model = SentenceTransformer(model_name)
