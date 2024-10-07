
from bibabot.ICommand import ICommand

class BibaCommand(ICommand):
    def is_valid_command(self, command: str) -> bool:
        return command.startswith('/biba')

    def get_message_from_command(self, command: str) -> str:
        return 'Hello this is Bibabot!'
