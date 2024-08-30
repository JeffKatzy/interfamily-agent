from langchain_core.pydantic_v1 import BaseModel, Field


class Part(BaseModel):
    part: str = Field("",
        description="A feeling, struggle, thought pattern, or part they encounter.")
    aware_of_part: str = Field("",
        description="Physical feeling of part or the sense of the part")
    feeling_to_part: str = Field("",
        description="Emotion or response towards the primary part")
    achieved_unblending: bool = Field("", description = """Achieved unblending if feels compassion or warmth towards the part.
    Did not achieve if feels negative towards the part.""")
    shared_feelings: bool = Field("", description = """Was the user able to share its compassion towards the part.""")
    
    