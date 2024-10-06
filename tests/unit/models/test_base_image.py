import asyncio
import json

import pytest

from domain.session import Session
from domain.workflows.images.base_image import (BaseImage, add_to_queue,
                                                get_and_yield_message)

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
