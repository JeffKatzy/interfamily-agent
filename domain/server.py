from domain.models import GeneralResponse, Part, Unblending, UserIntro
from domain.prompt import general_message_prompt
from domain.session import find_or_create_session
from lib.agent import build_chain
from lib.base_workflow import Step
from lib.model_updater import merge, parse_details


class Server:
    async def get_prompt_and_inputs(self, user_message, user_id, session_id = ''):
        session = find_or_create_session(user_id, session_id)
        session_id = session.session_id
        route_classes = [GeneralResponse] + [type(session.get_current_workflow().model)]
        
        output_json = parse_details(user_message, route_classes=route_classes,
                                   user_id=user_id, session_id=session_id)[0]
        prompt, next_message = await self.route_from(output_json,
                                                      user_message,
                                                      session)
        return prompt, next_message, session_id

    async def invoke_stream(self, prompt, next_message, user_id, session_id):
        chain = build_chain(prompt)
        print('calling invoke stream')
        
        async for chunk in chain.astream({"input": next_message},
            config={"configurable": {"user_id": user_id, "session_id": session_id}}):
            yield chunk

    def invoke(self, prompt, next_message, user_id, session_id):
        chain = build_chain(prompt)
        return chain.invoke({"input": next_message},
            config={"configurable": {"user_id": user_id, "session_id": session_id}})
            

    async def route_from(self, output_json, user_message, session):
        
        next_workflow_step = await self.get_next_step(session, output_json)
        next_workflow_step.invoked += 1
        print(output_json['type'])
        if output_json['type'] == 'GeneralResponse':
            workflow_prompt = general_message_prompt
        else:
            workflow_prompt = session.get_current_workflow().prompt()
        return workflow_prompt, next_workflow_step.prompt

    async def get_next_step(self, session, output_json):
        current_workflow = session.get_current_workflow()
        current_workflow._model = merge(current_workflow.model, output_json['args'])
        print('current_model',  current_workflow.model.__class__.__name__, current_workflow.model.dict())
        updated_workflow = session.get_current_workflow()
        next_workflow_step = await updated_workflow.get_next_step() or Step(prompt="Thank user for the session.")
        return next_workflow_step
    
    async def listen(self):
        user_id = '1'    
        while True:
            text_input = input("\n\nMe: ")
            print("\nBot:")
            user_id = '1'
            prompt, next_message, session_id = await self.get_prompt_and_inputs(text_input, user_id)
            print('next_message', next_message)
            
            async for chunk in self.invoke_stream(prompt, next_message, user_id, session_id):
                print(chunk, end="", flush=True)
