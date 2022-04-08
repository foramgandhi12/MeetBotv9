import unittest
from unittest.mock import Mock, MagicMock
import os
from automate import BOT_TOKEN, USER_ID, start, help, owner, restart, status, reset
from chromium_Scripts import telegram_bot_sendtext

bot_token = os.getenv('BOT_TOKEN')
user_id = os.getenv('USER_ID')

mocked_update = MagicMock()
mocked_update.effective_chat.id = 0
mocked_context = Mock()


class TestAutomate(unittest.TestCase):
    def test_sendText(self):
        self.assertEqual(telegram_bot_sendtext("test message"), 1)

    def test_setup(self):
        self.assertEqual(bot_token, BOT_TOKEN)
        self.assertEqual(user_id, USER_ID)

    def test_start(self):
        # initially test with a valid user id
        mocked_update.message.from_user.id = int(user_id)
        mocked_update.message.from_user.first_name = 'test start'
        mocked_update.message.text = "/start"

        self.assertEqual(start(mocked_update, mocked_context), 1)

    def test_help(self):
        mocked_update.message.from_user.id = int(user_id)
        mocked_update.message.text = "/help"

        self.assertEqual(help(mocked_update, mocked_context), 1)

        mocked_update.message.from_user.id = 0
        self.assertEqual(help(mocked_update, mocked_context), 0)

    def test_owner(self):
        mocked_update.message.from_user.id = int(user_id)
        mocked_update.message.text = "/owner"

        self.assertEqual(owner(mocked_update, mocked_context), 1)

    def test_restart(self):
        mocked_update.message.from_user.id = int(user_id)
        mocked_update.message.text = "/restart"

        self.assertEqual(restart(mocked_update, mocked_context), 1)

        mocked_update.message.from_user.id = 0
        self.assertEqual(restart(mocked_update, mocked_context), 0)

    def test_status(self):
        mocked_update.message.from_user.id = int(user_id)
        mocked_update.message.text = "/status"

        self.assertEqual(status(mocked_update, mocked_context), 1)

        mocked_update.message.from_user.id = 0
        self.assertEqual(status(mocked_update, mocked_context), 0)

    def test_reset(self):
        mocked_update.message.from_user.id = int(user_id)
        mocked_update.message.text = "/reset"

        self.assertEqual(reset(mocked_update, mocked_context), 1)
        # after the execution if reset the ChromiumData folder should be loaded into the directory agagin and the
        # gmeet.pkl file should be deleted
        self.assertEqual(os.path.exists("ChromiumData"), True)
        self.assertEqual(os.path.exists('../gmeet.pkl'), False)

        mocked_update.message.from_user.id = 0
        self.assertEqual(status(mocked_update, mocked_context), 0)
