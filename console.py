from agent.memory_agent import agent


def respond(input_text):
    return agent.invoke(
    {"input": input_text},
    config={"configurable": {"user_id": "123", "conversation_id": "1"}})
    




