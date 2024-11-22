from __future__ import annotations

from typing import Any

from domain.models.comfort_part import ComfortPart
from domain.prompt import next_message_prompt
from lib.base_workflow import BaseWorkflow, Step


class ComfortPartWorkflow(BaseWorkflow):
    _model: ComfortPart
    session: Any

    def __init__(self, **data):
        super().__init__(**data)
        self._model = ComfortPart()
    
    go_to_the_part: Step = Step(prompt = "Tell the user to go to that part in that time, and be the part in the way that the part needed somebody.  And then tell me when you're with the part at that time.",
                                skip=lambda view: bool(view._model.user_is_with_part_in_that_time))
    see_if_comforting_the_part: Step = Step(prompt = "Ask the user how the user is being or acting towards the part.",
                                skip=lambda view: bool(view._model.user_is_comforting_part))
    comfort_part: Step = Step(prompt = "Tell the user to comfort the part until the part trusts that the part is not alone with it.  Then tell the user to see how the part is reacting.",
                                skip=lambda view: bool(view._model.gets_part_reaction))
    act_for_part: Step = Step(prompt = "Ask the part if there's anything it wants the user to do for the part.",
                                skip=lambda view: bool(view._model.part_indicated_something_it_wants_user_to_do))
    find_out_what_part_wants_user_to_do: Step = Step(prompt = "Ask the user what the part wants the user to do.",
                                skip=lambda view: bool(view._model.description_of_what_part_wants))
    tell_user_to_do_that_for_part: Step = Step(prompt = "Tell the user to do that for the part.",
                                skip=lambda view: bool(view._model.user_acted_for_part))
    see_how_the_part_reacts_to_user_acting_for_it: Step = Step(prompt = "Ask the user how the part is reacting to the user acting for it.",
                                skip=lambda view: bool(view._model.user_says_how_the_part_reacted_to_user_acting_for_it))
    
