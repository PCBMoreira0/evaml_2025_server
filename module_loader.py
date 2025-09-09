# This module defines two functions.
# A function for identifying the elements used in the script.
# A function for importing the modules associated with each of these elements.
# The import function returns a table that associates the names (tags) of the elements with the objects of the imported modules.


import sys
import os

import importlib

from rich import print, box
from rich.console import Console
from rich.table import Table

import config

console = Console()

class ModuleLoader():
    def __init__(self):
        pass


    def __identify_elements(self, xml_root, verbose_mode=False):
        """Percorre toda a seção de script identificando os elementos utilizados."""
        if verbose_mode:
            # Rich has a method to clear the screen
            console.clear()
            print("[bold underline green]Identifying script elements.[/]")
        tab_elements = {}
        for element in xml_root.iter():
            if element.tag in tab_elements:
                tab_elements[element.tag][0] = tab_elements[element.tag][0] + 1
            else:
                tab_elements[element.tag] = [1]
                if element.getparent() == None: # It is the root element (EvaML).
                    tab_elements[element.tag].append("[b white]Root element[/]")
                elif element.getparent().tag == "evaml": # Its is an EvaML section.
                    tab_elements[element.tag].append("[b magenta]Section <" +  element.tag + ">[/]")
        if verbose_mode:
            print("[white]The script uses [bold]" + str(sum(1 for _ in xml_root.iter()) - 1) + " element(s).")
        
        return tab_elements # Returns a table with the elements used in the script.


    def import_modules(self, xml_root, verbose_mode=False):
        """Importa os módulos associados a cada um dos elementos do script."""

        # At this moment, the tab_modules structure is: {elem.tag: [occurrences]}
        tab_modules = self.__identify_elements(xml_root, verbose_mode)
        # From here, the tab_modules will have its structure modified. New information will be added to its value (list).
        for element_tag in tab_modules:
            module_name = element_tag.lower() + "_module" # Default name for module folders
            diretorio = os.getcwd() + "/" + config.ROBOT_PACKAGE_FOLDER + "/" + module_name
            sys.path.insert(0, diretorio) # Put the module directory in the path.
            try:
                mod = importlib.import_module(module_name) # import the module
                tab_modules[element_tag].append(module_name + ".py")
                tab_modules[element_tag].append(mod)
            except Exception as e:
                tab_modules[element_tag].append("Not imported")
                tab_modules[element_tag].append(None)

        if verbose_mode:
            print("")
            table = Table(title="[bold]Table: XML Elements and Modules", box=box.DOUBLE_EDGE) # show_header=False, box=None (Algumas opções)
            table.add_column("XML Element")
            table.add_column("Occurrence", justify='center')
            table.add_column("Associated Module")
            # At this moment, the tab_modules structure is: {elem.tag: [occurrences, dir. do módulo, module obj]}
            for key, value in tab_modules.items():
                if value[2]: # not None
                    table.add_row("[bold yellow]" + key, "[bold cyan ]" + str(value[0]), "[bold green]" + value[1])
                else:
                    table.add_row("[bold yellow]" + key, "[bold cyan ]" + str(value[0]), "[bold red]" + value[1])
            console.print(table)
        
        return tab_modules


    
