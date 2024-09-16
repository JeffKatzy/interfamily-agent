from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from domain.store import get_session, get_session_history

load_dotenv()
fine_tune_model = "" #"ft:gpt-4o-mini-2024-07-18:personal::A76mvjnr"
# model_id = "ft:gpt-4o-mini-2024-07-18:personal::A77fNj6o"
model_id = "gpt-4o-2024-08-06"
llm = ChatOpenAI(temperature=0, model=model_id, streaming=True)

async def invoke_message_from(prompt, input_message, user_id, session_id):
        info_gathering_chain = prompt | llm
        chain = build_message_chain(info_gathering_chain, "input")
        str_chain = chain | StrOutputParser()
        
        async for chunk in str_chain.astream(
            {"input": input_message},
            config={"configurable": {"user_id": user_id, "session_id": session_id}}):
            yield chunk

def build_message_chain(chain, messages_key):
    return RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key=messages_key,
        history_messages_key="messages",
        history_factory_config=[
        ConfigurableFieldSpec(
            id='user_id',
            annotation=str,
            name='User ID',
            description='Unique identifier for the user.',
            default='',
            is_shared=True,
        ),
        ConfigurableFieldSpec(
            id="session_id",
            annotation=str,
            name="Session ID",
            description="Unique identifier for the session.",
            default="",
            is_shared=True,
        ),
        ]
    )

