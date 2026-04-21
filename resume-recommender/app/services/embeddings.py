from sentence_transformers import SentenceTransformer
from app.core.config import settings

# -----------------------------
# Global Model (Lazy Loaded)
# -----------------------------
_model = None


def get_model():
    global _model

    if _model is None:
        print(f"🔄 Loading embedding model: {settings.EMBEDDING_MODEL}")
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
        print("✅ Embedding model loaded")

    return _model


# -----------------------------
# Generate Embedding
# -----------------------------
def get_embedding(text: str) -> list:
    """
    Convert text into embedding vector.

    Args:
        text (str): Input text (query or resume)

    Returns:
        list: Embedding vector
    """
    model = get_model()

    # Normalize text (important for consistency)
    text = text.strip()

    if not text:
        return []

    embedding = model.encode(text)

    return embedding.tolist()


# -----------------------------
# Batch Embeddings (Optional)
# -----------------------------
def get_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for multiple texts (faster for bulk operations)

    Args:
        texts (list[str]): List of texts

    Returns:
        list[list[float]]: List of embedding vectors
    """
    model = get_model()

    # Clean inputs
    texts = [t.strip() for t in texts if t.strip()]

    if not texts:
        return []

    embeddings = model.encode(texts)

    return [e.tolist() for e in embeddings]