import extract as extract_service
import os
import db
import logger
import transform as transform_service
import prompt_template
import chatbot

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
                                 query="Get reviews that talk about enginer and performance of the car",
                                 model_name=DEFAULT_EMBEDDING_MODEL)
    # logger.info(type(result))
    prompt = prompt_template.get_system_prompt(result)
    # logger.info(result)
    # logger.info(prompt)
    content = chatbot.query("I want to buy a car with good performance.Is this car right for me?",prompt)
    print(content)


if __name__ == "__main__":
    run(setup=False)