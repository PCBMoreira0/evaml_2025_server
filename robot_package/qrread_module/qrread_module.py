 
from rich import print
from rich.console import Console

console = Console()

import robot_profile  # Module with network device configurations.

import config


from base_command_handler import BaseCommandHandler

class CommandHandler(BaseCommandHandler):

    def __init__(self, xml_node, communicator_obj):
        
        super().__init__(self, communicator_obj)

    def node_process(self, xml_node, memory):
        """ Node handling function """   

        base_topic = memory.get_base_topic()
        
    
        self.send(topic_base=base_topic, pub_topic="LEDS", mqtt_message="LISTEN")
        self.send(topic_base=base_topic, pub_topic=xml_node.get("pubTopic")) 
        
        if xml_node.get("var") == None: # Maintains compatibility with the use of the $ variable
            print('[b white]State:[/] The Robot is [b green]reading[/] [b white]a QR Code[/]. It will be stored in [b white]$[/].')
        else:
            print('[b white]State:[/] The Robot is [b green]reading[/] [b white]a QR Code[/]. It will be stored in [b white]' + xml_node.get("var") + '[/].')
        
        mqtt_response = self.receive() # self.receive() returns a dict {RESPONSE: "response"}

        self.send(topic_base=base_topic, pub_topic="LEDS", mqtt_message="STOP")
        if xml_node.get("var") == None: # Maintains compatibility with the use of the $ variable
            memory.setDollar([mqtt_response["RESPONSE"], "<qrRead>"])
        else:
            var_name = xml_node.get("var")
            memory.setVar(var_name, mqtt_response["RESPONSE"])
        print(f"[b white on green blink] > [/]{mqtt_response}")

        return xml_node # It returns the same node

