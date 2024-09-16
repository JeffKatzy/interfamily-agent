from domain.models.user_intro import UserIntro
from domain.prompt import next_message_prompt
from lib.workflow_utils import BaseWorkflow, WField


class UserIntroWorkflow(BaseWorkflow):
    _model: UserIntro

    say_hi: WField = WField(prompt="Introduce yourself and your role as an IFS coach. Ask if they have questions about IFS or want to start a session.",
        skip=lambda view: bool(view.say_hi.invoked > 0))
    ask_if_want_session: WField = WField(prompt = "Ask if they would like to start a session.",
                        skip=lambda view: bool(view.invoked > 1))

    def __init__(self, model, **data):
        super().__init__(**data)
        self._model = model
    
    def prompt(self):
        return next_message_prompt