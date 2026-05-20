import time

from rich.progress import Progress, TextColumn, BarColumn, TimeElapsedColumn

from base_command_handler import BaseCommandHandler

class CommandHandler(BaseCommandHandler):

    def __init__(self, xml_node, communicator_obj):
        
        super().__init__(self, communicator_obj)

    def node_process(self, xml_node, memory):
        """ Node handling function """

        duration = xml_node.attrib["duration"]

        seconds = int(duration)

        # Time in seconds
        tempo_total = int(seconds)

        base_topic = memory.get_base_topic()

        print("[b white]State:[/] [b white]Waiting [/]for [b white]" + str(seconds) + "[/] seconds. 🕒")
        
        self.send(topic_base=base_topic, pub_topic="WAIT", mqtt_message=tempo_total)

        return xml_node # It returns the same node