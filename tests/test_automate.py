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
    # test if the telegram_bot_sendtext is sending a message to the telegram app
    def test_sendText(self):
        self.assertEqual(telegram_bot_sendtext("test message"), 1)

    # test if the Bot token and user id is being initialized from the .env properly
    def test_setup(self):
        self.assertEqual(bot_token, BOT_TOKEN)
        self.assertEqual(user_id, USER_ID)

    # test the /start command
    def test_start(self):
        mocked_update.message.from_user.id = int(user_id)
        mocked_update.message.from_user.first_name = 'test start'
        mocked_update.message.text = "/start"

        # validate the program is sending a message to the Telegram app
        self.assertEqual(start(mocked_update, mocked_context), 1)

    # test the /help command
    def test_help(self):
        # initially test with a valid user id
        mocked_update.message.from_user.id = int(user_id)
        mocked_update.message.text = "/help"

        # validate the bot is sending a message consisting of all the commands to user
        self.assertEqual(help(mocked_update, mocked_context), 1)

        # test invalid user id
        mocked_update.message.from_user.id = 0
        self.assertEqual(help(mocked_update, mocked_context), 0)

    # test /owner command
    def test_owner(self):
        mocked_update.message.from_user.id = int(user_id)
        mocked_update.message.text = "/owner"

        # validate the bot is sending a message containing the author information to user
        self.assertEqual(owner(mocked_update, mocked_context), 1)

    # test /restart command
    def test_restart(self):
        # initially test with a valid user id
        mocked_update.message.from_user.id = int(user_id)
        mocked_update.message.text = "/restart"

        # validate that the browser is being restarted
        self.assertEqual(restart(mocked_update, mocked_context), 1)

        # test invalid user id
        mocked_update.message.from_user.id = 0
        self.assertEqual(restart(mocked_update, mocked_context), 0)

    # test /status command
    def test_status(self):
        # initially test with a valid user id
        mocked_update.message.from_user.id = int(user_id)
        mocked_update.message.text = "/status"

        # validate the bot is sending the current status of the browser
        self.assertEqual(status(mocked_update, mocked_context), 1)

        # test invalid user id
        mocked_update.message.from_user.id = 0
        self.assertEqual(status(mocked_update, mocked_context), 0)

    # test /reset command
    def test_reset(self):
        # initially test with a valid user id
        mocked_update.message.from_user.id = int(user_id)
        mocked_update.message.text = "/reset"

        # validate the browser is being reset
        self.assertEqual(reset(mocked_update, mocked_context), 1)
        # after the execution if reset the ChromiumData folder should be loaded into the directory again and the
        # gmeet.pkl file should be deleted
        self.assertEqual(os.path.exists("ChromiumData"), True)
        self.assertEqual(os.path.exists('../gmeet.pkl'), False)

        # test invalid user id
        mocked_update.message.from_user.id = 0
        self.assertEqual(status(mocked_update, mocked_context), 0)
