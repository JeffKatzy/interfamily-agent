import os
import sys
import uuid

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from dotenv import load_dotenv

load_dotenv()
from data import examples, multiturn_examples
# from example_data import examples, multiturn_examples
from langchain_community.adapters.openai import convert_openai_messages
from langchain_core.prompts import ChatPromptTemplate
from langsmith import Client
from langsmith.evaluation import LangChainStringEvaluator, evaluate
from langsmith.schemas import Example, Run

from domain.prompt import next_message_prompt
from domain.session import find_or_create_session
from domain.store import get_session_history
from lib.agent import build_chain

client = Client()

def build_prompt():
    url = client.push_prompt("ifs-next-message-prompt", object=next_message_prompt)
    return url

def build_dataset(examples):
    uid = uuid.uuid4()
    dataset_name = f"Multiturn IFS"
    dataset = client.create_dataset(dataset_name)
    client.create_examples(
        inputs=[e["inputs"] for e in examples],
        outputs=[e["outputs"] for e in examples],
        dataset_id=dataset.id,
    )
    return dataset_name



# def predict(inputs: dict):
#     user_id = "123"
#     session_id = str(uuid.uuid4())
#     session = find_or_create_session(user_id, session_id)
#     session_id = session.session_id
#     messages = convert_openai_messages(inputs["chat_history"])
#     response = chain.invoke({"input": inputs["question"], "messages": messages},
#     config={"configurable": {"user_id": user_id, "session_id": session_id}})
#     return response

def multiturn_predict(inputs: dict):
    user_id = "123"
    session_id = "1"
    # session = find_or_create_session(user_id, session_id)
    # session_id = session.session_id
    # chain = build_chain(next_message_prompt)
    # history_messages = get_session_history(user_id, session_id).messages
    
    response = chain.invoke({"input": inputs["input"], "messages": messages})
    
    return response

def format_evaluator_inputs(run: Run, example: Example):
    return {
        "input": example.inputs["input"],
        "prediction": next(iter(run.outputs.values())),
        "reference": example.outputs["answer"],
    }



correctness_evaluator = LangChainStringEvaluator("string_distance",
 config={"distance": "levenshtein", "normalize_score": True},
 prepare_data=format_evaluator_inputs)

dataset_name = "Multiturn IFS" 
evaluate(
        multiturn_predict,
        data=dataset_name,
        experiment_prefix="Single-Turn IFS",
        evaluators=[correctness_evaluator],
        metadata={"model": "gpt-3.5-turbo"})
