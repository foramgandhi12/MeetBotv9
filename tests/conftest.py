import asyncio

import pytest
import os
from telethon import TelegramClient
from telethon.sessions import StringSession

dot_token = '5294114162:AAF6XQy-TcAetSjXGfXhDqBqtZx8Ju7MVlA'
api_id = 15480165
api_hash = '50304c016cc344632828669526122bb8'


@pytest.fixture(scope='session')
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def client():
    return TelegramClient(
        'bot', api_id, api_hash,
        sequential_updates=True
    )


@pytest.fixture(scope="session")
async def client() -> TelegramClient:
    client = TelegramClient(
        'bot', api_id, api_hash,
        sequential_updates=True
    )
    await client.connect()
    await client.get_me()
    await client.get_dialogs()

    yield client

    await client.disconnect()
    await client.disconnected
