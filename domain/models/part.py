from langchain_core.pydantic_v1 import BaseModel, Field


class Part(BaseModel):
    description_of_part: str = Field("",
        description="How does the user describe the part?")
    emotion_of_part: str = Field("", description = """What emotion does the user describe the part as feeling. Eg. angry, sad, depressed, scared.""")
    toned_down_emotion_of_part: str = Field("", description = """Take the emotion of the part and then tone it down. For example turn angry into frustrated, and sad into upset or feeling down.""")
    wants_to_care_for_part: bool = Field("", description = """Does the user desire to care for the part.""")
    shared_feelings: bool = Field("", description = """Did the user share compassion towards the part.""")
    shared_feelings_description: str = Field("", description = """How did the user share compassion towards the part.""")
