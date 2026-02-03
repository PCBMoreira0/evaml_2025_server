import paho.mqtt.client as mqtt
from communicator_interface import CommunicatorInterface

import time

import config

import sys

sys.path.append("./robot_package")


# Estratégia 2: Envio unidirecional via MQTT
class PubMqttCommunicator(CommunicatorInterface):
    def __init__(self, xml_node):
        # Criação do cliente Paho MQTT
        self.client = mqtt.Client()
        
        # Definição do on_connect para resiliência de conexão
        self.client.on_connect = self._on_connect
        
        # Conexão e início do loop
        self.client.connect(config.MQTT_BROKER_ADRESS, config.MQTT_PORT, 60)
        self.client.loop_start()
        
        self.pub_topic = xml_node.get("pubTopic")
        print(f"OneWay MQTT: Configurado para envio para '{self.pub_topic}'")
    

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("OneWay MQTT: Conectado com sucesso.")
        else:
            print(f"OneWay MQTT: Falha na conexão com código {rc}.")


    def send(self, **kwargs):
        if "mqtt_message" in kwargs:

            message = kwargs["mqtt_message"]
        else:
            message = "EMPTY_MESSAGE"
        
        if "pub_topic" in kwargs:
            self.pub_topic = kwargs["pub_topic"] # Update the pubTopic to MQTT command

        print('EVA/BROKER/' + config.SIMULATOR_BASE_TOPIC, self.pub_topic, message)
        self.client.publish('EVA/BROKER/' + config.SIMULATOR_BASE_TOPIC + '/' + self.pub_topic, message)

        print(f"OneWay MQTT: Enviando comando unidirecional -> {message}")
    

    def receive(self) -> dict:
        # A implementação é vazia, pois não recebe dados.
        print("OneWay MQTT: Comunicação unidirecional. Recebimento não suportado.")
        return {}