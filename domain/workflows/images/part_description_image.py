from typing import Any

from domain.workflows.images.base_image import BaseImage


class PartDescriptionImage(BaseImage):
    session: Any
    model: Any

    async def run(self, session, clients):
        prompt = self.build_prompt()
        print('image prompt: ', prompt)
        await self.add_image_to_queue(session, clients, prompt)

    def build_prompt(self):
        emotion = self.model.emotion_of_part
        description = self.model.description_of_part
        if emotion:
            return description.replace(emotion, \
            f"very slightly {self.model.toned_down_emotion_of_part or self.model.emotion_of_part}")
        else:
            return f"A {self.model.description_of_part}."
        
