from langchain_core.pydantic_v1 import BaseModel, Field


class UserIntro(BaseModel):
    """Use this when the user is saying hi, or asking to start a session."""
    user_greeting: str = Field("",
        description="This is the user input, for example 'hi', 'hello', 'how are you?'",
    )
    initial_session_request: bool = Field(False,
        description="Use this when the user is asking to start a session.",
    )
    end_session_request: bool = Field(False,
        description="Use this when the user is asking to end a session.",
    )