from robot_package.communicatior_interface import CommunicationInterface

class MyModule:
    def __init__(self, comms_strategy: CommunicationInterface):
        self.comms = comms_strategy

    def process_command(self, command_data):
        self.comms.send(command_data)
        response = self.comms.receive()
        print(f"Módulo: Processamento concluído com resposta -> {response}")