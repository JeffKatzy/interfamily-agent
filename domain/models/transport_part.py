from langchain_core.pydantic_v1 import BaseModel, Field


class TransportPart(BaseModel):
    user_asked_part_if_ready_to_leave_time_and_place_with_user: bool = Field(False, description = """Did the user ask the part if he is ready to leave that time and place with the user.""")
    desired_place: str = Field("", description = """The place the part wants to go to.""")
    part_in_desired_place: bool = Field(False, description = """Is the part in the desired place.""")
    part_likes_being_in_desired_place: bool = Field(False, description = """Does the part like being in the desired place.""")
    user_told_part_that_part_does_not_need_to_return: bool = Field(False, description = """Did the user tell the part that the part does not need to return to the scene where he was hurt.""")