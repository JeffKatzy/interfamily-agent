from langchain_core.pydantic_v1 import BaseModel, Field


class ExplorePart(BaseModel):
    asked_if_wants_you_to_know: bool = Field("", description = """Did the user ask if the part has anything that it wants the user to know about how it's feeling.""")
    asked_if_wants_to_leave: bool = Field("", description = """Did the user ask if the part is open to getting out of there where it feels stuck.""")
    asked_part_to_show_how_bad_it_was: bool = Field("", description = """Did the user ask the part to really let the user get how bad it was for it.""")
    does_user_get_how_bad_it_was: bool = Field("", description = """Does the part feel that the user gets how bad it was for it.""")
    part_wants_to_leave: bool = Field("", description = """Does the part want to leave.""")
    
    