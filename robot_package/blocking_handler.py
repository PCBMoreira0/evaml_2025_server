from abc import ABC, abstractmethod

class BlockingHandler(ABC):
    """
    Interface for commands that need to self-block
    waiting for the physical robot to complete the action.
    """

    @abstractmethod
    def block(self):
        pass