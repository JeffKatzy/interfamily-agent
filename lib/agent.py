from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from domain.store import get_session, get_session_history

load_dotenv()

# fine_tune_model = "ft:gpt-4o-mini-2024-07-18:personal::A77fNj6o"
model_id = "gpt-4o-2024-08-06"
llm = ChatOpenAI(temperature=0, model=model_id, streaming=True)

def build_chain(prompt):
    qa_chain = prompt | llm
    chain = build_runnable(qa_chain, "input")
    str_chain = chain | StrOutputParser()
    return str_chain
        

def build_runnable(chain, messages_key):
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

