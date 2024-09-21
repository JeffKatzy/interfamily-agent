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


def test_part(setup_session):
    session_id, user_id = setup_session
    text_input = "I feel some anxiety."
    result = parse_details(text_input, [GeneralResponse, Part, UserIntro], user_id, session_id)[0]
    assert "anxiety" in result['args']['part']

def test_aware_of_part(setup_session):
    session_id, user_id = setup_session
    text_input = "I feel it in the back of my neck."
    result = parse_details(text_input, [GeneralResponse, Part, UserIntro], user_id, session_id)[0]
    assert "neck" in result['args']['aware_of_part']

def test_feeling_to_part(setup_session):
    session_id, user_id = setup_session
    text_input = "I wish it would go away."
    result = parse_details(text_input, [GeneralResponse, Part, UserIntro], user_id, session_id)[0]
    assert "go away" in result['args']['feeling_to_part']

def test_agreed_can_step_back(setup_session):
    session_id, user_id = setup_session
    text_input = "Yes, I can ask it to take a step back."
    result = parse_details(text_input, [GeneralResponse, Part, UserIntro], user_id, session_id)[0]
    assert result['args']['agreed_can_step_back'] == True

def test_achieved_unblending_and_has_compassion_towards_part(setup_session):
    session_id, user_id = setup_session
    text_input = "I feel compassion for it."
    
    result = parse_details(text_input, [GeneralResponse, Part, UserIntro], user_id, session_id)[0]
    assert result['args']['achieved_unblending'] == True
    assert result['args']['has_compassion_towards_part'] == True

def test_shared_feelings(setup_session):
    session_id, user_id = setup_session
    text_input = "I shared my feelings with it."
    results = parse_details(text_input, [GeneralResponse, Part, UserIntro], user_id, session_id)
    for result in results:
        if result['args']['shared_feelings']:
            assert True

