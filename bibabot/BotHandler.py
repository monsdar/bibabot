
import logging
import time
from typing import List

from bibabot.IBot import IBot
from bibabot.ICommand import ICommand

class BotHandler():
    def __init__(self, bot_impl: IBot, commands: List[ICommand]):
        self.bot = bot_impl
        self.commands = commands
        
    def handle_command(self, command: str):
        logging.info(f"Looking for a command object to handle '{command}'...")
        command_found = False
        for cmd in self.commands:
            if cmd.is_valid_command(command):
                logging.info(f"Found valid command: {type(cmd).__name__}")
                command_found = True
                for msg in cmd.get_messages_from_command(command):
                    self.bot.send_message(msg)
                    time.sleep(.5) # wait a bit before sending the next message to avoid running into rate limits
                    
        if not command_found:
            logging.info(f"Could not find a command object to handle '{command}'...")
    