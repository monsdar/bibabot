
import unittest

from bibabot.BotHandler import BotHandler
from bibabot.LogBot import LogBot

class TestBotHandler(unittest.TestCase):
  def test_handle_biba(self):
    bot = LogBot()
    bot_handler = BotHandler(bot)
    bot_handler.handle_biba()
        