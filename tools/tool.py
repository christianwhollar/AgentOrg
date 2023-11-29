from abc import ABC, abstractmethod

class Tool(ABC):
    @abstractmethod
    def run(self):
        pass

    @property
    @abstractmethod
    def identifier(self):
        pass

    @property
    @abstractmethod
    def command(self):
        pass