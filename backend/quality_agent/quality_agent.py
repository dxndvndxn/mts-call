import requests


rules = ("1. Ответы должны быть только по тематике деятельности компании"
         "2. Нельзя обсуждать политику"
         "3. Нельзя обсуждать религию"
         "4. Нельзя хамить клиенту"
         "5. Если запрос клиента не ясен, нужно уточнить у клиента, что он имеет в виду, предложив ему наиболее подходящие варианты из базы знаний")


def reasoning_step_one(chat, intent, emotion, action, rules):

    intent_query = intent['query']
    emotion_emotion = emotion['emotion']
    emotion_cause = emotion['cause']
    action = action['answer']

    system = {
        "role": "system",
        "content": f"Ты виртуальный ассистент оператора колл-центра компании сотовой связи. В фирме много различных услуг, тарифов, подписок, сервисов. Твоя задача - проверять сообщения оператора оператора на соответствие стандартов и правил общения, принятых в компании. Проанилизируй диалог и сопутствующие данные и в ответе напиши нарушенные пункты правил, если такие найдутся. Если нарушений нет, напиши, что нарушений нет. Не пиши ничего лишнего, только выводы по нарушениям правил. Запрос клиента: {intent_query}. Эмоция клиента: {emotion_emotion}. Причина эмоции клиента: {emotion_cause}. Сообщение, котороже нужно проверить на соответствие правилам перед отправкой: {action}. Правила, на соответствие которым нужно проверить сообщение: {rules}. Не пиши ничего, кроме ответа."
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
    }

    try:
        response = requests.post('https://api.gpt.mws.ru/v1/chat/completions', json=payload, headers=headers)
        response.raise_for_status()
        resp = response.json()
        print("Quality Agent, проверка на нарушение правил: ", resp['choices'][0]['message']['content'])
        return resp['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print("Ошибка при выполнении запроса:", e)
        return "Запрос не распознан"


def reasoning_step_two(chat, intent, emotion, action, rs_1, knowlege):

    intent_query = intent['query']
    emotion_emotion = emotion['emotion']
    emotion_cause = emotion['cause']
    action = action['answer']

    system = {
        "role": "system",
        "content": f"Ты виртуальный ассистент оператора колл-центра компании сотовой связи. В фирме много различных услуг, тарифов, подписок, сервисов. Твоя задача - исправлять и улучшать сообщение оператора, если это требуется после проверки его сообщения на соблюдение стандартов общения. Проанализируй контекст диалога и сопутствующую информацию и напиши в ответе исправленное сообщение оператора. Запрос клиента: {intent_query}. Эмоция клиента: {emotion_emotion}. Причина эмоции клиента: {emotion_cause}. Информация из базы знаний по теме запроса клиента: {knowlege}. Сообщение оператора, которое нужно исправить, если выявлены нарушения правил коммуникации: {action}. Результат проверки сообщения на нарушения: {rs_1}. В ответе напиши только сообщение, которое нужно отправить. Дай подробный ответ клиенту. "
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
        "max_tokens": 600,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }

    try:
        response = requests.post('https://api.gpt.mws.ru/v1/chat/completions', json=payload, headers=headers)
        response.raise_for_status()
        resp = response.json()
        print("Quality Agent, исправленное сообщение: ", resp['choices'][0]['message']['content'])
        return resp['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print("Ошибка при выполнении запроса:", e)
        return "Запрос не распознан"


def quality_agent(chat, intent, emotion, action, knowlege):
    rs_1 = reasoning_step_one(chat, intent, emotion, action, rules)
    rs_2 = reasoning_step_two(chat, intent, emotion, action, rs_1, knowlege)

    response = {
        'answer': rs_2,
        'quality': rs_1,
    }
    return response



