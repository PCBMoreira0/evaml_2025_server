from rich import print as rprint

from base_command_handler import BaseCommandHandler

class CommandHandler(BaseCommandHandler):

    def node_process(self, node, memory):
        """ Node handling function """
        rprint("[bold white]State:[/] [b white]Stopping [/]the script.")

        return node # It returns the "target" node.