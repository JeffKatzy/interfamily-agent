from __future__ import annotations

from typing import Any

from domain.models.unburden_part import UnburdenPart
from domain.prompt import next_message_prompt
from lib.base_workflow import BaseWorkflow, Step


class UnburdenPartWorkflow(BaseWorkflow):
    _model: UnburdenPart
    session: Any

    def __init__(self, **data):
        super().__init__(**data)
        self._model = UnburdenPart()

    ask_if_ready_to_unload: Step = Step(prompt="Tell the user to ask the part if he is ready to unload the feelings and beliefs he got from back there.  If the user is unsure what this means, tell him we just need his desire to stop carrying negative feelings.",
        skip=lambda view: bool(view._model.user_asked_if_ready_to_unload))
    ask_where_carries_negative_feelings: Step = Step(prompt="Ask the user to ask the part where in the body the part carries negative feelings.",
        skip=lambda view: bool(view._model.where_carries_negative_feelings))
    ask_how_user_wants_to_unload_negative_feelings: Step = Step(prompt="Ask the user to ask the part what he would like to give these feelings up to: light, water, fire, wind, earth, or anything else.",
        skip=lambda view: bool(view._model.description_of_how_user_wants_to_unload_negative_feelings))
    tell_user_to_unload_negative_feelings: Step = Step(prompt="Tell the user to bring in that force described earlier (for example, light, water, fire, wind, earth, etc.) to the part in the body where the part carries negative feelings.  And that the force can take it the feelings away, and that there is no need to carry it anymore.",
        skip=lambda view: bool(view.tell_user_to_unload_negative_feelings.invoked > 0))
    ask_how_the_part_is_doing: Step = Step(prompt="Ask the user how the part is doing with unloading the negative feelings.  If the part is not doing ok, see if there is anything else the user can do for it.",
        skip=lambda view: bool(view.ask_how_the_part_is_doing.invoked > 0))
    invite_new_qualities: Step = Step(prompt="Tell the user to tell the part, that if the part wants to, the part can invite new qualities into the part's body that the part would like to have.",
        skip=lambda view: bool(view._model.description_of_new_qualities))
    ask_how_the_part_is_doing_with_new_qualities: Step = Step(prompt="Ask the user how the part seems now.",
        skip=lambda view: bool(view.ask_how_the_part_is_doing_with_new_qualities.invoked > 0))
    invite_other_parts_to_join: Step = Step(prompt="Tell the user, if the user wants to, the user can invite other parts to come in and see the unburdened part.",
        skip=lambda view: bool(view.invite_other_parts_to_join.invoked > 0))
    ask_if_complete: Step = Step(prompt="Ask the user if it feels complete now.",
        skip=lambda view: bool(view.ask_if_complete.invoked > 0))

    def prompt(self):
        return next_message_prompt
