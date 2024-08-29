from typing import Callable, Optional

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel

from domain.prompt import system_message


class WField(BaseModel):
    prompt: str
    skip: Optional[Callable] = None
    was_asked: int = 0

class BaseWorkflow(BaseModel):
    def next_message_prompt():
        return ChatPromptTemplate.from_messages(
        [("system", system_message),
        MessagesPlaceholder(variable_name="history"),
        ("human", "suggested next question: {input}"),
        ])

    def render_fields(self, preamble = ""):
        indexed_prompts = [(i, v['prompt']) for i, v in enumerate(self.dict().values())]
        return "\n".join([f"{i + 1}. {prompt}"
         for i, prompt in indexed_prompts])

    def get_next_message(self):
        for field, attrs in self.dict().items():
            if attrs.get('skip') and not attrs['skip'](self):
                return attrs['prompt']
                
    @property
    def model(self):
        return self._model