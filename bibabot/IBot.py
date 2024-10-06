import abc

class IBot(abc.ABC):        
    @abc.abstractmethod
    def send_message(self, message):
        raise NotImplementedError()
        