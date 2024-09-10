import asyncio

from domain.models.general_response import GeneralResponse
from domain.models.part import Part
from domain.prompt import general_message_prompt
from domain.store import get_session_history
from lib.agent import invoke_message_from
from lib.model_updater import merge, parse_details


class Server:
    def __init__(self, workflows):
        self.workflows = workflows

    def current_workflow(self):
        return self.workflows[-1]

    async def route_from(self, user_message):
        output_json = parse_details(user_message, [Part, GeneralResponse])[0]
        if output_json['type'] == 'GeneralResponse':
            async for chunk in invoke_message_from(general_message_prompt, user_message):
                yield chunk
        else:
            workflow = self.current_workflow()
            workflow._model = merge(workflow.model, output_json['args'])
            next_workflow_msg = workflow.get_next_message() or "Thank the user for the session."
            async for chunk in invoke_message_from(workflow.prompt(), next_workflow_msg):
                yield chunk
    
    async def listen(self):
        ai_text = "Hey there."
        print(ai_text)
        while True:
            text_input = input("\n\nMe: ")
            print("\nBot:")
            async for chunk in self.route_from(text_input):
                print(chunk, end="", flush=True)

    def log(self):
        history = get_session_history(**{"user_id": "123", "conversation_id": "1"})
        print(history.messages[-2:])
        
def build_server():
    workflows = [ PartWorkflow(Part()) ]
    return Server(workflows)