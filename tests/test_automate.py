import unittest
from telegram import Message
from telegram import Update
from telegram import User
from telegram.ext import CallbackContext
from telegram.ext import Updater
from datetime import datetime
from telegram import Chat, Bot

from MeetBotv9 import BOT_TOKEN, USER_ID, help
from MeetBotv9 import telegram_bot_sendtext

update_id_sample = 123456789
user_sample = User(id=update_id_sample, first_name='test first name', is_bot=True)

message_sample = Message(message_id=1234, date=datetime.now(), chat=Chat(id=int(USER_ID), type='test'), from_user=user_sample)
update_sample = Update(
    update_id=update_id_sample,
    message=message_sample
)
updater_sample = Updater(use_context=True, bot=Bot(token=BOT_TOKEN))
context_sample = CallbackContext(updater_sample.dispatcher)


class TestAutomate(unittest.TestCase):
    def test_sendText(self):
        self.assertEquals(telegram_bot_sendtext("test message"), 1)

    def test_token(self):
        self.assertEquals(BOT_TOKEN, '5294114162:AAF6XQy-TcAetSjXGfXhDqBqtZx8Ju7MVlA')

    def test_help(self):
        help(update=update_sample, context=context_sample)
