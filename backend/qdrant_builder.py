from qdrant_client import QdrantClient, models
import ast
import pandas as pd


client = QdrantClient(url="http://localhost:6333")

data = pd.read_csv('db.csv')
documents = data.to_dict(orient='records')

def convert_name_emb(data_list):
    for item in data_list:
        if 'content_emb' in item:
            item['content_emb'] = ast.literal_eval(item['content_emb'])
    return data_list

documents = convert_name_emb(documents)


client.create_collection(
    collection_name="content",
    vectors_config=models.VectorParams(
        size=1024,
        distance=models.Distance.COSINE
    )
)

client.upload_points(
    collection_name="content",
    points=[models.PointStruct(
        id=idx,
        vector=doc['content_emb'],
        payload=doc
    )
    for idx, doc in enumerate(documents)],
)