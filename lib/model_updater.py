import json

from langchain.output_parsers import PydanticOutputParser
from langchain.output_parsers.openai_tools import JsonOutputToolsParser
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_core.runnables.history import RunnableWithMessageHistory

from domain.prompt import parse_details_prompt
from domain.store import get_session_history
from lib.agent import build_runnable, llm


def merge(current_details, new_details):
    non_empty_details = {k: v for k, v in new_details.items() if v not in [None, ""]}
    updated_details = current_details.copy(update=non_empty_details)
    return updated_details
    
def parse_details(text_input, route_classes, user_id, session_id):

    runnable = parse_details_prompt | llm.bind_tools(route_classes, tool_choice="any")
    runnable_with_history = build_runnable(runnable, "input")
    parser = JsonOutputToolsParser()
    chain = runnable_with_history | parser
    runnable_res = runnable_with_history.invoke(
        {"input": text_input},
        config={"configurable": {"user_id": user_id, "session_id": session_id}}
    )
    add_tool_message(runnable_res, user_id, session_id)
    return parser.invoke(runnable_res)

def add_tool_message(runnable_res, user_id, session_id):
    for tool_call in runnable_res.tool_calls:
        content = json.dumps(tool_call['args'])
        tool_message = ToolMessage(content = content,
                    tool_call_id = tool_call['id'])
        history = get_session_history(user_id, session_id)
        history.messages.append(tool_message)
