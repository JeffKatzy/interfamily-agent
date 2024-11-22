from __future__ import annotations

from typing import Any

from domain.models.user_intro import UserIntro
from domain.prompt import next_message_prompt
from lib.base_workflow import BaseWorkflow, Step


class UserIntroWorkflow(BaseWorkflow):
    _model: UserIntro
    session: Any

    def __init__(self, **data):
        super().__init__(**data)
        self._model = UserIntro()

    say_hi: Step = Step(prompt="Introduce yourself and your role as an IFS coach. Ask if they have questions about IFS or want to start a session.",
        skip=lambda view: bool(view.say_hi.invoked))
    ask_if_want_session: Step = Step(prompt = "Ask if they would like to start a session.",
                        skip=lambda view: bool(view._model.initial_session_request))

    
    def prompt(self):
        return next_message_prompt
    
    def is_done(self):
        return self._model.initial_session_request