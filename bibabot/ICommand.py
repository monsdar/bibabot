import abc
from typing import List

class ICommand(abc.ABC):        
    def is_valid_command(self, command: str) -> bool:
        return False
    
    @abc.abstractmethod
    def get_messages_from_command(self, command: str) -> List[str]:
        raise NotImplementedError()
        