from langchain_core.pydantic_v1 import BaseModel, Field


class ComfortPart(BaseModel):
    user_is_with_part_in_that_time: bool = Field(False, description = """Is the user with the part in that time.""")
    user_is_comforting_part: bool = Field(False, description = """Does the user describe being with the part in a comforting or sympathetic way.""")
    gets_part_reaction: bool = Field(False, description = """Does the part feel comforted by the user.""")
    part_indicated_something_it_wants_user_to_do: bool = Field(False, description = """Does the part indicate something it wants the user to do for it.""")
    description_of_what_part_wants: str = Field("", description = """What the part wants the user to do for it.""")
    user_acted_for_part: bool = Field(False, description = """Did the user do what the part wants.""")
    user_says_how_the_part_reacted_to_user_acting_for_it: str = Field("", description = """How the part reacted to the user acting for it.""")
