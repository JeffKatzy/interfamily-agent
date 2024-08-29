import chainlit as cl
from dotenv import load_dotenv
from langchain.schema import StrOutputParser
from langchain.schema.runnable.config import RunnableConfig

from domain.models.part import Part
from domain.server import Server
from domain.workflows.part_workflow import PartWorkflow


@cl.on_chat_start
async def on_chat_start():    
    # runnable = agent | StrOutputParser()
    server = build_server()
    cl.user_session.set("server", server)

@cl.on_message
async def on_message(message: cl.Message):
    server = cl.user_session.get("server")
    msg = cl.Message(content="")
    async for chunk in server.route_from(message.content):
        await msg.stream_token(chunk)

    await msg.send()

def build_server():
    workflows = [ PartWorkflow(Part()) ]
    return Server(workflows)