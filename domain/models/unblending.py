from langchain_core.pydantic_v1 import BaseModel, Field


class Unblending(BaseModel):
    part: str = Field("",
        description="A feeling, struggle, thought pattern, or part they encounter.")
    aware_of_part: str = Field("",
        description="Physical feeling of part or the sense of the part.  For example, a pain the neck or tightness in the jaw.")
    agreed_can_step_back: bool = Field(False, description = """Did the user agree to take a step back from the part.""")
    feeling_to_part: str = Field("",
        description="Emotion or response towards the primary part")
    achieved_unblending: bool = Field(False, description = """This is related to the feeling to part unblending
    Achieved unblending if feels compassion, warmth or acceptance towards the part.""")