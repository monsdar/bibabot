
from bibabot.IBot import IBot

class BotHandler():
    def __init__(self, bot_impl: IBot):
        self.bot = bot_impl

    def handle_biba(self):
        self.bot.send_message('Hello this is Bibabot!')
    