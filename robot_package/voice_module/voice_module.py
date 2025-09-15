from rich import print

from base_command_handler import BaseCommandHandler

class CommandHandler(BaseCommandHandler):

    def node_process(self, node, memory):
        """ Node pocess function """
        memory.default_voice = node.get("type")
        if node.get("pitchShift") != None:
            memory.default_voice_pitch_shift = node.get("pitchShift")
        else:
            memory.default_voice_pitch_shift = "0"
            
        print("[b white]State: Setting [/]the robot default[b white] voice=" + node.get("type") + "[/], with [b white]pitch shift=" + memory.default_voice_pitch_shift + "[/].")

        return node # It returns the same node