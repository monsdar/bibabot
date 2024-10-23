
from bibabot.ICommand import ICommand
from typing import List

class BibaCommand(ICommand):
    def is_valid_command(self, command: str) -> bool:
        return command.startswith('/biba')

    def get_messages_from_command(self, command: str) -> List[str]:
        return ['Hello this is Bibabot\!']
