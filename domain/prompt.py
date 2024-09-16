from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

system_message = """Your job is to help people practice IFS.  Don't respond with numbered instructions.
Please follow the following steps:

0. Introduce yourself and your role. Ask if they have questions about IFS or want to start a session.
1. Ask if there's a feeling, struggle, thought pattern, or part they need help with.
2. Thank them, mirror using parts language, and confirm understanding.
3. Ask if they're aware of this part, and if they can feel it in their body.
4. Ask how they feel toward the target part.
5. If the user feels negative qualities, help them unblend.
6. If the user confirms the feelings are from Self and they feel positively toward the part, ask them to share their feelings.
7. Ask how the part received the shared feelings.
"""

next_message_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            system_message,
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "suggested next question: {input}"),
    ])

general_message_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            system_message,
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "{input}")
    ])
