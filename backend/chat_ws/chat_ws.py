import json
from fastapi import WebSocket
from core_agent import core_agent
import logging

logger = logging.getLogger("uvicorn.error")

# Список подключенных клиентов
connected_clients = []

# Очередь сообщений
message_queue = []

async def chat_ws(websocket: WebSocket, username):
    await websocket.accept()
    logger.info(username)

    connected_client = {
        "websocket": websocket,
        "username": username
    }
    connected_clients.append(connected_client)

    try:
        # Отправляем сообщения из очереди (если они есть)
        for message in message_queue:
            await websocket.send_text(json.dumps(message))

        while True:
            receive_text = await websocket.receive_text()

            if receive_text == "clearDialog":
                message_queue.clear()
                for client in connected_clients:
                    await client["websocket"].send_text(json.dumps({
                        "clearDialog": True
                    }))
            else:
                message_data = {
                    "role": username,
                    "content": receive_text
                }

                # Добавляем сообщение в очередь
                message_queue.append(message_data)

                logger.info(message_data)

                # Отправляем сообщение всем подключенным клиентам
                for client in connected_clients:
                    await client["websocket"].send_text(json.dumps(message_data))

                if len(message_queue) > 0 and message_queue[-1]['role'] == 'user':
                    agents_response = core_agent.core_agent(message_queue)
                    response = {
                       "operator": {
                          **agents_response
                       }
                    }

                    for client in connected_clients:
                        if client['username'] == 'operator':
                            await client["websocket"].send_text(json.dumps(response))
    except Exception as e:
        logger.info('chat_ws: ', e)
        connected_clients.remove(connected_client)
