import unittest
from unittest.mock import Mock, MagicMock
import os
from gscripts.login import login
from automate import reset

bot_token = os.getenv('BOT_TOKEN')
user_id = os.getenv('USER_ID')

mocked_update = MagicMock()
mocked_update.effective_chat.id = 0
mocked_context = Mock()


class TestLogin(unittest.TestCase):
    # test /login command
    def test_login(self):
        # initially test with a valid user id
        mocked_update.message.from_user.id = int(user_id)
        mocked_update.message.from_user.first_name = 'test login'
        mocked_update.message.text = "/login"

        self.assertEqual(os.path.exists('../gmeet.pkl'), False)
        self.assertEqual(login(mocked_update, mocked_context), 1)

        # after the execution of the last test the gmeet.pkl file should be created (already logged in)
        self.assertEqual(os.path.exists('../gmeet.pkl'), True)
        self.assertEqual(login(mocked_update, mocked_context), 0)
        reset(mocked_update, mocked_context)  # run reset to delete the gmeet.pkl

        # test invalid user id
        mocked_update.message.from_user.id = 0
        self.assertEqual(login(mocked_update, mocked_context), -1)
