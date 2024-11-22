import asyncio
import json
import os
import time
from typing import Any

import aiohttp
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()


key = os.getenv('IMAGE_API_KEY')
client = OpenAI(api_key=key)

class BaseImage(BaseModel):
    session: Any

    async def add_image_to_queue(self, session, clients, prompt):
        img_base64 = await self.build_image(prompt)
        data = json.dumps({"image": img_base64, "description": prompt})
        await clients[session.session_id].put(data)
        return data

    async def build_image(self, prompt):
        if not prompt:
            raise ValueError('prompt is required')
        print('building image: ', prompt)
        start_time = time.time()
        prompt = f"""For the following description, create a flat cartoon style image with a light blue background.
        But keep all emotions very subtle.
        Do not put any text in the image.  Description: {prompt}.
        Keep all emotions subtle and slight."""
        url = "https://api.openai.com/v1/images/generations"
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "dall-e-3",
            "prompt": prompt,
            "size": "1024x1024",
            "response_format": "b64_json",
            "n": 1
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                response_data = await response.json()
                img_base64 = response_data['data'][0]['b64_json']
        end_time = time.time()  # End timing
        duration = end_time - start_time
        return img_base64

def add_to_queue(session_id, clients):
    if session_id not in clients:
        clients[session_id] = asyncio.Queue()

async def get_and_yield_message(session_id, clients):
    message = await clients[session_id].get()
    yield f"data: {message}\n\n"
