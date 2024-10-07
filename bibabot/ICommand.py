import abc

class ICommand(abc.ABC):        
    def is_valid_command(self, command: str) -> bool:
        return False
    
    @abc.abstractmethod
    def get_message_from_command(self, command: str) -> str:
        raise NotImplementedError()
        