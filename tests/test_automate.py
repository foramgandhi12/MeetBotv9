import unittest
from unittest.mock import Mock
# from MeetBotv9 import start
# from automate import start

from chromium_Scripts import *
from automate import *
from gscripts.login import *
from gscripts.meet import *


class TestAutomate(unittest.TestCase):
    def test_sendText(self):
        self.assertEqual(telegram_bot_sendtext("test message"), 1)
        # assert BOT_TOKEN == ""

    def test_token(self):
        self.assertEqual(BOT_TOKEN, '')

    def test_user_id(self):
        self.assertEqual(USER_ID, '')

    def test_gmail_username(self):
        self.assertEqual(GMAIL_USERNAME, 'meet.botv9@gmail.com')
