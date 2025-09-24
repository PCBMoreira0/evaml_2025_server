from rich import print

from base_command_handler import BaseCommandHandler

class CommandHandler(BaseCommandHandler):

    def __init__(self, xml_node, communicator_obj):
        
        super().__init__(self, communicator_obj)

    def node_process(self, xml_node, memory):
        """ Node pocess function """
        
        memory.default_voice = xml_node.get("type")
        if xml_node.get("pitchShift") != None:
            memory.default_voice_pitch_shift = xml_node.get("pitchShift")
        else:
            memory.default_voice_pitch_shift = "0"
            
        print("[b white]State: Setting [/]the robot default[b white] voice=" + xml_node.get("type") + "[/], with [b white]pitch shift=" + memory.default_voice_pitch_shift + "[/].")

        return xml_node # It returns the same node