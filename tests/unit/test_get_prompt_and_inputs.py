from dotenv import load_dotenv

from domain.models import Part, UserIntro
from domain.server import Server
from domain.session import start_new_session
from domain.store import get_session
from domain.workflows import PartWorkflow, UserIntroWorkflow

load_dotenv()


def test_user_intro_workflow_and_properly_exits_when_done():
    
    workflows = [UserIntroWorkflow(UserIntro())]
    user_id = "1"
    server = Server()
    session = start_new_session(workflows=workflows, user_id=user_id)
    session_id = session.session_id
    
    text_input = "Hi."
    prompt, next_message, session_id = server.get_prompt_and_inputs(text_input, user_id, session_id)
    msg = 'Introduce yourself and your role as an IFS coach. Ask if they have questions about IFS or want to start a session.'
    assert next_message == msg
    server.invoke(prompt, next_message, user_id, session_id)
    text_input = "Let's start a session"
    prompt, next_message, session_id = server.get_prompt_and_inputs(text_input, user_id)
    assert next_message == 'Thank user for the session.'

def test_get_prompt_and_inputs_for_user_intro_and_part_workflow():
    server = Server()
    workflows = [UserIntroWorkflow(UserIntro()), PartWorkflow(Part())]
    user_id = "1"
    session = start_new_session(workflows=workflows, user_id=user_id)
    session_id = session.session_id
    
    text_input = "Hello"
    
    prompt, next_message, session_id = server.get_prompt_and_inputs(text_input, user_id, session_id)
    msg = 'Introduce yourself and your role as an IFS coach. Ask if they have questions about IFS or want to start a session.'
    assert next_message == msg
    server.invoke(prompt, next_message, user_id, session_id)
    text_input = "Let's start a session"
    prompt, next_message, session_id = server.get_prompt_and_inputs(text_input, user_id)
    msg = "Ask if there's a feeling, struggle, thought pattern, or part they need help with."
    assert next_message == msg
    text_input = "Yes, I feel some anxiety in the back of my neck"
    prompt, next_message, session_id = server.get_prompt_and_inputs(text_input, user_id)
    msg = "Ask how they feels towards the target part.  For example, are they ok with the part being there?"
    assert next_message == msg
    text_input = "If I'm being honest, I would prefer that it wasn't there."
    prompt, next_message, session_id = server.get_prompt_and_inputs(text_input, user_id)
    
    msg = "If the user feels negative qualities towards the target part, ask if that part that feels negative to the target part can take a step back during the session so that we can get to know the target part better."
    assert next_message == msg
    text_input = "Ok, I can do that."

    prompt, next_message, session_id = server.get_prompt_and_inputs(text_input, user_id)
    msg = "Ask how the user feels now that they've unblended from the part."
    assert next_message == msg
    text_input = "Ok, well now I feel bad for that part."
    prompt, next_message, session_id = server.get_prompt_and_inputs(text_input, user_id)
    msg = "If the user confirms the feelings are from Self, ask them to share their feelings with the part"
    assert next_message == msg
    text_input = "Ok, sure."
    prompt, next_message, session_id = server.get_prompt_and_inputs(text_input, user_id)
    msg = "Ask how the part received the shared feelings."
    assert next_message == msg
    