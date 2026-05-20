import sys

from rich import print

import robot_profile  # Module with network device configurations.

import config

from base_command_handler import BaseCommandHandler

class CommandHandler(BaseCommandHandler):

    def __init__(self, xml_node, communicator_obj):
        
        super().__init__(self, communicator_obj)

    def node_process(self, xml_node, memory):
        """ Node handling function """

        topic_base = memory.get_base_topic()

        if xml_node.get("leftArm") != None: # Move the left arm
            print("[b white]State:[/] [b white]Moving[/] the [b white]LEFT ARM[/]. [b white]Type: [/][reverse b white on black] " + xml_node.attrib["leftArm"] + " [/].")
        if xml_node.get("rightArm") != None: # Move the right arm
            print("[b white]State:[/] [b white]Moving[/] the [b white]RIGHT ARM[/]. [b white]Type: [/][reverse b white on black] " + xml_node.attrib["rightArm"] + " [/].")
        if xml_node.get("head") != None: # Move head with the new format (<head> element)
            print("[b white]State:[/] [b white]Moving[/] the [b white]HEAD[/]. [b white]Type: [/][reverse b white on black] " + xml_node.attrib["head"] + " [/].")
        else: # Check if the old version was used
            if xml_node.get("type") != None: # Maintaining compatibility with the old version of the motion element
                print("[b white]State:[/] [b white]Moving[/] the [b white]HEAD[/]. [b white]Type: [/][reverse b white on black] " + xml_node.attrib["type"] + " [/].")

        
        self.send(topic_base=topic_base, pub_topic=xml_node.get("pubTopic"), mqtt_message=xml_node.attrib["head"])

        return xml_node # It returns the same node
