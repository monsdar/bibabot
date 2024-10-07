
import unittest

from bibabot.BotHandler import BotHandler
from bibabot.LogBot import LogBot

class TestBotHandler(unittest.TestCase):
      
  def test_handle_command(self):
    bot = LogBot()
    bot_handler = BotHandler(bot)
    bot_handler.handle_command("/biba")
        
  def test_handle_invalid_command(self):
    bot = LogBot()
    bot_handler = BotHandler(bot)
    bot_handler.handle_command("invalid command")
      