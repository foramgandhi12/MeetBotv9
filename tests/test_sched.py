import unittest
from unittest.mock import Mock, MagicMock
import os
import gscripts.sched
import datetime
from automate import today
from gscripts.login import login

bot_token = os.getenv('BOT_TOKEN')
user_id = os.getenv('USER_ID')

mocked_update = MagicMock()
mocked_update.effective_chat.id = 0
mocked_context = Mock()


class TestSched(unittest.TestCase):
    def test_addws(self):
        # initially test with a valid user id
        mocked_update.message.from_user.id = int(user_id)
        mocked_update.message.from_user.first_name = 'test addws'

        # test invalid meet link
        mocked_update.message.text = "/addws monday"  # incomplete command (need to include meet link)
        self.assertEqual(gscripts.sched.sched(mocked_update, mocked_context), 0)

        mocked_update.message.text = "/addws monday 1902 test"  # invalid meet link
        self.assertEqual(gscripts.sched.sched(mocked_update, mocked_context), 2)

        mocked_update.message.text = "/addws monday 2400 https://meet.google.com/gfr-iksc-qdv"  # invalid time
        self.assertEqual(gscripts.sched.sched(mocked_update, mocked_context), 3)

        mocked_update.message.text = "/addws monday 1200 https://meet.google.com/gfr-iksc-qdv"  # valid command
        self.assertEqual(gscripts.sched.sched(mocked_update, mocked_context), 1)

        # test invalid user id
        mocked_update.message.from_user.id = 0
        self.assertEqual(gscripts.sched.sched(mocked_update, mocked_context), -1)

    def test_ssch(self):
        # initially test with a valid user id
        mocked_update.message.from_user.id = int(user_id)
        mocked_update.message.from_user.first_name = 'test ssch'

        # check if the time check function returns true depending command passed
        mocked_update.message.text = "/addws {} {} https://meet.google.com/gfr-iksc-qdv".format(datetime.datetime.now().strftime("%A").lower() ,datetime.datetime.now().strftime("%H%M"))
        gscripts.sched.sched(mocked_update, mocked_context)
        self.assertEqual(gscripts.sched.checkTime(mocked_context), 1)


