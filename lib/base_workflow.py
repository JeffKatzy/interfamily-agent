import asyncio
from typing import Callable, Optional

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel

from domain.prompt import system_message
from domain.store import clients


class Step(BaseModel):
    prompt: str
    skip: Optional[Callable] = None
    then: Optional[Callable] = None
    invoked: int = 0


class BaseWorkflow(BaseModel):

    def next_message_prompt():
        return ChatPromptTemplate.from_messages(
        [("system", system_message),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "suggested next question: {input}"),
        ])

    def render_fields(self):
        indexed_prompts = [(i, v['prompt']) for i, v in enumerate(self.model_dump().values())]
        return "\n".join([f"{i + 1}. {prompt}"
         for i, prompt in indexed_prompts])

    def steps(self):
        return {field:attrs for field, attrs in self.model_dump().items() if field != 'session'}

    async def get_next_step(self):
        """Iterate through fields.  If skip function not satisfied, then it's the next step."""
        for field, attrs in self.steps().items():
            if not attrs['skip'](self):
                step = getattr(self, field) # retrieve next step
                if attrs.get('then'):
                    image_obj = attrs['then'](self)
                    print('running image generation from next step')
                    asyncio.create_task(image_obj.run(self.session, clients))
                return step
                
    @property
    def model(self):
        return self._model

    def is_done(self):
        for field, attrs in self.model_dump().items():
            if attrs.get('skip') and not attrs['skip'](self):
                return False
        return True