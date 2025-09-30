from rich import print

import robot_profile  # Module with network device configurations.

import config

from base_command_handler import BaseCommandHandler

class CommandHandler(BaseCommandHandler):

    def __init__(self, xml_node, communicator_obj):
        
        super().__init__(self, communicator_obj)

    def node_process(self, xml_node, memory):
        """ Node handling function """

        if memory.get_running_mode() == "simulator":
            topic_base = config.SIMULATOR_TOPIC_BASE

        elif memory.get_running_mode() == "robot":
            topic_base = robot_profile.ROBOT_TOPIC_BASE

        else:
            topic_base = config.TERMINAL_TOPIC_BASE


        if xml_node.get("emotion") == "NEUTRAL":
            emoji = " 😐"
        elif xml_node.get("emotion") == "ANGRY":
            emoji = " 😡"
        elif xml_node.get("emotion") == "DISGUST":
            emoji = " 😖"
        elif xml_node.get("emotion") == "FEAR":
            emoji = " 😧"
        elif xml_node.get("emotion") == "HAPPY":
            emoji = " 😄"
        elif xml_node.get("emotion") == "INLOVE":
            emoji = " 🥰"
        elif xml_node.get("emotion") == "SAD":
            emoji = " 😔"
        elif xml_node.get("emotion") == "SURPRISE":
            emoji = " 😲"

        print("[b white]State:[/] Setting the robot [b white]expression[/] to [b white]" + xml_node.get("emotion") + emoji + "[/].")

        message = xml_node.get("emotion")

        if topic_base == config.SIMULATOR_TOPIC_BASE or topic_base == robot_profile.ROBOT_TOPIC_BASE:
            self.send(topic_base=topic_base, mqtt_message=message)


        return xml_node # It returns the same node

