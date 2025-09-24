import paho.mqtt.client as mqtt
from communicator_interface import CommunicatorInterface # Supondo a interface em um arquivo separado

import config

# Estratégia 2: Envio unidirecional via MQTT
class PubMqttCommunicator(CommunicatorInterface):
    def __init__(self, xml_node):
        # 1. Criação do cliente Paho MQTT
        self.client = mqtt.Client()
        
        # 2. Definição do on_connect para resiliência de conexão
        self.client.on_connect = self._on_connect
        
        # 3. Conexão e início do loop
        self.client.connect(config.MQTT_BROKER_ADRESS, config.MQTT_PORT, 60)
        self.client.loop_start()
        
        self.topic = xml_node.get("pubTopic")
        print(f"OneWay MQTT: Configurado para envio para '{self.topic}'")
    
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("OneWay MQTT: Conectado com sucesso.")
        else:
            print(f"OneWay MQTT: Falha na conexão com código {rc}.")

    def send(self, data: dict):
        # 4. Lógica de envio
        self.client.publish(self.topic, str(data))
        print(f"OneWay MQTT: Enviando comando unidirecional -> {data}")
    
    def receive(self) -> dict:
        # A implementação é vazia, pois não recebe dados.
        print("OneWay MQTT: Comunicação unidirecional. Recebimento não suportado.")
        return {}