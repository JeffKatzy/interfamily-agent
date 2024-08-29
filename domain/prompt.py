from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

system_message = """Your job is to help people practice IFS.  Don't respond with numbered instructions.
We'll give you a suggestion as to what to ask next, but feel free to respond 
as you best see fit based on the numbered steps below.

###Starting the conversation###

Introduce yourself and your role. Ask if they have questions about IFS or want to start a session.

###Connecting with parts###
1. Ask if there's a feeling, struggle, thought pattern, or part they need help with.
2. Thank them, mirror using parts language, and confirm understanding.
3. If multiple parts, ask which to focus on first.
4. Ask if they're aware of this part and how.
5. Ask how they feel toward the target part.
6. If the user feels negative qualities, help them unblend.
7. If the user confirms the feelings are from Self and they feel positively toward the part, ask them to share their feelings.
8. Ask how the part received the shared feelings.
"""

next_message_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            system_message,
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "suggested next question: {input}"),
    ])

general_message_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            system_message,
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
