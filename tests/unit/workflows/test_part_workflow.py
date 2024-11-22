from unittest.mock import AsyncMock, patch

import pytest
from dotenv import load_dotenv

from domain.server import Server
from domain.session import setup_session
from domain.workflows import (ExplorePartWorkflow, PartWorkflow,
                              TransportPartWorkflow, UnblendingWorkflow,
                              UnburdenPartWorkflow)

load_dotenv()

@pytest.mark.asyncio
async def test_unblending_workflow():
    user_id = "1"
    server = Server()
    session = setup_session(user_id=user_id, workflows=[UnblendingWorkflow])
    session_id = session.session_id
    text_input = "Hi."
    
    prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id, session_id)
    msg = "Ask if there's a feeling, struggle, thought pattern, or part they need help with."
    
    assert next_message == msg
    server.invoke(prompt, next_message, user_id, session_id)
    text_input = "I want to explore my anger"
    prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id)
    assert next_message == "Thank them, mirror using parts language.  Then ask if they're aware of this part and how they sense or are aware of the part in their body."
    text_input = "Yes, I feel some anxiety in the back of my neck"
    prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id)
    assert next_message == "Ask how they feels towards the target part.  For example, are they ok with the part being there?"
    text_input = "Well I wish it would go away."
    prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id)
    assert next_message == "If the user feels negative qualities towards the target part, ask if that part that feels negative to the target part can take a step back during the session so that we can get to know the target part better."

@pytest.mark.asyncio
async def test_part_workflow():
    user_id = "1"
    server = Server()
    with patch('domain.workflows.images.part_description_image.PartDescriptionImage.run', new_callable=AsyncMock) as mock_run:
        session = setup_session(user_id=user_id, workflows=[PartWorkflow])
        session_id = session.session_id
        text_input = "Hi."
        prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id, session_id)
        msg = "Ask the user to describe the part now that they've unblended from it.  Can you see the part - what does it look like, and what is it feeling?"
        assert next_message == msg
        text_input = "It looks like a scared kid."
        prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id, session_id = session_id)
        assert next_message == "Ask the user if if it feels compassion towards this part."
        text_input = "Yes, I feel compassion towards it."
        prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id)
        assert next_message == "Ask the user to share it's compassion, in however way it thinks is best.  For example, the user can give the part a hug, or some kind words.  The user can let the part know that it's not alone, and that the user can care for it."
        text_input = "Ok, I just did."
        prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id)
        assert next_message == "Ask how the part received the shared feelings."

@pytest.mark.asyncio
async def test_explore_part_workflow():
    user_id = "1"
    server = Server()
    
    session = setup_session(user_id=user_id, workflows=[ExplorePartWorkflow])
    session_id = session.session_id
    text_input = "Hi."
    
    prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id)
    
    assert next_message == """Ask the user if the part has anything that it wants the user to know about how it's feeling.
    For example, if it's anxious ask if there's something it wants the user to know about it's anxiety.
    Or are there any memories it would like to share with you."""
    text_input = "Ok, I just shared it a memory."
    prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id)
    assert next_message == """Then tell the user, to tell the part to really let the user get how bad it was for it.
                                                          Have it say or show whatever it needs to trust that the user gets it.
                                                          Let the user feel it and see it and sense it."""
    text_input = "Ok, it just shared a memory."
    prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id)
    assert next_message == """Ask the part if it thinks the user gets how bad it was for it.  Or it can always show the user more."""
    text_input = "No, I think it feels that I get it."
    prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id)
    assert next_message == """If we learn more about the part's feelings, let it know the feelings make sense.
    And have the user ask the part is if it is open to getting out of there where it feels stuck."""

@pytest.mark.asyncio
async def test_transport_part_workflow():
    user_id = "1"
    session = setup_session(user_id=user_id, workflows=[TransportPartWorkflow])
    session_id = session.session_id
    text_input = "Hi."
    server = Server()
    prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id, session_id)
    msg = "Tell the user to ask the part if he is ready to leave that time and place with you, and either go to your place now, or to any fantasy place of the part's choice."
    assert next_message == msg
    text_input = "Ok, it's ready."
    
    prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id, session_id)
    assert next_message == "Ask the user what place the part wants to go to.  Where does the part want to go?"
    text_input = "It wants to go to the beach."
    prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id, session_id)
    assert next_message == "Tell the user to take the part to that place.  Then, ask the user if the part is now in that place."
    text_input = "Yes, it's in the beach."
    prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id, session_id)
    assert next_message == "Ask the user how the part likes being in that place."
    text_input = "It likes it a lot."
    prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id, session_id)
    assert next_message == "Tell the user to tell the part that the part does not need to return to the scene where he was hurt.  And tell the part to tell the user that to tell the part that the user will be taking care of the part now."

@pytest.mark.asyncio
async def test_unburden_part_workflow():
    user_id = "1"
    server = Server()
    session = setup_session(user_id=user_id, workflows=[UnburdenPartWorkflow])
    session_id = session.session_id
    text_input = "Hi."
    prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id, session_id)
    msg = 'Tell the user to ask the part if he is ready to unload the feelings and beliefs he got from back there.  If the user is unsure what this means, tell him we just need his desire to stop carrying negative feelings.'
    assert next_message == msg
    text_input = "ok he's ready."
    prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id, session_id)
    assert next_message == "Ask the user to ask the part where in the body the part carries negative feelings."
    text_input = "It carries negative feelings in my neck."
    prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id, session_id)
    assert next_message == "Ask the user to ask the part what he would like to give these feelings up to: light, water, fire, wind, earth, or anything else."
    text_input = "It wants to give it to the wind."
    prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id, session_id)
    assert next_message == "Tell the user to bring in that force described earlier (for example, light, water, fire, wind, earth, etc.) to the part in the body where the part carries negative feelings.  And that the force can take it the feelings away, and that there is no need to carry it anymore."
    text_input = "Ok, it's done."
    prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id, session_id)
    assert next_message == "Ask the user how the part is doing with unloading the negative feelings.  If the part is not doing ok, see if there is anything else the user can do for it."
    text_input = "It's doing ok."
    prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id, session_id)
    
    assert next_message == "Tell the user to tell the part, that if the part wants to, the part can invite new qualities into the part's body that the part would like to have."
    text_input = "Ok, I invited some new qualities."
    prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id, session_id)
    assert next_message == "Ask the user how the part seems now."
    text_input = "It seems better."
    prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id, session_id)
    assert next_message == "Tell the user, if the user wants to, the user can invite other parts to come in and see the unburdened part."
    text_input = "Ok, I invited some other parts."
    prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id, session_id)
    assert next_message == "Ask the user if it feels complete now."
