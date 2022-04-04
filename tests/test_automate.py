import unittest
import pytest
from pytest import mark
import os
from MeetBotv9 import BOT_TOKEN
from MeetBotv9 import telegram_bot_sendtext
from telethon.tl.custom.message import Message
from telethon import TelegramClient
from telethon.sessions import StringSession

bot_token = os.getenv('BOT_TOKEN')
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')


# client = TelegramClient(None, api_id, api_hash).start(bot_token=bot_token)


# @pytest.fixture(scope='session')
# async def client() -> TelegramClient:
#     client = TelegramClient(None, int(api_id), api_hash, sequential_updates=True)
#
#     await client.connect()
#     await client.get_me()
#     await client.get_dialogs()
#
#     yield client
#
#     await client.disconnect()
#     await client.disconnected


class TestAutomate(unittest.TestCase):
    def test_sendText(self):
        self.assertEquals(telegram_bot_sendtext("test message"), 1)

    def test_token(self):
        self.assertEquals(BOT_TOKEN, '5294114162:AAF6XQy-TcAetSjXGfXhDqBqtZx8Ju7MVlA')

    def test_start(self):
        pass


@mark.asyncio
async def test_help(client: TelegramClient):
    with client.conversation("@myReplicaLikeBot", timeout=5) as bot:
        bot.loop.run_until_complete(client.send_message('/help'))


if __name__ == '__main__':
    # main()
    pass
