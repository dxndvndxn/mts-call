import requests


def reasoning_step_one(chat):
    system = {
        "role": "system",
        "content": "Ты виртуальный ассистент оператора колл-центра компании сотовой связи. Твоя задача - подводить итоги диалога. Проанализируй диалог и намерение клиента и верно классифицируй тип диалога. Варианты ответа:  1. Жалоба  2. Информирование  3. Подключение услуги  4. Отключение услуги. В ответе напиши только тип запроса. Не пиши ничего лишнего."
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
        print("Summary Agent, распознание типа обращения: ", resp['choices'][0]['message']['content'])
        return resp['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print("Ошибка при выполнении запроса:", e)
        return "Запрос не распознан"


def reasoning_step_two(chat):
    system = {
        "role": "system",
        "content": "Ты виртуальный ассистент оператора колл-центра компании сотовой связи. Твоя задача - подводить итоги диалога. Проанализируй диалог и намерение клиента и верно классифицируй итоги диалога. Варианты ответа:  1. Информирование проведено  2. Услуга подключена  3. Услуга отключена  4. Проблема решена  5. Ухудшение ситуации. В ответе напиши только один из предложенных вариантов. Не пиши ничего лишнего."
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
        print("Summary Agent, распознание итогов обращения: ", resp['choices'][0]['message']['content'])
        return resp['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print("Ошибка при выполнении запроса:", e)
        return "Запрос не распознан"


def summary_agent(chat, emotion):
    rs_1 = reasoning_step_one(chat)
    rs_2 = reasoning_step_one(chat)
    response = {
        'type': rs_1,
        'emotion': emotion['emotion'],
        'final': rs_2
    }
    return response



