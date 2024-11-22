import uuid

from langchain_community.chat_message_histories import ChatMessageHistory

from domain.store import add_session_to_store, get_session
from domain.workflows import (ExplorePartWorkflow, PartWorkflow,
                              TransportPartWorkflow, UnblendingWorkflow,
                              UnburdenPartWorkflow, UserIntroWorkflow)


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
        
def build_session(user_id: str, session_id: str = ""):
    session_id = session_id or str(uuid.uuid4())
    session = Session(user_id, session_id, history = ChatMessageHistory())
    return session

def add_workflows_to_session(session, workflows):
    session.workflows = [Workflow(session = session) for Workflow in workflows]
    return session

def setup_session(user_id: str, session_id: str = "", workflows = []):
    if not workflows:
        workflows = [ UserIntroWorkflow,UnblendingWorkflow,PartWorkflow,
                    ExplorePartWorkflow, TransportPartWorkflow, 
                    UnburdenPartWorkflow]
    session = build_session(user_id, session_id)
    session = add_workflows_to_session(session, workflows)
    session = add_session_to_store(session)
    return session

def find_or_create_session(user_id: str, session_id: str = ""):
    if session := get_session(user_id, session_id):
        if not session.ended:
            return session
    else:
        session = setup_session(user_id, session_id)
        return session
