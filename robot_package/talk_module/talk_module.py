import time

import random as rnd
import re
from rich import print

import config # Module with network device configurations.

from tts_ibm import TtsIBM

import play_speech

import robot_profile  # Module with network device configurations.


robot_topic_base = robot_profile.ROBOT_TOPIC_BASE
broker = config.MQTT_BROKER_ADRESS # Broker address.
port = config.MQTT_PORT # Broker Port.
voice_type = config.VOICE_TYPE


from base_command_handler import BaseCommandHandler

class CommandHandler(BaseCommandHandler):

    def __init__(self, xml_node, communicator_obj):
        
        super().__init__(self, communicator_obj)


    def node_process(self, xml_node, memory):
        """ Node handling function """

        if memory.running_mode == "simulator":
            topic_base = config.SIMULATOR_TOPIC_BASE
        elif memory.running_mode == "robot":
            topic_base = robot_profile.ROBOT_TOPIC_BASE
        else:
            topic_base = config.TERMINAL_TOPIC_BASE

        # Node processing
        if xml_node.text == None: # There is no text to speech
            print("[b white on red blink] FATAL ERROR [/]: [b yellow reverse] There is no text to speech [/] in the element [b white]<talk>[/]. Please, check your code.✋⛔️")
            exit(1)

        text_to_speech = xml_node.text
        palavras = text_to_speech.split()
        texto_normalizado = ' '.join(palavras)
        text_to_speech = texto_normalizado.replace('\n', '').replace('\r', '').replace('\t', '') # Remove tabulações e salto de linha.
        # Replace variables throughout the text. variables must exist in memory
        if "#" in text_to_speech:
            # Checks if the robot's memory (vars) is empty
            if memory.vars == {}:
                print("[b white on red blink] FATAL ERROR [/]: [b yellow reverse] No variables have been defined [/] to be used in the[b white] <talk>[/]. Please, check your code.✋⛔️")
                exit(1)

            var_list = re.findall(r'\#[a-zA-Z_]+[0-9]*', text_to_speech) # Generate list of occurrences of vars (#...)
            for v in var_list:
                if v[1:] in memory.vars:
                    text_to_speech = text_to_speech.replace(v, str(memory.vars[v[1:]]))
                else:
                    # If the variable does not exist in the robot's memory, it displays an error message
                    print("[b white on red blink] FATAL ERROR [/]: The variable [b white]" + v[1:] + "[/] [b yellow reverse] has not been declared [/] to be used in the [b white]<talk>[/]. Please, check your code.✋⛔️")
                    exit(1)

        # This part replaces the $, or the $-1 or the $1 in the text
        if "$" in text_to_speech: # Check if there is $ in the text
            # Checks if var_dollar has any value in the robot's memory
            if (len(memory.var_dolar)) == 0:
                print("[b white on red blink] FATAL ERROR [/]: There are [b yellow reverse] no values [/] for the [b white]$[/] used in the [b white]<talk>[/]. Please, check your code.✋⛔️")
                exit(1)
            else: # Find the patterns $ $n or $-n in the string and replace with the corresponding values
                dollars_list = re.findall(r'\$[-0-9]*', text_to_speech) # Find dollar patterns and return a list of occurrences
                dollars_list = sorted(dollars_list, key=len, reverse=True) # Sort the list in descending order of length (of the element)
                for var_dollar in dollars_list:
                    if len(var_dollar) == 1: # Is the dollar ($)
                        text_to_speech = text_to_speech.replace(var_dollar, memory.var_dolar[-1][0])
                    else: # May be of type $n or $-n
                        if "-" in var_dollar: # $-n type
                            indice = int(var_dollar[2:]) # Var dollar is of type $-n. then just take n and convert it to int.
                            try:
                                text_to_speech = text_to_speech.replace(var_dollar, memory.var_dolar[-(indice + 1)][0]) 
                            except IndexError:
                                print('[b white on red blink] FATAL ERROR [/]: There was an [b yellow reverse] index error [/] for the variable [b white]"' + var_dollar + '"[/]. Please, check your code.✋⛔️')
                                exit(1)
                        else: # tipo $n
                            indice = int(var_dollar[1:]) # Var dollar is of type $n. then just take n and convert it to int.
                            try:
                                text_to_speech = text_to_speech.replace(var_dollar, memory.var_dolar[(indice - 1)][0])
                            except IndexError:
                                print('[b white on red blink] FATAL ERROR [/]: There was an [b yellow reverse] index error [/] for the variable [b white]"' + var_dollar + '"[/]. Please, check your code.✋⛔️')
                                exit(1)
                            

        # This part implements the random text generated by using the / character
        text_to_speech = text_to_speech.split(sep="/") # Text becomes a list with the number of sentences divided by character. /
        ind_random = rnd.randint(0, len(text_to_speech)-1)

        if memory.running_mode == "terminal":
            # Rodando no modo terminal....
            print('[b white]State:[/] The Robot is [b blue]speaking[/] the sentence: [b white]"[/]', end="")
            for c in text_to_speech[ind_random]:
                print('[b white]' + c + '[/]', end="")
                time.sleep(0.08)
            print('[b white]"')


        elif memory.running_mode == "terminal-plus":
            tts_service = TtsIBM(xml_node) # Create the Text-To-Speech service obj.
            play_speech_audio = play_speech.create_audio_player()
            if xml_node.get("voiceType") == None:
                tts_file_name = tts_service.make_tts_and_play(text_to_speech[ind_random], voice_type) # This method return file_name if TTS file generated is ok.
            else:
                tts_file_name = tts_service.make_tts_and_play(text_to_speech[ind_random], xml_node.get("voiceType"))

            if tts_file_name: # A file_name is None if the tts was wrong.
                play_speech_audio.play(xml_node, text_to_speech[ind_random], tts_file_name)

        else:
            # Controls the physical robot
            print('[b white]State:[/] The Robot is [b blue]speaking[/] the sentence: [b white]"' + text_to_speech[ind_random] + '"[/]')

            if xml_node.get("voiceType") == None:
                message = memory.default_voice + "|" + memory.default_voice_pitch_shift + "|" + text_to_speech[ind_random]
            else:
                message = xml_node.get("voiceType") + "|" + xml_node.get("pitchShift") + "|" + text_to_speech[ind_random]
            
            # client_mqtt.publish(topic_base + '/' + xml_node.tag, message)
            
            # block("Speaking", memory, client_mqtt)

        return xml_node # It returns the same node
