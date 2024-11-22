from __future__ import annotations

from typing import Any

from domain.models.explore_part import ExplorePart
from domain.prompt import next_message_prompt
from lib.base_workflow import BaseWorkflow, Step


class ExplorePartWorkflow(BaseWorkflow):
    _model: ExplorePart
    session: Any
    
    def __init__(self, **data):
        super().__init__(**data)
        self._model = ExplorePart()

    see_if_wants_you_to_know_part: Step = Step(prompt = """Ask the user if the part has anything that it wants the user to know about how it's feeling.
    For example, if it's anxious ask if there's something it wants the user to know about it's anxiety.
    Or are there any memories it would like to share with you.""",
        skip=lambda view: bool(view.see_if_wants_you_to_know_part.invoked > 0))
    
    ask_for_part_to_indicate_how_bad_it_was: Step = Step(prompt = """Then tell the user, to tell the part to really let the user get how bad it was for it.
                                                          Have it say or show whatever it needs to trust that the user gets it.
                                                          Let the user feel it and see it and sense it.""",
                                skip=lambda view: bool(view.ask_for_part_to_indicate_how_bad_it_was.invoked > 0))
    ask_if_part_thinks_user_gets_it: Step = Step(prompt = """Ask the part if it thinks the user gets how bad it was for it.  Or it can always show the user more.""",
                                skip=lambda view: bool(view._model.does_user_get_how_bad_it_was or view.ask_if_part_thinks_user_gets_it.invoked > 1))
    see_if_part_wants_to_leave: Step = Step(prompt = """If we learn more about the part's feelings, let it know the feelings make sense.
    And have the user ask the part is if it is open to getting out of there where it feels stuck.""",
                                skip=lambda view: bool(view.see_if_part_wants_to_leave.invoked > 1 and view._model.part_wants_to_leave))
    
    def prompt(self):
        return next_message_prompt