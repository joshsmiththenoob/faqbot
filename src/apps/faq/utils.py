from django.conf import settings
from sentence_transformers import SentenceTransformer

# 兩個擇一
# _model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
_model = SentenceTransformer("BAAI/bge-base-zh-v1.5")

def get_embedding(text: str):
    vec = _model.encode(text, normalize_embeddings=True)
    return vec.tolist()


def check_channel_config() -> None:
    """
    Check if the LINE channel configuration is set properly.

    Raises:
        ValueError: If the LINE channel secret or access token is not set.
    """
    if not settings.CHANNEL_SECRET:
        raise ValueError("LINE_CHANNEL_SECRET is not set.")
    if not settings.CHANNEL_ACCESS_TOKEN:
        raise ValueError("LINE_CHANNEL_ACCESS_TOKEN is not set.")