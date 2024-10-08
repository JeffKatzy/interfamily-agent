import uuid

from langchain_community.chat_message_histories import ChatMessageHistory

from domain.models import Part, Unblending, UserIntro
from domain.store import add_session_to_store, get_session
from domain.workflows import (PartWorkflow, UnblendingWorkflow,
                              UserIntroWorkflow)


class Session:
    def __init__(self, user_id, session_id, workflows = [], history = ChatMessageHistory()):
        self.workflows = workflows
        self.user_id = user_id
        self.session_id = session_id
        self.history = history
        self.ended = False
        
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

    @property
    def workflows(self):
        return self._workflows
    
    @workflows.setter
    def workflows(self, workflows):
        self._workflows = workflows
        self._current_workflow = workflows and workflows[0]
        
def start_new_session(user_id: str, session_id: str = "", workflows = []):
    session_id = session_id or str(uuid.uuid4())
    unblending = Unblending()
    
    session = Session(user_id, session_id, history = ChatMessageHistory())
    unblending_workflow = UnblendingWorkflow(unblending, session = session)
    session.workflows = [ UserIntroWorkflow(UserIntro(), session = session),
                          unblending_workflow,
                          PartWorkflow(Part(), session = session)
                          ]
    add_session_to_store(session)
    return session

def find_or_create_session(user_id: str, session_id: str = ""):
    if session := get_session(user_id, session_id):
        if not session.ended:
            return session
    return start_new_session(user_id, session_id)

