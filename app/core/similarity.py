from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def calculate_similarity(embedding_a: np.ndarray, embedding_b: np.ndarray) -> float:
    """
    Calculates the cosine similarity between two embeddings.
    Returns a score between 0 and 1.
    """
    # Reshape to (1, -1) if they are 1D arrays
    if len(embedding_a.shape) == 1:
        embedding_a = embedding_a.reshape(1, -1)
    if len(embedding_b.shape) == 1:
        embedding_b = embedding_b.reshape(1, -1)

    score = cosine_similarity(embedding_a, embedding_b)[0][0]
    return float(score)

def get_risk_level(score: float) -> str:
    """
    Returns the risk level based on the similarity score.
    < 40%: Low
    40-70%: Medium
    > 70%: High
    """
    # Convert to percentage for comparison
    percentage = score * 100
    if percentage < 40:
        return "Low"
    elif percentage <= 70:
        return "Medium"
    else:
        return "High"
