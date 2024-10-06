
from bibabot.IBot import IBot
import logging

class LogBot(IBot):
    def send_message(self, message):
        logging.info(message)
        