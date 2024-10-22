
import telebot
from bibabot.IBot import IBot

class TelegramBot(IBot):

    def __init__(self, bot_token, bot_channel):
        self.bot = telebot.TeleBot(bot_token)
        self.bot_channel = bot_channel

    def send_message(self, message):
        self.bot.send_message(self.bot_channel, message, parse_mode='MarkdownV2')
        