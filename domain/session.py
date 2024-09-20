import uuid

from langchain_community.chat_message_histories import ChatMessageHistory

from domain.models.part import Part
from domain.models.user_intro import UserIntro
from domain.store import add_session_to_store, get_session
from domain.workflows import PartWorkflow, UserIntroWorkflow, UserOutroWorkflow


class Session:
    def __init__(self, user_id, session_id, workflows, history):
        self.workflows = workflows
        self.user_id = user_id
        self.session_id = session_id
        self.history = history
        self.ended = False
        self._current_workflow = workflows[0]

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def get_current_workflow(self):
        current_index = self.workflows.index(self._current_workflow)
        if self._current_workflow.is_done() and self.is_next_workflow(current_index):
            self._current_workflow = self.workflows[current_index + 1]
        return self._current_workflow

    def is_next_workflow(self, current_index):
        next_index = current_index + 1
        return next_index < len(self.workflows)

    def set_current_workflow(self, workflow):
        self._current_workflow = workflow

def start_new_session(user_id: str, session_id: str = "", workflows = []):
    workflows = workflows or [ UserIntroWorkflow(UserIntro()), PartWorkflow(Part()) ]
    session_id = session_id or str(uuid.uuid4())

    session = Session(user_id, session_id, workflows, ChatMessageHistory())
    add_session_to_store(session)
    return session

def find_or_create_session(user_id: str, session_id: str = ""):
    if session := get_session(user_id, session_id):
        if not session.ended:
            return session
    return start_new_session(user_id, session_id)

