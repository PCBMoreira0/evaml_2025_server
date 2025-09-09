import sys
import os

from rich import print
from rich.console import Console

from lxml import etree as ET


from module_loader import ModuleLoader
from script_metadata import ScriptMetadata

from robot_memory import RobotMemory

sys.path.append(os.getcwd() + "/" + "robot_package/")

console = Console()



class ScriptEngine:
    def __init__(self):
        # Player Object states:
        # "EMPTY" - O objeto foi criado e nenhum script foi carregado na memória.
        # "NOT_INIT" - O objeto já leu o script mas precisa ser inicializado. Na inicialização os módulos são carregado e a tabela de IDs e gerada.
        # "IDLE" - O objeto script_player já foi incializado e está pronto para executar um script do início ou o player terminou de executar um script.
        # "PLAY" - Nesse estado o player está executando um script.
        # "BLOCKED" - O player está bloqueado aguardando a finalização do processamento de um módulo, como o talk, por exemplo.

        self.__state = "EMPTY"
        self.__robot_memory = RobotMemory() # Cria o objeto de memória do "robô"
        self.__root = None # Elemento root do arquivo XML
        self.__moduleloader = ModuleLoader()
        self.__scriptmetadata = ScriptMetadata()

    # get the player state
    def get_state(self):
        return self.__state 


    def load_script(self, script_file):
        self.script_file  = script_file
        
        try:
            tree = ET.parse(self.script_file)  # XML code file
        except:
            print("[b blink reverse red] We have a problem... I can't find the file: " + script_file + "[/]")
            exit(1)
            # Retornar False para falha....
        
        self.__root = tree.getroot() # script root node
        self.__state  = "NOT_INIT"

        return True
        


    # Rodar antes de um play para posicionar o inicio do XML
    def initialize(self, verbose_mode=True):
        if self.__state != "NOT_INIT":
            if self.__state == "EMPTY":
                print("O Player se encontra no estado EMPTY e não pode ser inicializado. Primeiro, carregue um script!")
                return False # A incialização não ocorreu
            else:
                print("O Player já foi inicializado e se encontra no estado " + self.__state + ".")
                return False # A incialização não ocorreu
        
        self.__robot_memory = RobotMemory() # Reseta a memória do "robô"
        
        # Loading commands modules
        # # Contains the association between the element names and their modules.
        # The key is the element tag and the value is a list with two elements:
        # 1) the number of occurrences of the element in the script.
        # 2) the object that points to the imported module.
        self.tab_modules = self.__moduleloader.import_modules(self.__root, verbose_mode) # Load modules dynamically
        # This table must contain all elements with "id", that is, those that can be called by a <goto> or by a <useMacro>.
        self.__robot_memory.tab_ids = self.__scriptmetadata.identify_targets(self.__root, verbose_mode) # Identify scrpit elements

        self.settings_node = self.__root.find("settings")
        self.script_node = self.__root.find("script")
        self.__state = "IDLE"
        return True # Tudo ok!
        


    def start_script(self, running_mode="terminal"):
        if self.__state != "IDLE":
            print("O Player não se encontra no estado IDLE.")
            return False

        console.rule("🤖 [yellow reverse b]  Starting the script - Reading the global <settings> from file: " + self.script_file + "  [/] 🤖\n")
        self.__robot_memory.reset_memory()
        self.__robot_memory.running_mode = running_mode

        # Executa a seção <settings>
        self.node = self.settings_node[0] # Primero nó da seção <settings>
        self.__state = "PLAY"
        self.play_next() # <voice>
        self.play_next() # <lightEffects>
        self.play_next() # <audioEffects>
        
        # Aponta para o primeiro nó da seção <script>
        self.node = self.script_node[0] # Primero nó da seção <script>
        self.__state = "PLAY"
        console.rule("🤖 [red reverse b]  Executing the script: " + self.script_file + "  [/] 🤖\n")


    # play the script
    def play_next(self): 
        if self.__state != "PLAY":
            print("O Player não se encontra no estado PLAY e não pode ser resetado.")
            return False
        # # Versão iterativa do player. Agora o XML é lido de maneira iterativa, sem recursão.
        # while True: # Roda até ser interrompido por um break.
        if self.node == None: # None significa o fim de um um nível, onde não existe mais um nó irmão.
            if len(self.__robot_memory.node_stack) != 0: # Se tem elemento na pilha.
                self.node = self.__robot_memory.node_stack.pop()
            else:
                if self.__state  == "PLAY":
                    # End of script
                    print('[b white]State:[/] [b white]End of script![/] 🎈🥳🥳🎈\n')
                    console.rule("🤖 [green reverse b]  Script finished: " + self.script_file + "  [/] 🤖")
                    print("\n\n")
                self.__state  = "IDLE"
                return True# break

        # Processa os nós que têm filhos.
        elif len(self.node) > 0:
            if self.node.tag == "switch":
                if self.node.getnext() != None: # O nó "switch" tem um irmão adiante.
                    self.__robot_memory.node_stack.append(self.node.getnext()) # Nó que será executado após o retorno do <switch>.
                mod = self.tab_modules[self.node.tag][2]
                self.node = eval('mod.node_processing')(self.node, self.__robot_memory) # Executa o <switch> colocando seu operador na memória.
                self.node = self.node[0] # Primeiro <case> do <switch>

            elif self.node.tag == "case":
                # Um case só executa se houver um operador do switch na memória.
                if self.__robot_memory.op_switch != None: # Deve haver um operador do switch na memória. None indica que um case verdadeiro já ocorreu neste switch
                    mod = self.tab_modules[self.node.tag][2]
                    self.node = eval('mod.node_processing')(self.node, self.__robot_memory) # Executa o elemento <case> comparando com o operador (do switch) na memória. O result. da comparação fica em self.memory.flag_case.
                    if self.__robot_memory.flag_case == True:
                        self.__robot_memory.flag_case = False
                        self.__robot_memory.op_switch = None
                        self.node = self.node[0] # Executa o primeiro nó do elemento composto <case> (True).
                    else:
                        # Tenta buscar o case seguinte ou o default.
                        # Senão encontrar, node será None.
                        self.node = self.node.getnext() 
                else:
                    # if len(memory.node_stack) != 0:
                    self.node = self.node.getnext() 

            elif self.node.tag == "default" and self.__robot_memory.op_switch != None: # Se chegou aqui... então executa!
                mod = self.tab_modules[self.node.tag][2]
                self.node = eval('mod.node_processing')(self.node, self.__robot_memory)
                self.node = self.node[0] # Primeiro nó do <Default>
            
            else:
                self.node = self.node.getnext()

        else: # Execução de nós comuns.
            # Alguns casos de nós especiais.
            if self.node.tag == "goto":
                mod = self.tab_modules[self.node.tag][2]
                self.node = eval('mod.node_processing')(self.node, self.__robot_memory) # Executa o <goto> que retorna o nó destino (target).
                self.node_target = self.node # Armazena o target do goto.
                # Com a execução sendo direcionada para o nó "target" do <goto>
                # Os nós na pilha de endereços de retorno podem perder o significado, caso o goto direcione
                # a execução para um nó destino que pertence a um outro pai, dieferente do pai do goto.
                # É preciso zerar a pilha e inserir novos nó que são os pais do nó "target".
                self.__robot_memory.node_stack = []

                # Primeiro elemento da node_stack deve ser o próprio node target.
                self.__robot_memory.node_stack.append(self.node_target)
                self.node = self.node_target.getparent()

                # Busca pelos pais do node target.
                # Cases não são considerados, pois para se executar um case é preciso ter informação do switch que seria o pai dos cases.
                # Sendo assim, os switchs são considerados na busca pelos pais e por último o root (script).
                # As macros também são considerdas como pais dos seus grupos de comandos, mas não....
                while self.node.tag != "script" and self.node.tag != "macro":
                    if self.node.tag == "switch":
                        if self.node.getnext() == None:
                            self.node = self.node.getparent()
                        else:
                            self.__robot_memory.node_stack.append(self.node.getnext())
                            self.node = self.node.getparent()
                    else:
                        self.node = self.node.getparent()

                self.__robot_memory.node_stack.reverse()
                self.node = None # Vai forçar a leitura da node_stack.

            elif self.node.tag == "useMacro": # Tratando elemento <useMacro>
                if self.node.getnext() != None: # O nó "useMacro" tem um irmão adiante.
                    self.__robot_memory.node_stack.append(self.node.getnext()) # Nó que será executado após o retorno do <useMacro>.
                
                mod = self.tab_modules[self.node.tag][2]
                self.node = eval('mod.node_processing')(self.node, self.__robot_memory) # Executa o <useMacro> que retorna o nó "macro".
                self.node = self.node[0] # Primeiro nó  dentro da "macro"

            else:
                mod = self.tab_modules[self.node.tag][2]
                self.node = eval('mod.node_processing')(self.node, self.__robot_memory)
                if self.node.tag == "stop":
                    if self.__state  == "PLAY":
                        # End of script
                        print('[b white]State:[/] [b white]End of script![/] 🎈🥳🥳🎈')
                        print()
                        console.rule("🤖 [green reverse b]  Script finished: " + self.script_file + "  [/] 🤖\n\n\n")
                        print("\n\n")
                    self.__state  = "IDLE"
                    return True # break
                self.node = self.node.getnext() # Chama o próximo irmão do no corrente.


    # Faz com que o play possa voltar do início do script, resetando a memória sem resetar a tabela de IDs    
    def reset(self):
        if self.__state != "PLAY":
            print("O Player não se encontra no estado PLAY e não pode ser resetado.")
            return False
        self.__state  = "IDLE"
        self.node = self.script_node[0] # Primeiro nó do script.
        self.__robot_memory.reset_memory()
        return True