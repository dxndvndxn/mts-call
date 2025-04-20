from emotional_agent import emotional_agent
from intent_agent import intent_agent
from action_agent import action_agent

def core_agent(chat):
    intent = intent_agent.intent_agent(chat)
    emotion = emotional_agent.emotional_agent(chat)
    action = action_agent.action_agent(chat, intent, emotion)

    return {
        'action': action,
        'emotion': emotion
    }
