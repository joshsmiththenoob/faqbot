from sentence_transformers import SentenceTransformer

# 兩個擇一
# _model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
_model = SentenceTransformer("BAAI/bge-base-zh-v1.5")

def get_embedding(text: str):
    vec = _model.encode(text, normalize_embeddings=True)
    return vec.tolist()
