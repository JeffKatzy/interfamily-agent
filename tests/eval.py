import os
import sys
import uuid

from langsmith import Client

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from dotenv import load_dotenv

load_dotenv()
uid = uuid.uuid4()
client = Client()
import os

# OPENAI_API_KEY=
from dotenv import load_dotenv
from example_data import examples

load_dotenv()


from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

# An example chain
chain = (
    ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful tutor AI."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
        ]
    )
    | ChatOpenAI(model="gpt-3.5-turbo")
    | StrOutputParser()
)

from langchain_community.adapters.openai import convert_openai_messages
from langsmith.evaluation import LangChainStringEvaluator, evaluate
from langsmith.schemas import Example, Run


def predict(inputs: dict):
    # Add a step to convert the data from the dataset to a form the chain can consume
    return chain.invoke(
        {
            "input": inputs["question"],
            "chat_history": convert_openai_messages(inputs["chat_history"]),
        }
    )


def format_evaluator_inputs(run: Run, example: Example):
    return {
        "input": example.inputs["question"],
        "prediction": next(iter(run.outputs.values())),
        "reference": example.outputs["expected"],
    }


correctness_evaluator = LangChainStringEvaluator(
    "cot_qa",
    prepare_data=format_evaluator_inputs,
)
dataset_name = 'Single-Turn IFS e3757d1b-ad67-4b22-b20b-7a8060606650'
results = evaluate(
    predict,
    data=dataset_name,
    experiment_prefix="Chat Single Turn",
    evaluators=[correctness_evaluator],
    metadata={"model": "gpt-3.5-turbo"},
)