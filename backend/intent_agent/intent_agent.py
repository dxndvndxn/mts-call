import requests
import logging

logger = logging.getLogger("uvicorn.error")

def reasoning_step_one(chat):
    system = {
        "role": "system",
        "content": "Ты виртуальный ассистент оператора колл-центра компании сотовой связи. В фирме много различных услуг, тарифов, подписок, сервисов. Твоя задача - определять, насколько по сообщениям клиента понятно, чего он хочет. В ответе напиши 'Запрос клиента понятен', если вопросов нет, и 'Требует уточнения', если запрос клиента можно трактовать по-разному (например, не уточняется тариф, услуга, сервис, подписка). Если запрос требует уточнения, напиши, что конкретно нужно уточнить. Следующий агент будет использовать эту информацию для поиска в базе знаний. Не пытайся решить проблему, выполни только свою функцию."
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
        print("Intent Agent, проверка полноты запроса: ", resp['choices'][0]['message']['content'])
        logger.info("Intent Agent, проверка полноты запроса: ", resp['choices'][0]['message']['content'])
        return resp['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print("Ошибка при выполнении запроса:", e)
        logger.info("Ошибка при выполнении запроса:", e)
        return "Запрос не распознан"
def reasoning_step_two(chat):
    system = {
        "role": "system",
        "content": "Ты виртуальный ассистент оператора колл-центра компании сотовой связи. В фирме много различных услуг, тарифов, подписок, сервисов. Твоя задача - определять запрос-намерение клиента. В ответ напиши только намерение клиента, следующий агент будет использовать эту информацию для поиска в базе знаний."
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
        "temperature": 0.6,
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
        print("Intent Agent, классификация запроса клиента: ", resp['choices'][0]['message']['content'])
        logger.info("Intent Agent, классификация запроса клиента: ", resp['choices'][0]['message']['content'])

        return resp['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print("Ошибка при выполнении запроса:", e)
        logger.info("Ошибка при выполнении запроса:", e)
        return "Запрос не распознан"

def intent_agent(chat):
    rs_1 = reasoning_step_one(chat)
    rs_2 = reasoning_step_two(chat)

    return {
        'query': rs_2,
        'precision': rs_1
    }

