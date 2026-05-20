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
        '''
            STOP : grey
            LISTEN : green
            SPEAK : blue
            ANGRY : red
            HAPPY : green
            SAD : blue
            SURPRISE : yellow
            WHITE : white
            RAINBOW : white
        '''

        base_topic = memory.get_base_topic()

        # print on terminal
        print('[b white]State:[/] The Robot is [b green]listening[/] in [b white]' + xml_node.get("language") + '[/]. It will be stored in [b white]$[/] ',end="")
        
        # Turn on listening LED
        self.send(topic_base=base_topic, pub_topic="LEDS", mqtt_message="LISTEN")
        self.send(topic_base=base_topic, pub_topic=xml_node.get("pubTopic")) 
        response = self.receive() # self.receive() returns a dict {RESPONSE: "response"}
        # Turn off listening LED
        self.send(topic_base=base_topic, pub_topic="LEDS", mqtt_message="STOP")

        if xml_node.get("var") == None: # Maintains compatibility with the use of the $ variable
            user_answer = response["RESPONSE"]
            memory.setDollar([user_answer, "<listen>"])
        else:
            var_name = xml_node.get("var")
            user_answer = response["RESPONSE"]
            memory.setVar(var_name, user_answer)   

        print(f"[b white on green blink] > [/]{user_answer} ")

        return xml_node # It returns the same node

