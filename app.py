import extract as extract_service
import embed_service
import db
import logger

DEFAULT_EMBEDDING_MODEL="paraphrase-albert-small-v2"

def etl():
        df = extract_service.extract_data()
        df.dropna(subset=["Review"],inplace=True)
        reviews = df["Review"].to_list()
        # texts = df["Review"].to_list()
        # embeddings = embed_service.get_embeddings(texts=texts)
        df.drop(columns=["Review"],inplace=True)
        rows_num = df.shape[0]
        metadata = []
        ids = []
        for i in range(0,rows_num):
            ids.append(f"review_{i}")
            meta = df.iloc[i].to_dict()
            metadata.append(meta)
        data = {
            "documents":reviews,
            "metadata":metadata,
            "ids" : ids,
            "size":rows_num
        }
        db.save(collection_name="reviews",model=DEFAULT_EMBEDDING_MODEL, data=data)

def run(setup=False):
    if setup:
        etl()
    result = db.query_collection(collection_name="reviews",
                                 query="Review of a car taliking about the engine",
                                 model_name=DEFAULT_EMBEDDING_MODEL)
    logger.info(result)

run()