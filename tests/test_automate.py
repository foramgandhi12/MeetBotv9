import unittest
from unittest.mock import Mock, MagicMock
import os
from MeetBotv9 import BOT_TOKEN, USER_ID, help
from MeetBotv9 import telegram_bot_sendtext

bot_token = os.getenv('BOT_TOKEN')


class TestAutomate(unittest.TestCase):
    def test_sendText(self):
        self.assertEquals(telegram_bot_sendtext("test message"), 1)

    def test_token(self):
        self.assertEquals(BOT_TOKEN, '5294114162:AAF6XQy-TcAetSjXGfXhDqBqtZx8Ju7MVlA')

    def test_help(self):
        mocked_update = MagicMock()
        mocked_update.effective_chat.id = 0
        mocked_update.message.from_user.id = int(USER_ID)
        mocked_update.message.text = "/help"

        mocked_context = Mock()
        self.assertEquals(help(mocked_update, mocked_context), 1)
        mocked_context.bot.send_message.asset_called(chat_id=USER_ID, text="Test")

        mocked_update.message.from_user.id = 0
        self.assertEquals(help(mocked_update, mocked_context), 0)
