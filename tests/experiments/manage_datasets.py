import os
import sys

from langsmith import Client

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)
from dotenv import load_dotenv

from tests.experiments.data import examples

load_dotenv()

client = Client()

def update_or_create(dataset_name, examples):
    dataset = find_dataset_by(dataset_name)
    if dataset:
        update_dataset(dataset, examples)
    else:
        dataset = client.create_dataset(dataset_name)
        create_examples(dataset, examples)
    return dataset_name

def create_examples(dataset, examples):
    client.create_examples(
        inputs=[e["inputs"] for e in examples],
        outputs=[e["outputs"] for e in examples],
        dataset_id=dataset.id,
    )

def update_dataset(dataset, new_examples):
    examples = client.list_examples(dataset_id = dataset.id)
    for example in examples:
        client.delete_example(example_id=example.id)
    inputs = [example["inputs"] for example in new_examples]
    outputs = [example["outputs"] for example in new_examples]
    client.create_examples(inputs=inputs, outputs=outputs, dataset_id=dataset.id)
    
def find_dataset_by(dataset_name):
    datasets = client.list_datasets()
    matching_datasets = [dataset for dataset in datasets if dataset.name == dataset_name]
    if not matching_datasets:
        return
    else:
        return matching_datasets[0]

def list_examples(dataset):
    return [example for example in client.list_examples(dataset_id = dataset.id)]

