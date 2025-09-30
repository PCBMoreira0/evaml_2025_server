import time

from rich import print

import config

import robot_profile  # Module with network device configurations.

robot_topic_base = robot_profile.ROBOT_TOPIC_BASE

from base_command_handler import BaseCommandHandler

class CommandHandler(BaseCommandHandler):

    def __init__(self, xml_node, communicator_obj):
        
        super().__init__(self, communicator_obj)

    def node_process(self, xml_node, memory):
        """ Função de tratamento do nó """

        if memory.get_running_mode() == "simulator":
            topic_base = config.SIMULATOR_TOPIC_BASE

        elif memory.get_running_mode() == "robot":
            topic_base = robot_profile.ROBOT_TOPIC_BASE

        else:
            topic_base = config.TERMINAL_TOPIC_BASE
            
        print("[b white]State: Setting [/]the robot [b white]LEDs[/] to the animation/color [bold]" + xml_node.get("animation") + "![/].")

        message = xml_node.get("animation")
        
        
        if topic_base == config.SIMULATOR_TOPIC_BASE or topic_base == robot_profile.ROBOT_TOPIC_BASE:
            self.send(topic_base=topic_base, mqtt_message=message)


        return xml_node # It returns the same node