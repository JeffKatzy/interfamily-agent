from domain.models.user_outro import UserOutro
from domain.prompt import next_message_prompt
from lib.workflow_utils import BaseWorkflow, WField


class UserOutroWorkflow(BaseWorkflow):
    _model: UserOutro
    thank_user: WField = WField(prompt="Thank the user and tell them it's the end of the session and they can request a new one.")

    def __init__(self, model, **data):
        super().__init__(**data)
        self._model = model
    
    def prompt(self):
        return next_message_prompt
    
    def is_done(self):
        return False # last workflow, user ends by ending session