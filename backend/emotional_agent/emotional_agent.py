import requests


def reasoning_step_one(chat):
    system = {
        "role": "system",
        "content": "Ты виртуальный ассистент оператора колл-центра компании сотовой связи. В фирме много различных услуг, тарифов, подписок, сервисов. Твоя задача - следить за эмоциональным состоянием клиента. Проанализируй диалог и скажи, в каком из трёх состояний сейчас находится клиент: позитивное, нейтральное, негативное. В ответе напиши только 1 слово (позитивное, нейтральное, негативное). Не пиши ничего кроме эмоционального состояния."
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
        print("Emotion Agent, распознание эмоции: ", resp['choices'][0]['message']['content'])
        return resp['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print("Ошибка при выполнении запроса:", e)
        return "Запрос не распознан"

def reasoning_step_two(chat, rs_1):
    system = {"role": "system", "content": f"Ты виртуальный ассистент оператора колл-центра компании сотовой связи. В фирме много различных услуг, тарифов, подписок, сервисов. Твоя задача - определять, что вызвало {rs_1} эмоциональное состояние клиента. Проанализируй диалог и напиши только причину эмоционального состояния. Не пытайся решить проблему клиента. Ты должен написать только причину эмоционального состояния клиента."}

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
        print("Emotion Agent, причина эмоции: ", resp['choices'][0]['message']['content'])
        return resp['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print("Ошибка при выполнении запроса:", e)
        return "Запрос не распознан"

def emotional_agent(chat):
    rs_1 = reasoning_step_one(chat)
    rs_2 = reasoning_step_two(chat, rs_1)
    response = {
        'emotion': rs_1,
        'cause': rs_2,
    }
    return response



