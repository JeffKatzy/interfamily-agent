import os
import sys
import uuid

import pytest
from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from dotenv import load_dotenv

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)
from domain.models import Part, UserIntro
from domain.server import Server
from domain.session import start_new_session
from domain.store import get_session
from domain.workflows import PartWorkflow, UserIntroWorkflow

load_dotenv()

@pytest.fixture
def setup_session():
    server = Server()
    workflows = [UserIntroWorkflow(UserIntro()), PartWorkflow(Part())]
    user_id = "1"
    session = start_new_session(workflows=workflows, user_id=user_id)
    session_id = session.session_id
    yield session_id, user_id, server

def test_user_intro_and_part_workflow(setup_session):
    session_id, user_id, server = setup_session
    similarity_metric = GEval(name="Similarity",
        evaluation_params=[
            LLMTestCaseParams.ACTUAL_OUTPUT,
            LLMTestCaseParams.EXPECTED_OUTPUT,
        ],
        evaluation_steps=[
            "Assess if there are any discrepancies in information between the actual and expected outputs.",
        ],
    )
    inputs_and_outputs = [("Hi.", "Hello! I'm here to help you explore and practice Internal Family Systems (IFS). Do you have any questions about IFS, or would you like to start a session?"),
    ("Let's start a session.", "Is there a particular feeling, struggle, thought pattern, or part of yourself that you would like some help with today?"),
    ("Yes, I feel some anxiety in the back of my neck", "Thank you for sharing that. It sounds like there's a part of you that's feeling anxiety, and you're noticing it in the back of your neck. How do you feel toward this part? Are you okay with it being there, or do you have other feelings about it?"),
    ("Well I wish it would go away", "It sounds like there's a part of you that wishes the anxiety would go away. Would it be possible for that part to take a step back during our session, so we can get to know the anxiety part a little better?"),
    ("Sure, it can do that.", "Now that the part wishing the anxiety would go away has stepped back, how do you feel toward the anxiety part?"),
    ("Well I feel sympathetic towards it", "Could you take a moment to share these sympathetic feelings with the anxiety part? Let it know how you feel toward it."),
    ("Ok sure, I just let it know", "How did the anxiety part receive the sympathetic feelings you shared with it?"),
    ("Well I think it feels good", "It sounds like the anxiety part appreciated the compassion and understanding you offered. If you'd like, we can continue exploring this part or any other parts that might need attention.")
    ]
    test_cases = []
    for text_input, expected_output in inputs_and_outputs:
        prompt, next_message, session_id = server.get_prompt_and_inputs(text_input, user_id, session_id)
        response = server.invoke(prompt, next_message, user_id, session_id)
        test_case = LLMTestCase(input=text_input, actual_output=response, expected_output=expected_output, context= next_message)
        test_cases.append(test_case)
    
    for test_case in test_cases:
        assert_test(test_case, [similarity_metric])


