import asyncio
import json
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel


load_dotenv()
client = OpenAI()

class BaseImage(BaseModel):
    session: Any

    async def run(self, session, clients):
        img_base64 = self.build_image()
        description = "This is a generated image."
        data = json.dumps({"image": img_base64, "description": description})
        await clients[session.session_id].put(data)
        return data

    def build_image(self, prompt = ""):
        prompt = "A happy cartoon dog with big eyes, sitting in a grassy field, with flat colors and no background details, minimalistic style."
        response = client.images.generate(
        model="dall-e-3",
        response_format="b64_json",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1)

        img_base64 = response.data[0].b64_json
        return img_base64

def add_to_queue(session_id, clients):
    if session_id not in clients:
        clients[session_id] = asyncio.Queue()

async def get_and_yield_message(session_id, clients):
    message = await clients[session_id].get()
    print(message)
    yield f"data: {message}\n\n"
