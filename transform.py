def transform(df):
    df.dropna(subset=["Review"],inplace=True)
    reviews = df["Review"].to_list()
    # texts = df["Review"].to_list()
    # embeddings = embed_service.get_embeddings(texts=texts)
    df.drop(columns=["Review"],inplace=True)
    return df,reviews