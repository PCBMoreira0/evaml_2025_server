import time

from rich import print

import config

import robot_profile  # Module with network device configurations.

robot_topic_base = robot_profile.ROBOT_TOPIC_BASE

from base_command_handler import BaseCommandHandler

class CommandHandler(BaseCommandHandler):

    def node_process(self, node, memory):
        """ Função de tratamento do nó """
        if memory.running_mode == "simulator":
            topic_base = config.SIMULATOR_TOPIC_BASE
        elif memory.running_mode == "robot":
            topic_base = robot_profile.ROBOT_TOPIC_BASE
        else:
            topic_base = config.TERMINAL_TOPIC_BASE
            
        print("[b white]State: Setting [/]the robot [b white]LEDs[/] to the animation/color [bold]" + node.get("animation") + "![/].")

        message = node.get("animation")
        

        if topic_base != "TERMINAL":
            # client_mqtt.publish(topic_base + '/' + "leds", "STOP") # Although node.tag is "led" the defined topic was "leds".
            time.sleep(0.1)
            # client_mqtt.publish(topic_base + '/' + "leds", message) # Although node.tag is "led" the defined topic was "leds".

        return node # It returns the same node