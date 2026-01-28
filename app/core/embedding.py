from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingModel:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initializes the SentenceTransformer model.
        Using all-MiniLM-L6-v2 for speed and good performance.
        """
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        print("Model loaded.")

    def get_embedding(self, text: str) -> np.ndarray:
        """
        Generates a vector embedding for the given text.
        """
        return self.model.encode(text)

# Global instance to avoid reloading
_embedding_model_instance = None

def get_model_instance():
    global _embedding_model_instance
    if _embedding_model_instance is None:
        _embedding_model_instance = EmbeddingModel()
    return _embedding_model_instance
