import asyncio
import json

import pytest

from domain.models.part import Part
from domain.session import Session
from domain.workflows.images.base_image import (BaseImage, add_to_queue,
                                                get_and_yield_message)
from domain.workflows.images.part_description_image import PartDescriptionImage


@pytest.mark.asyncio
async def test_base_image():
    clients = {}
    add_to_queue(session_id="456", clients=clients)
    session = Session(user_id="123", session_id="456")
    base_image = BaseImage(session=session, clients=clients)
    result = await base_image.run()
    assert result is not None


@pytest.mark.asyncio
async def test_get_and_yield_message():
    clients = {}
    add_to_queue(session_id="456", clients=clients)
    session = Session(user_id="123", session_id="456")
    base_image = BaseImage(session=session, clients=clients)
    message_generator_task = asyncio.create_task(get_and_yield_message(session_id="456", clients=clients).__anext__())
    result = await base_image.run(session, clients)
    message = await message_generator_task
    
    data = json.loads(message.split("data: ")[1])
    assert data["image"] is not None
    assert data["description"] is not None

@pytest.mark.asyncio
async def test_part_description_image():
    clients = {}
    add_to_queue(session_id="456", clients=clients)
    session = Session(user_id="123", session_id="456")
    part = Part(description_of_part="A happy cartoon dog with big eyes, sitting in a grassy field, with flat colors and no background details, minimalistic style.")
    part_description_image = PartDescriptionImage(session=session, model=part)
    message_generator_task = asyncio.create_task(get_and_yield_message(session_id="456", clients=clients).__anext__())
    result = await part_description_image.run(session, clients)
    message = await message_generator_task
    
    data = json.loads(message.split("data: ")[1])
    assert data["image"] is not None
    assert data["description"] is not None
