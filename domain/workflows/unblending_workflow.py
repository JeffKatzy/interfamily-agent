from typing import Any

from domain.models.unblending import Unblending
from lib.base_workflow import BaseWorkflow, WField
from domain.prompt import next_message_prompt

class UnblendingWorkflow(BaseWorkflow):
    _model: Unblending
    session: Any

    find_part: WField = WField(prompt="Ask if there's a feeling, struggle, thought pattern, or part they need help with.",
        skip=lambda view: bool(view._model.part))
    assess_awareness: WField = WField(prompt = "Thank them, mirror using parts language.  Then ask if they're aware of this part and how they sense or are aware of the part in their body.",
                        skip=lambda view: bool(view._model.aware_of_part))
    ask_feeling_towards_part: WField = WField(prompt = "Ask how they feels towards the target part.  For example, are they ok with the part being there?",
                                skip=lambda view: bool(view._model.feeling_to_part))
    unblend_from_part: WField = WField(prompt = "If the user feels negative qualities towards the target part, ask if that part that feels negative to the target part can take a step back during the session so that we can get to know the target part better.", 
                                    skip=lambda view: bool(view._model.achieved_unblending or view._model.agreed_can_step_back or view.unblend_from_part.invoked > 1))

    def __init__(self, model, **data):
        super().__init__(**data)
        self._model = model

    def prompt(self):
        return next_message_prompt
