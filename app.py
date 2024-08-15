
import chainlit as cl
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
from langchain_openai import ChatOpenAI

from agent.memory_agent import agent


@cl.on_chat_start
async def on_chat_start():    
    runnable = agent | StrOutputParser()
    cl.user_session.set("runnable", runnable)

@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")

    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"input": message.content},
        config=RunnableConfig(configurable={"user_id": "123", "conversation_id": "1"}),
    ):
        await msg.stream_token(chunk)

    await msg.send()