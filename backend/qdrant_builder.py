from qdrant_client import QdrantClient, models
import ast
import pandas as pd


client = QdrantClient(url="http://localhost:6333")

data = pd.read_csv('db.csv')
documents = data.to_dict(orient='records')

def convert_name_emb(data_list):
    for item in data_list:
        if 'name_emb' in item:
            item['names_emb'] = ast.literal_eval(item['name_emb'])
    return data_list

def convert_content_emb(data_list):
    for item in data_list:
        if 'content_emb' in item:
            item['content_emb'] = ast.literal_eval(item['content_emb'])
    return data_list


client.create_collection(
    collection_name="names",
    vectors_config=models.VectorParams(
        size=1024,
        distance=models.Distance.COSINE
    )
)

client.create_collection(
    collection_name="content",
    vectors_config=models.VectorParams(
        size=1024,
        distance=models.Distance.COSINE
    )
)


documents_name = convert_name_emb(documents)

client.upload_points(
    collection_name="names",
    points=[models.PointStruct(
        id=idx,
        vector=doc['name_emb'],
        payload=doc
    )
    for idx, doc in enumerate(documents_name)],
)


documents_content = convert_content_emb(documents)

client.upload_points(
    collection_name="content",
    points=[models.PointStruct(
        id=idx,
        vector=doc['content_emb'],
        payload=doc
    )
    for idx, doc in enumerate(documents_content)],
)