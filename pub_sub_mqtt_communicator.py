import paho.mqtt.client as mqtt
import queue
from communicator_interface import CommunicatorInterface # Supondo a interface em um arquivo separado

import config

import robot_profile

# Estratégia 3: Envio e Resposta Síncronos via MQTT
class PubSubMqttComunicator(CommunicatorInterface):
    def __init__(self, node_xml):

        # Criação do cliente Paho MQTT
        self.client = mqtt.Client()
        
        # Definição das callbacks de conexão e mensagem
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        
        # Conexão e início do loop
        self.client.connect(config.MQTT_BROKER_ADRESS, config.MQTT_PORT, 60)
        
        self.pub_topic = node_xml.get("pubTopic")
        self.sub_topic = node_xml.get("subTopic")
        self.response_queue = queue.Queue()
        self.client.loop_start()
        print(f"Sync MQTT: Configurado. Tópicos req:'{self.pub_topic}', resp:'{self.sub_topic }'")

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Sync MQTT: Conectado. Assinando tópicos de resposta...")
            # A assinatura é crucial para a reconexão
            client.subscribe(robot_profile.ROBOT_TOPIC_BASE + "/" + self.sub_topic)
        else:
            print(f"Sync MQTT: Falha na conexão com código {rc}.")
    
    def _on_message(self, client, userdata, msg):
        # Colocando a mensagem recebida na fila para processamento síncrono
        print(f"Sync MQTT: Mensagem recebida de '{msg.topic}', colocando na fila.")
        self.response_queue.put(msg.payload.decode())

    # def send(self, data: dict):
    #     # Lógica de envio
    #     self.client.publish(self.pub_topic, str(data))
    #     print(f"Sync MQTT: Enviando requisição síncrona -> {data}")
    def send(self, **kwargs):
        # Lógica de envio
        self.topic_base = ""
        if kwargs["topic_base"]:
            self.topic_base = kwargs["topic_base"] + "/"
        mqtt_message = kwargs["mqtt_message"]
        self.client.publish(self.topic_base + self.pub_topic, mqtt_message)
        print(f"OneWay MQTT: Enviando comando unidirecional -> {mqtt_message}")

    def receive(self) -> dict:
        # Lógica de recebimento síncrono (bloqueia)
        print("Sync MQTT: Bloqueando e aguardando resposta...")
        response = self.response_queue.get()
        print(f"Sync MQTT: Resposta recebida -> {response}")
        return {"response": response}