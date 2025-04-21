import requests
from qdrant_client import QdrantClient, models


client = QdrantClient(url="http://localhost:6333")



def reasoning_step_one(chat, intent):

    intent_query = intent['query']
    intent_precision = intent['precision']

    system = {
        "role": "system",
        "content": "Ты виртуальный ассистент оператора колл-центра компании сотовой связи. В фирме много различных услуг, тарифов, подписок, сервисов. Твоя задача - анализировать потребность клиента и формировать запрос для векторного поиска по базе знаний. Напиши только сам запрос."
    }

    headers = {
        'Authorization': 'Bearer sk-KNo006G2a48UVE3IxFlQEQ'
    }

    payload = {
        "model": "mws-gpt-alpha",
        "messages": [
            system,
            *chat,
            system
        ],
        "temperature": 0.4,
        "max_tokens": 150,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stop": ["\n"]
    }

    try:
        response = requests.post('https://api.gpt.mws.ru/v1/chat/completions', json=payload, headers=headers)
        response.raise_for_status()
        resp = response.json()
        print("Knowlege Agent, запрос в qdrant: ", resp['choices'][0]['message']['content'])
        return resp['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print("Ошибка при выполнении запроса:", e)
        return "Запрос не распознан"


def reasoning_step_two(query):

    headers = {
        'Authorization': 'Bearer sk-KNo006G2a48UVE3IxFlQEQ'
    }

    payload = { "model": "bge-m3", "input": query}

    try:
        response = requests.post('https://api.gpt.mws.ru/v1/embeddings', json=payload, headers=headers)
        response.raise_for_status()
        resp = response.json()
        print("Knowlege Agent, вектор: ", resp['data'][0]['embedding'])
        embedding = resp['data'][0]['embedding']

        hits_names = client.query_points(
            collection_name="names",
            query=embedding,
            limit=1,
        ).points

        answer_by_name = hits_names[0].payload['content']
        print("Knowlege Agent, найдено в базе знаний по названию статьи: ", answer_by_name)

        hits_content = client.query_points(
            collection_name="content",
            query=embedding,
            limit=1,
        ).points

        answer_by_content = hits_content[0].payload['content']
        print("Knowlege Agent, найдено в базе знаний по содержанию статьи: ", answer_by_content)

        if not (answer_by_name == answer_by_content):
            return f"{answer_by_name} \n  {answer_by_content}"
        else:
            return answer_by_name

    except requests.exceptions.RequestException as e:
        print("Ошибка при выполнении запроса:", e)
        return "Запрос не распознан"



def knowlege_agent(chat, intent):
    rs_1 = reasoning_step_one(chat, intent)
    rs_2 = reasoning_step_two(rs_1)

    return rs_2



