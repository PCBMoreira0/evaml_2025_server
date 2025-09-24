import paho.mqtt.client as mqtt
import queue
from communicator_interface import CommunicatorInterface # Supondo a interface em um arquivo separado

import config

# Estratégia 3: Envio e Resposta Síncronos via MQTT
class PubSubMqttComunicator(CommunicatorInterface):
    def __init__(self, node_xml):

        # 1. Criação do cliente Paho MQTT
        self.client = mqtt.Client()
        
        # 2. Definição das callbacks de conexão e mensagem
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        
        # 3. Conexão e início do loop
        self.client.connect(config.MQTT_BROKER_ADRESS, config.MQTT_PORT, 60)
        
        self.req_topic = node_xml.get("pubTopic")
        self.resp_topic = node_xml.get("subTopic")
        self.response_queue = queue.Queue()
        self.client.loop_start()
        print(f"Sync MQTT: Configurado. Tópicos req:'{self.req_topic}', resp:'{self.resp_topic }'")

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Sync MQTT: Conectado. Assinando tópicos de resposta...")
            # A assinatura é crucial para a reconexão
            client.subscribe(self.resp_topic)
        else:
            print(f"Sync MQTT: Falha na conexão com código {rc}.")
    
    def _on_message(self, client, userdata, msg):
        # 4. Colocando a mensagem recebida na fila para processamento síncrono
        print(f"Sync MQTT: Mensagem recebida de '{msg.topic}', colocando na fila.")
        self.response_queue.put(msg.payload.decode())

    def send(self, data: dict):
        # 5. Lógica de envio
        self.client.publish(self.req_topic, str(data))
        print(f"Sync MQTT: Enviando requisição síncrona -> {data}")

    def receive(self) -> dict:
        # 6. Lógica de recebimento síncrono (bloqueia)
        print("Sync MQTT: Bloqueando e aguardando resposta...")
        response = self.response_queue.get()
        print(f"Sync MQTT: Resposta recebida -> {response}")
        return {"response": response}