from __future__ import annotations

from typing import Any

from domain.models.part import Part
from domain.prompt import next_message_prompt
from domain.workflows.images.base_image import BaseImage
from lib.base_workflow import BaseWorkflow, WField


class PartWorkflow(BaseWorkflow):
    _model: Part
    session: Any

    find_part: WField = WField(prompt="Ask if there's a feeling, struggle, thought pattern, or part they need help with.",
        skip=lambda view: bool(view._model.part), then = lambda view: BaseImage(view.session))
    assess_awareness: WField = WField(prompt = "Thank them, mirror using parts language.  Then ask if they're aware of this part and how they sense or are aware of the part in their body.",
                        skip=lambda view: bool(view._model.aware_of_part))
    ask_feeling_towards_part: WField = WField(prompt = "Ask how they feels towards the target part.  For example, are they ok with the part being there?",
                                skip=lambda view: bool(view._model.feeling_to_part))
    unblend_from_part: WField = WField(prompt = "If the user feels negative qualities towards the target part, ask if that part that feels negative to the target part can take a step back during the session so that we can get to know the target part better.", 
                                    skip=lambda view: bool(view._model.achieved_unblending or view._model.agreed_can_step_back))
    see_if_more_compassionate: WField = WField(prompt = "Ask how the user feels now that they've unblended from the part.",
                                skip=lambda view: bool(view._model.has_compassion_towards_part))
    ask_for_description_of_part: WField = WField(prompt = "Ask the user to describe the part to you.  Does it seem like a boy or a girl, and what is it feeling?",
                                skip=lambda view: bool(view._model.description_of_part))
    ask_to_share_feelings: WField = WField(prompt = "If the user confirms the feelings are from Self, ask them to share their feelings with the part",
                                skip=lambda view: bool(view._model.shared_feelings))
    ask_how_receieved: WField = WField(prompt = "Ask how the part received the shared feelings.", skip = lambda view: bool(view.ask_how_receieved.invoked > 0))
    
    def __init__(self, model, **data):
        super().__init__(**data)
        self._model = model
    
    def prompt(self):
        return next_message_prompt