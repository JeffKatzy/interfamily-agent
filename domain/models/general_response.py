from langchain_core.pydantic_v1 import BaseModel, Field


class GeneralResponse(BaseModel):
    """Use this when the other parser is not applicable.  This is for storing general information about the user responses."""
    text: str = Field("",
        description="This is the user input",
    )