from __future__ import annotations

from typing import Any

from domain.models.transport_part import TransportPart
from domain.prompt import next_message_prompt
from lib.base_workflow import BaseWorkflow, Step


class TransportPartWorkflow(BaseWorkflow):
    _model: TransportPart
    session: Any

    def __init__(self, **data):
        super().__init__(**data)
        self._model = TransportPart()

    go_to_the_part: Step = Step(prompt = "Tell the user to ask the part if he is ready to leave that time and place with you, and either go to your place now, or to any fantasy place of the part's choice.",
                                skip=lambda view: bool(view.go_to_the_part.invoked > 0))
    find_out_desired_place: Step = Step(prompt = "Ask the user what place the part wants to go to.  Where does the part want to go?",
                                skip=lambda view: bool(view._model.desired_place))
    tell_user_to_go_to_desired_place: Step = Step(prompt = "Tell the user to take the part to that place.  Then, ask the user if the part is now in that place.",
                                skip=lambda view: bool(view._model.part_in_desired_place))
    see_how_the_part_reacts_to_user_going_to_desired_place: Step = Step(prompt = "Ask the user how the part likes being in that place.",
                                skip=lambda view: bool(view._model.part_likes_being_in_desired_place))
    tell_does_not_need_to_return: Step = Step(prompt = "Tell the user to tell the part that the part does not need to return to the scene where he was hurt.  And tell the part to tell the user that to tell the part that the user will be taking care of the part now.",
                                skip=lambda view: bool(view._model.user_told_part_that_part_does_not_need_to_return))  

    def prompt(self):
        return next_message_prompt