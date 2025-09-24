from abc import ABC, abstractmethod

class CommunicatorInterface(ABC):
    @abstractmethod
    def send(self, data: dict):
        pass

    @abstractmethod
    def receive(self) -> dict:
        pass