import chromadb
from chromadb.utils import embedding_functions 
import logger

def get_embedding_function(model_name):
    return embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)

def save(collection_name, model, data, distance_function_name="cosine"):
    logger.info(f"Saving data in collection {collection_name}")
    client = chromadb.PersistentClient(path="chroma_data/")
    collection = client.get_or_create_collection(
        name = collection_name,
        embedding_function = get_embedding_function(model),
        metadata = {"hnsw:space": distance_function_name},
    )
    documents = data["documents"]
    metadata = data["metadata"]
    ids = data["ids"]
    # size = data["size"]
    collection.add(documents=documents, ids=ids, metadatas=metadata)
    logger.info(f"Saved {len(documents)} documents in collection {collection_name}")

    

def query_collection(collection_name,query,model_name,distance_function_name="cosine"):
    client = chromadb.PersistentClient(path="chroma_data/")
    collection = client.get_or_create_collection(
        name = collection_name,
        embedding_function = get_embedding_function(model_name),
        metadata = {"hnsw:space": distance_function_name},
    )
    results = collection.query(
        query_texts=[query],
        n_results=5,
        include=["documents", "distances", "metadatas"]
    )
    logger.info(f"Found {len(results['documents'])} documents")
    # logger.info(results["documents"][0][0])
    return results["documents"][0][0]