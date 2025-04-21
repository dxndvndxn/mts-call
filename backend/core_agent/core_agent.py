from emotional_agent import emotional_agent
from intent_agent import intent_agent
from action_agent import action_agent
from knowlege_agent import knowlege_agent
from quality_agent import quality_agent
from summary_agent import summary_agent

def core_agent(chat):
    intent = intent_agent.intent_agent(chat)
    emotion = emotional_agent.emotional_agent(chat)
    knowledge = knowlege_agent.knowlege_agent(chat, intent)
    action = action_agent.action_agent(chat, intent, emotion, knowledge)
    quality = quality_agent.quality_agent(chat, intent, emotion, action, knowledge)
    summary = summary_agent.summary_agent(chat, emotion)

    return {
        'action': quality,
        'emotion': emotion,
        'knowledge': knowledge,
        'summary': summary
    }
