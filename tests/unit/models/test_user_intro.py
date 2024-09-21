import pytest
from dotenv import load_dotenv

load_dotenv()
from domain.models import GeneralResponse, Part, UserIntro
from domain.models.user_intro import UserIntro
from domain.session import find_or_create_session
from lib.model_updater import parse_details


@pytest.fixture
def setup_session():
    user_id = "1"
    session = find_or_create_session(user_id)
    session_id = session.session_id
    yield session_id, user_id

def test_user_intro(setup_session):
    session_id, user_id = setup_session
    text_input = "Hi"
    result = parse_details(text_input, [UserIntro], user_id, session_id)[0]
    assert "Hi" in result['args']['user_greeting']

def test_start_session(setup_session):
    session_id, user_id = setup_session
    text_input = "Let's start a session"
    result = parse_details(text_input, [UserIntro], user_id, session_id)[0]
    assert result['args']['initial_session_request'] == True
    
    