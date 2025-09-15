from rich import print

from base_command_handler import BaseCommandHandler


class CommandHandler(BaseCommandHandler):

    def node_process(self, node, memory):
        """ Node process function """
            
        print("[b white]State: Setting [/]the [b white] light effects=" + node.get("mode") + "[/].")

        return node # It returns the same node