import extract as extract_service
import os
import db
import logger
import transform as transform_service

DEFAULT_EMBEDDING_MODEL="paraphrase-albert-small-v2"
DATA_PATH=os.environ["DATA_PATH"]

def generate_metadata(df):
        ids = []
        metadata = []
        for i in range(0,df.shape[0]):
            ids.append(f"review_{i}")
            meta = df.iloc[i].to_dict()
            metadata.append(meta)
        return ids,metadata

def etl():
        df = extract_service.extract_data()
        df, reviews = transform_service.transform(df)
        rows_num = df.shape[0]
        ids, metadata = generate_metadata(df)   
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


if __name__ == "__main__":
    run(setup=False)