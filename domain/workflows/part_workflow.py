from domain.models.part import Part
from domain.prompt import next_message_prompt
from lib.workflow_utils import BaseWorkflow, WField


class PartWorkflow(BaseWorkflow):
    _model: Part

    find_part: WField = WField(prompt="Ask if there's a feeling, struggle, thought pattern, or part they need help with.",
        skip=lambda view: bool(view._model.part))
    assess_awareness: WField = WField(prompt = "Thank them, mirror using parts language.  Then ask if they're aware of this part and how they sense or are aware of the part.",
                        skip=lambda view: bool(view._model.aware_of_part))
    ask_feeling_towards_part: WField = WField(prompt = "Ask how they feel toward the target part.",
                                skip=lambda view: bool(view._model.feeling_to_part))
    unblend_from_part: WField = WField(prompt = "If the user feels negative qualities towards the part, help them unblend.", 
                                    skip=lambda view: bool(view._model.achieved_unblending))
    ask_to_share_feelings: WField = WField(prompt = "If the user confirms the feelings are from Self and they feel positively toward the part, ask them to share their feelings with the part",
                                skip=lambda view: bool(view._model.shared_feelings))
    ask_how_receieved: WField = WField(prompt = "Ask how the part received the shared feelings.")

    def __init__(self, model, **data):
        super().__init__(**data)
        self._model = model
    
    def prompt(self):
        return next_message_prompt