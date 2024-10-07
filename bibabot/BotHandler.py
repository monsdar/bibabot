
import logging

from bibabot.IBot import IBot
from bibabot.ICommand import ICommand
from bibabot.BibaCommand import BibaCommand

class BotHandler():
    def __init__(self, bot_impl: IBot):
        self.bot = bot_impl
        self.commands = [
            BibaCommand(),
            ]
        
    def handle_command(self, command: str):
        logging.info(f"Looking for a command object to handle '{command}'...")
        command_found = False
        for cmd in self.commands:
            if cmd.is_valid_command(command):
                logging.info(f"Found valid command: {type(cmd).__name__}")
                command_found = True
                msg = cmd.get_message_from_command(command)
                self.bot.send_message(msg)
        if not command_found:
            logging.info(f"Could not find a command object to handle '{command}'...")
    