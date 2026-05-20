 
from rich import print
from rich.console import Console

console = Console()


import robot_profile  # Module with network device configurations.

import config



# Função de bloqueio que é usada para sincronia entre os módulos e o Script Player
# def block(state, memory, client_mqtt):
#     memory.robot_state = state # Altera o estado do robô.
#     client_mqtt.publish(topic_base + "/leds", "LISTEN")
#     while memory.robot_state != "free": # Aguarda que o robô fique livre para seguir para o próximo comando.
#         time.sleep(0.01)
#     client_mqtt.publish(topic_base + "/leds", "STOP")

from base_command_handler import BaseCommandHandler

class CommandHandler(BaseCommandHandler):

    def __init__(self, xml_node, communicator_obj):
        
        super().__init__(self, communicator_obj)

    def node_process(self, xml_node, memory):
        """ Node handling function """

        base_topic = memory.get_base_topic()
        

        # Whether in terminal mode or terminal-plus mode, entries are made via the keyboard via the terminal.
        if memory.running_mode == "terminal" or memory.running_mode == "terminal-plus": 
            
            print('[b white]State:[/] The Robot is [b green]recognizing[/] [b white]the user emotion[/].', end="")

            user_answer = console.input("[b white on green blink] > [/] ")
            
            if xml_node.get("var") == None: # Maintains compatibility with the use of the $ variable
                memory.var_dollar.append([user_answer, "<userEmotion>"])
            else:
                var_name = xml_node.get("var")
                memory.vars[var_name] = user_answer
        

        elif base_topic == config.SIMULATOR_BASE_TOPIC or base_topic == robot_profile.ROBOT_BASE_TOPIC:
            print('[b white]State:[/] The Robot is [b green]recognizing[/] [b white]the user emotion[/].', end="")

            # Turn on listening LED
            self.send(topic_base=base_topic, pub_topic="LEDS", mqtt_message="LISTEN")
            self.send(topic_base=base_topic, pub_topic=xml_node.get("pubTopic")) 

            response = self.receive() # self.receive() returns a dict {RESPONSE: "response"}
            
            # Turn off listening LED
            self.send(topic_base=base_topic, pub_topic="LEDS", mqtt_message="STOP")

            print(f"[b white on green blink] > [/]{response}")
            if xml_node.get("var") == None: # Maintains compatibility with the use of the $ variable
                memory.var_dollar.append([response["RESPONSE"], "<userEmotion>"])
            else:
                var_name = xml_node.get("var")
                memory.vars[var_name] = response["RESPONSE"]

        return xml_node # It returns the same node

 
