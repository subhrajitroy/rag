from sentence_transformers import SentenceTransformer

# all-MiniLM-L6-v2,paraphrase-albert-small-v2,paraphrase-MiniLM-L3-v2
DEFAULT_EMBEDDING_MODEL="paraphrase-albert-small-v2"

def get_embeddings(model_name=DEFAULT_EMBEDDING_MODEL,texts=[]):
    model=SentenceTransformer(model_name)
    encodings = []
    for text in texts:
        # print(f"Now encoding : {text}")
        encoding = model.encode(text)
        encodings.append(encoding)
    return encodings
    

