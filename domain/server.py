import asyncio

from domain.models.general_response import GeneralResponse
from domain.models.part import Part
from domain.models.user_intro import UserIntro
from domain.prompt import general_message_prompt
from domain.session import find_or_create_session
from lib.agent import invoke_message_from
from lib.model_updater import merge, parse_details


class Server:
    async def get_response_from(self, user_message, user_id, session_id = ''):
        session = find_or_create_session(user_id, session_id)
        session_id = session.session_id
        output_json = parse_details(user_message, [UserIntro, Part, GeneralResponse], user_id, session_id)[0]
        
        prompt, next_message = self.route_from(output_json, user_message, session)

        async for chunk in invoke_message_from(prompt, next_message,  user_id, session_id):
            yield chunk

    def route_from(self, output_json, user_message, session):
        if output_json['type'] == 'GeneralResponse':
            return general_message_prompt, user_message
        else:
            prompt, next_message = self.build_prompt_and_message(session, output_json)
            return prompt, next_message

    def build_prompt_and_message(self, session, output_json):
        workflow = session.get_current_workflow()
        workflow._model = merge(workflow.model, output_json['args'])
        next_workflow_msg = workflow.get_next_message() or "Thank the user for the session."
        return workflow.prompt(), next_workflow_msg

    async def listen(self):
        user_id = '1'
        # async for chunk in self.route_from(text_input, user_id):
        #     print(chunk, end="", flush=True)
        while True:
            text_input = input("\n\nMe: ")
            print("\nBot:")
            user_id = '1'
            async for chunk in self.get_response_from(text_input, user_id):
                print(chunk, end="", flush=True)
