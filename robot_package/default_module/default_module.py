from rich import print

from base_command_handler import BaseCommandHandler

class CommandHandler(BaseCommandHandler):
    
    def node_process(self, node, memory):
        """ Node handling function """
        print("[b white]State:[/] Executing the [b green reverse] Default [/] option.")
        
        return node # It returns the same node
    
