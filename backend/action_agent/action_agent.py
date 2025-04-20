import requests


def reasoning_step_one(chat, intent, emotion):
    intent_query = intent['query']
    intent_precision = intent['precision']
    emotion_emotion = emotion['emotion']
    emotion_cause = emotion['cause']

    system = {"role": "system", "content": f"Ты виртуальный ассистент оператора колл-центра компании сотовой связи. В фирме много различных услуг, тарифов, подписок, сервисов. Твоя задача - написать идеальный ответ клиенту, учитывая историю чата и сопутствующую информацию от предыдущих агентов. Намерение клиента: {intent_query}. Трубется ли уточнение по запросу клиента: {intent_precision}. Эмоция клиента сейчас: {emotion_emotion}. Причина эмоции клиента: {emotion_cause}."}

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
        "max_tokens": 300,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }

    try:
        response = requests.post('https://api.gpt.mws.ru/v1/chat/completions', json=payload, headers=headers)
        response.raise_for_status()
        resp = response.json()
        print("Action Agent, генерация ответа: ", resp['choices'][0]['message']['content'])
        return resp['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print("Ошибка при выполнении запроса:", e)
        return "Запрос не распознан"


def action_agent(chat, intent, emotion):
    rs_1 = reasoning_step_one(chat, intent, emotion)

    return {
        'answer': rs_1
    }

