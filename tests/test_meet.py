import unittest
from unittest.mock import Mock, MagicMock
import os
from gscripts.meet import meet, meet_url, close
from gscripts.login import login
from automate import reset

bot_token = os.getenv('BOT_TOKEN')
user_id = os.getenv('USER_ID')

mocked_update = MagicMock()
mocked_update.effective_chat.id = 0
mocked_context = Mock()


class TestMeet(unittest.TestCase):
    def test_meet(self):
        # initially test with a valid user id
        mocked_update.message.from_user.id = int(user_id)
        mocked_update.message.from_user.first_name = 'test meet'

        # test invalid meet link
        mocked_update.message.text = "/meet sdf"
        self.assertEqual(meet(mocked_update, mocked_context), 0)

        # test valid meet link
        login(mocked_update, mocked_context)
        mocked_update.message.text = "/meet https://meet.google.com/gfr-iksc-qdv"
        self.assertEqual(meet(mocked_update, mocked_context), 1)
        reset(mocked_update, mocked_context)

        # test invalid user id
        mocked_update.message.from_user.id = 0
        self.assertEqual(meet(mocked_update, mocked_context), -1)

    def test_meet_url(self):
        # initially test with a valid user id
        mocked_update.message.from_user.id = int(user_id)
        mocked_update.message.from_user.first_name = 'test meet'
        mocked_update.message.text = "/meet"

        self.assertEqual(os.path.exists('../gmeet.pkl'), False)
        self.assertEqual(meet_url(mocked_context, 'https://meet.google.com/gfr-iksc-qdv'), 0)
        login(mocked_update, mocked_context)  # log into gmail

        self.assertEqual(os.path.exists('../gmeet.pkl'), True)
        self.assertEqual(meet_url(mocked_context, 'https://meet.google.com/gfr-iksc-qdv'), 1)
        reset(mocked_update, mocked_context)

    def test_close(self):
        # initially test with a valid user id
        mocked_update.message.from_user.id = int(user_id)
        mocked_update.message.from_user.first_name = 'test close'
        mocked_update.message.text = "/close"
        login(mocked_update, mocked_context)

        # run /close when not in a meeting
        self.assertEqual(close(mocked_update, mocked_context), 0)

        # run /close when in a meeting
        mocked_update.message.text = "/meet https://meet.google.com/gfr-iksc-qdv"
        meet(mocked_update, mocked_context)
        self.assertEqual(close(mocked_update, mocked_context), 1)

        # test invalid user id
        mocked_update.message.from_user.id = 0
        self.assertEqual(close(mocked_update, mocked_context), -1)
        reset(mocked_update, mocked_context)





