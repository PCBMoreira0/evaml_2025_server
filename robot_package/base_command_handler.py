from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET

class BaseCommandHandler(ABC):
    """
    Base class for all EvaML language command modules.
    All must implement the node_process() method.
    """

    @abstractmethod
    def node_process(self, xml_node: ET.Element, memory) -> ET.Element:
        """
        Processes the XML node corresponding to the command.
        """

