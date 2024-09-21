import os
import sys
import uuid

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)
from dotenv import load_dotenv

load_dotenv()
from data import examples, multiturn_examples
from langchain_community.adapters.openai import convert_openai_messages
from langchain_core.prompts import ChatPromptTemplate
from langsmith import Client
from langsmith.evaluation import LangChainStringEvaluator, evaluate
from langsmith.schemas import Example, Run

from domain.prompt import next_message_prompt
from domain.session import find_or_create_session
from domain.store import get_session_history
from lib.agent import build_chain
from tests.experiments.manage_datasets import update_or_create

client = Client()

def multiturn_predict(inputs: dict):
    user_id = '1'
    session_id = '1'
    chain = build_chain(next_message_prompt)
    response = chain.invoke({"input": inputs["input"], "messages": convert_openai_messages(inputs["messages"])},
    config={"configurable": {"user_id": user_id, "session_id": session_id}})
    return response

def format_evaluator_inputs(run: Run, example: Example):
    return {
        "input": example.inputs["input"],
        "prediction": next(iter(run.outputs.values())),
        "reference": example.outputs["answer"],
    }

def assess_chain_outputs():
    dataset_name = "Multiturn IFS"
    # update_or_create(dataset_name, examples)
    correctness_evaluator = LangChainStringEvaluator("string_distance",
    config={"distance": "levenshtein", "normalize_score": True},
    prepare_data=format_evaluator_inputs)    
    evaluate(
            multiturn_predict,
            data=dataset_name,
            experiment_prefix="Single-Turn IFS",
            evaluators=[correctness_evaluator],
            metadata={"model": "gpt-3.5-turbo"})

if __name__ == '__main__':
    pass
    # assess_chain_outputs()