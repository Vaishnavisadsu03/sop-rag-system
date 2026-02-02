from langchain_community.embeddings import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL_NAME

# Global cache so model loads only once
_embedding_model = None


def get_embedding_model():
    """
    Returns a cached HuggingFace embedding model.
    Uses CPU explicitly to avoid CUDA/GPU issues.
    """
    global _embedding_model

    if _embedding_model is None:
        _embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
            model_kwargs={"device": "cpu"}
        )

    return _embedding_model
