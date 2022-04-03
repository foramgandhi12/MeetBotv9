import unittest
# from MeetBotv9 import start
from MeetBotv9 import telegram_bot_sendtext
# from automate import start

class TestAutomate(unittest.TestCase):
    def test_sendText(self):
        # pass
        self.assertEquals(telegram_bot_sendtext("test message"), 1)
        # assert BOT_TOKEN == "5294114162:AAF6XQy-TcAetSjXGfXhDqBqtZx8Ju7MVlA"
