
import pytest
from dotenv import load_dotenv

load_dotenv()
from domain.models import GeneralResponse, Part, UserIntro
from domain.session import find_or_create_session
from lib.model_updater import parse_details


@pytest.fixture
def setup_session():
    user_id = "123"
    session_id = "456"
    session = find_or_create_session(user_id, session_id)
    session_id = session.session_id
    yield session_id, user_id
    
def test_parse_details_detects_greetings(setup_session):
    session_id, user_id = setup_session
    user_messages = ["Hi", "Hello", "Hey"]
    output_types = []
    for user_message in user_messages:
        output_type = parse_details(user_message, [UserIntro, Part, GeneralResponse],
                                   user_id, session_id)[0]['type']
        output_types.append(output_type)
    assert all(output_type == 'UserIntro' for output_type in output_types)

def test_parse_details_detects_questions(setup_session):
    session_id, user_id = setup_session
    user_messages = ["What is IFS?", "Why should I do that?", "I don't like that."]
    output_types = []
    for user_message in user_messages:
        output_type = parse_details(user_message, [UserIntro, Part, GeneralResponse],
                                   user_id, session_id)[0]['type']
        output_types.append(output_type)
    assert all(output_type == 'GeneralResponse' for output_type in output_types)