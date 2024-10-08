from __future__ import annotations

from typing import Any

from domain.models.part import Part
from domain.prompt import next_message_prompt
from domain.workflows.images.part_description_image import PartDescriptionImage
from lib.base_workflow import BaseWorkflow, WField


class PartWorkflow(BaseWorkflow):
    _model: Part
    session: Any
    
    ask_for_description_of_part: WField = WField(prompt = "Ask the user to describe the part now that they've unblended from it.  Can you see the part - what does it look like, and what is it feeling?",
                                skip=lambda view: bool(view._model.description_of_part))
    ask_for_compassion_to_part: WField = WField(prompt = f"Ask the user if would if it feels compassion towards this part.",
                                then = lambda view: PartDescriptionImage(session=view.session, model=view._model),
                                skip=lambda view: bool(view._model.wants_to_care_for_part))
    ask_to_share_feelings: WField = WField(prompt = f"Ask the user to share it's compassion, in however way it thinks is best.  For example, the user can give the part a hug, or some kind words.",
                                    skip=lambda view: bool(view._model.shared_feelings)) 
    ask_how_receieved: WField = WField(prompt = "Ask how the part received the shared feelings.", skip = lambda view: bool(view.ask_how_receieved.invoked > 0))
    
    def __init__(self, model, **data):
        super().__init__(**data)
        self._model = model
    
    def prompt(self):
        return next_message_prompt