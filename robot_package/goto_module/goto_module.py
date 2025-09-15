from rich import print

from base_command_handler import BaseCommandHandler

class CommandHandler(BaseCommandHandler):

    def node_process(self, node, memory):
        """ Node handling function """

        # Check if <goto> has the "target" attribute set
        target_value = node.get('target')
        if target_value == None:
            print("[red bold]Target ID no found on <goto>.")
            exit(1)

        # Search for id in tab_ids
        for key, value in memory.tab_ids.items():
            if key == node.get("target"):
                print("[b white]State:[/] Jumping ↪️  to the element [b white]" + value[1].tag.capitalize() + "[/] with [b white]id=" + value[1].get("id") + "[/].")
                return value[1] # Returns the element associated with the found id.
        
        # Could not find "id"
        print("[red bold]It was not possible to find the target: " + target_value)
        exit(1)
