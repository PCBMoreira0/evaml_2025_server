from rich import print

import re

from base_command_handler import BaseCommandHandler

class CommandHandler(BaseCommandHandler):

    def __init__(self, xml_node, communicator_obj):
        
        super().__init__(self, communicator_obj)

    def node_process(self, xml_node, memory):
        """ Node handling function """

        if (len(xml_node.get("pubTopic"))) == 0: # error
            print("[b white on red blink] FATAL ERROR [/]: The [bold white]MQTT topic[/] is [b reverse white] EMPTY [/].✋⛔️")
            exit(1)

        if xml_node.text == None: # There is no text to send.
            print("[b white on red blink] FATAL ERROR [/]:[bold] There is [b reverse white] no message [/] to send.✋⛔️")
            exit(1)

        texto = xml_node.text
        palavras = texto.split()
        texto = ' '.join(palavras) # Removing more than one space between words.
        texto = texto.replace('\n', '').replace('\r', '').replace('\t', '') # Remove tabs and line breaks.
        # Replace variables throughout the text. variables must exist in memory
        if "#" in texto:
            var_list = re.findall(r'\#[a-zA-Z]+[a-zA-Z0-9_-]*', texto) # Generate list of occurrences of vars (#...)
            for v in var_list:
                if v[1:] in memory.vars:
                    texto = texto.replace(v, str(memory.vars[v[1:]]))
                    print(texto)
                else:
                    # If the variable does not exist in the robot's memory, it displays an error message
                    print("[b white on red blink] FATAL ERROR [/]:  The variable [b white]" + v[1:] + "[/] used in[b white] MQTT[/] element,[b yellow reverse] has not been declared [/]. Please, check your code.✋⛔️")
                    exit(1)

        # This part replaces the $, or the $-1 or the $1 in the text
        if "$" in texto: # Check if there is $ in the text
            # Checks if var_dollar has any value in the robot's memory
            if (len(memory.var_dolar)) == 0:
                exit(1)
            else: # Find the patterns $ $n or $-n in the string and replace with the corresponding values
                dollars_list = re.findall(r'\$[-0-9]*', texto) # Find dollar patterns and return a list of occurrences
                dollars_list = sorted(dollars_list, key=len, reverse=True) # Sort the list in descending order of length (of the element)
                for var_dollar in dollars_list:
                    if len(var_dollar) == 1: # Is the dollar ($)
                        texto = texto.replace(var_dollar, memory.var_dolar[-1][0])
                    else: # May be of type $n or $-n
                        if "-" in var_dollar: # $-n type
                            indice = int(var_dollar[2:]) # Var dollar is of type $-n. then just take n and convert it to int
                            texto = texto.replace(var_dollar, memory.var_dolar[-(indice + 1)][0]) 
                        else: # tipo $n
                            indice = int(var_dollar[1:]) # Var dollar is of type $n. then just take n and convert it to int
                            texto = texto.replace(var_dollar, memory.var_dolar[(indice - 1)][0])

        print("[b white ]STATE[/]:[bold] Sending the [b white]MQTT message: [/][yellow]" + texto + "[/]. [b white] TOPIC: [/][reverse cyan] " + xml_node.get("pubTopic") + " [/].") #  to the topic: [b white]" + node.get("topic") + "[/]."

        # Send the message
        if memory.running_mode == "robot":
            # Send to the robot.
            # client_mqtt.publish(xml_node.get("topic"), texto)   
            self.send(texto) 
        else:
            # client_mqtt.publish(xml_node.get("topic"), texto)  
            self.send(texto) 
        
        return xml_node # It returns the same node
