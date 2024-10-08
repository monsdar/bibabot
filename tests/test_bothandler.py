
import unittest

from bibabot.BotHandler import BotHandler
from bibabot.LogBot import LogBot
from bibabot.BibaCommand import BibaCommand

class TestBotHandler(unittest.TestCase):
      
  def test_handle_command(self):
    bot = LogBot()
    commands = [
        BibaCommand(),
    ]
    bot_handler = BotHandler(bot, commands)
    bot_handler.handle_command("/biba")
        
  def test_handle_invalid_command(self):
    bot = LogBot()
    commands = [
        BibaCommand(),
    ]
    bot_handler = BotHandler(bot, commands)
    bot_handler.handle_command("invalid command")
      