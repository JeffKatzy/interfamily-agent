import os
import sys
import uuid
from datetime import datetime, timedelta

from langsmith import Client

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from dotenv import load_dotenv

load_dotenv()
client = Client()

def get_runs_by_session_id(session_id, project_name = "ifs-development"):
    return list(client.list_runs(
    project_name=project_name,
    filter=f"and(eq(metadata_key, 'session_id'), eq(metadata_value, '{session_id}'))"
    ))

def get_message_runs(runs):
    message_runs = []
    for run in runs:
        if "messages" in run.inputs or run.outputs:        
            message_runs.append(run)
    return message_runs

def get_all_run_types(runs):
    run_types = set()
    for run in runs:
        run_types.add(run.run_type)
    return run_types

def get_messages(message_runs):
    for message_run in message_runs:
        if messages := message_run.inputs.get('messages'):
            break
    selected_messages = []
    for message in messages:
        kwargs = message['kwargs']
        if 'tool_calls' in kwargs or kwargs['content'] == '' or kwargs['type'] == 'tool':
            continue
        selected_messages.append(kwargs)
    return selected_messages
        
def get_run_by_id(run_ids):
    return list(client.list_runs(id=run_ids))[0]

def get_messages_from_run_ids(run_ids):
    run = get_run_by_id(run_ids = run_ids)
    session_id = run.extra['metadata']['session_id']
    runs_by_session_id = get_runs_by_session_id(session_id)
    message_runs = get_message_runs(runs_by_session_id)
    messages = get_messages(message_runs)
    return messages

if __name__ == '__main__':
    run_ids = ["c110fd90-e8d5-4078-ab63-315f6530e683"]
    messages = get_messages_from_run_ids(run_ids)