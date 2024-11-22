from langchain_core.pydantic_v1 import BaseModel, Field


class UnburdenPart(BaseModel):
    user_asked_if_ready_to_unload: bool = Field(False, description = """Did the user ask the part if he is ready to unload the feelings and beliefs he got from back there.""")
    description_of_how_user_wants_to_unload_negative_feelings: str = Field("", description = """The description of how the user wants to unload the negative feelings.  For example, this may be 'light', 'water', 'fire', 'wind', 'earth', or anything else.""")
    where_carries_negative_feelings: str = Field("", description = """The description of where in the body the part carries negative feelings.  For example, this may be 'heart', 'head', 'belly', 'back', 'chest', 'jaw' etc.""")
    description_of_new_qualities: str = Field("", description = """The description of the new qualities the part wants to invite into the part's body.""")
    part_is_doing_ok: bool = Field(False, description = """Did the part tell the user that he is doing ok now that the part has unloaded the negative feelings.""")
