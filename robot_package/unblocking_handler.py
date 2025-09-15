from abc import ABC, abstractmethod

class UnblockingHandler(ABC):
    """
    Interface for commands that depend on an unlock
    initiated by the physical robot.
    """

    @abstractmethod
    def unblock(self):
        pass