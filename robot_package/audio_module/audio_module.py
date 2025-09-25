from rich import print

import sys

import os

import time

import config

sys.path.insert(0, "../")

import robot_profile  # Module with network device configurations.

import play_audio

from base_command_handler import BaseCommandHandler

class CommandHandler(BaseCommandHandler):

    def __init__(self, xml_node, communicator_obj):
        
        super().__init__(self, communicator_obj)

        
    # Função de bloqueio que é usada para sincronia entre os módulos e o Script Player
    def block(self, state, memory):
        memory.robot_state = state # Altera o estado do robô.
        while memory.robot_state != "free": # Aguarda que o robô fique livre para seguir para o próximo comando.
            time.sleep(0.01)


    def node_process(self, xml_node, memory):
        """ Função de tratamento do nó """
        if memory.running_mode == "simulator":
            topic_base = config.SIMULATOR_TOPIC_BASE
        elif memory.running_mode == "robot":
            topic_base = robot_profile.ROBOT_TOPIC_BASE
        else:
            topic_base = config.TERMINAL_TOPIC_BASE

        if xml_node.get("block") == "TRUE":
            print('[b white]State:[/][b white] Playing[/] ▶️  the sound [bold][b white]"' + xml_node.get("source") + '"[/] in [b white]BLOCKING[/] mode.')
            if topic_base != "TERMINAL":
                message = xml_node.get("source") + "|" + xml_node.get("block")
                # client_mqtt.publish(topic_base + '/' + xml_node.tag, message)
                self.block("Playing a sound", memory)
            else:
                try:
                    play_audio_obj = play_audio.create_audio_player() # Obtem a classe adequada ao SO
                    play_audio_obj.play(xml_node, os.getcwd() + "/" + config.ROBOT_PACKAGE_FOLDER + "/audio_module/audio_files/" + xml_node.get("source") + ".wav", block = True)
                except FileNotFoundError as e:
                    print('[b white on red blink] FATAL ERROR [/]: [b yellow reverse] There was a problem playing the audio file [/]: [b white]"' + xml_node.get("source") + '"[/]. Check if it [b white u]exists[/] or is in the [b white u]correct format[/] (wav).✋⛔️')
                    exit(1) 
        else:
            print('[b white]State:[/][b white] Playing[/] ▶️  the sound [bold][b white]"' + xml_node.get("source") + '"[/] in [b white]NON-BLOCKING[/] mode.')
            if topic_base != "TERMINAL":
                message = xml_node.get("source") + "|" + xml_node.get("block")
                # client_mqtt.publish(topic_base + '/' + xml_node.tag, message)
            else:
                try:
                    play_audio_obj = play_audio.create_audio_player()
                    play_audio_obj.play(xml_node, os.getcwd() + "/" + config.ROBOT_PACKAGE_FOLDER + "/audio_module/audio_files/" + xml_node.get("source") + ".wav", block = False)
                except FileNotFoundError as e:
                    print('[b white on red blink] FATAL ERROR [/]: [b yellow reverse] There was a problem playing the audio file [/]: [b white]"' + xml_node.get("source") + '"[/]. Check if it [b u white]exists[/] or is in the [b u white]correct format[/] (wav)[/].✋⛔️')
                    exit(1) 
        
        return xml_node # It returns the same node