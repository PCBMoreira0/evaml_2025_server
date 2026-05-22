from script_engine import ScriptEngine
from paho.mqtt import client as mqtt_client
import config

from enum import Enum
import threading
import queue
import time

class Command(Enum):
    RESET = 0
    START = 1
    SET_SCRIPT = 2
    KILL = 3
    EMPTY = 4

from dataclasses import dataclass

@dataclass
class Message:
    command: Command
    payload: str

queue = queue.Queue()



sp1 = ScriptEngine() 

# connect mqtt
client = mqtt_client.Client()
client.connect(config.MQTT_BROKER_ADRESS, config.MQTT_PORT, 60)

# set controll topics
start_topic = f"BROKER/EVA/{config.SIMULATOR_BASE_TOPIC}/START"
set_script_topic = f"BROKER/EVA/{config.SIMULATOR_BASE_TOPIC}/SET_SCRIPT"
reset_topic = f"BROKER/EVA/{config.SIMULATOR_BASE_TOPIC}/RESET"
kill_topic = f"BROKER/EVA/{config.SIMULATOR_BASE_TOPIC}/KILL"
end_topic = f"EVA/BROKER/{config.SIMULATOR_BASE_TOPIC}/END_SCRIPT"
error_topic = f"EVA/BROKER/{config.SIMULATOR_BASE_TOPIC}/ERROR"

client.subscribe(start_topic) 
client.subscribe(set_script_topic) 
client.subscribe(kill_topic) 
client.subscribe(reset_topic) 

# global variables for flow control
start_var = True
play_var = True

def on_message(client : mqtt_client.Client, userdata, message):
    if message.topic == start_topic:
        queue.put_nowait(Message(Command.START, payload=""))

    elif message.topic == set_script_topic:
        queue.put_nowait(Message(Command.SET_SCRIPT, message.payload.decode("utf-8")))

    elif message.topic == reset_topic:
        queue.put_nowait(Message(Command.RESET, ""))

    elif message.topic == kill_topic:
        queue.put_nowait(Message(Command.KILL, ""))


client.on_message = on_message 
client.loop_start()

print("Simulator initialized")

def player_loop():
    global play_var, start_var

    while play_var:

        if start_var:
            time.sleep(0.05)
            continue

        if sp1.get_state() == "PLAY":
            sp1.play_next()
        else:
            client.publish(end_topic)
            sp1.reset()
            start_var = True


def command_loop():
    global play_var, start_var, sp1

    while play_var:
        message = queue.get()
        if message.command == Command.SET_SCRIPT:
            if(sp1.get_state() == "PLAY" or sp1.get_state() == "BLOCKED"):
                client.publish(error_topic, "RUNNING ERROR | Você deve parar o simulador antes de trocar o script.")
            else:
                file = message.payload
                if not sp1.load_script(f"eva_scripts/{file}"):
                    client.publish(error_topic, f"LOAD ERROR | Não foi possível encontrar o arquivo {file}.")
                else:
                    sp1.initialize()
                    start_var = True
        elif message.command == Command.START:
            if not sp1.start_script("simulator"):
                client.publish(error_topic, "START ERROR | O player não está no estado IDLE. Verifique se um script foi setado.")
            else:
                start_var = False 
        elif message.command == Command.RESET:
            while sp1.get_state() == "BLOCKED":
                client.publish(f"EVA/{config.SIMULATOR_BASE_TOPIC}/UNBLOCK", "")
                time.sleep(0.05)

            if sp1.get_state() != "PLAY" and sp1.get_state() != "IDLE":
                client.publish(error_topic, f"RESET ERROR | O simulador não está rodando.")
            else:
                sp1.reset()
                start_var = True
            
        elif message.command == Command.KILL:
            play_var = False


t1 = threading.Thread(target=player_loop)
t2 = threading.Thread(target=command_loop)

t1.start()
t2.start()
t1.join()
t2.join()

client.disconnect()

print('fim')

# while play_var: 
#     if not queue.empty():
#         message = queue.get_nowait()

#         if message.command == Command.SET_SCRIPT:
#             if(sp1.get_state() == "PLAY"):
#                 client.publish(error_topic, "RUNNING ERROR | Você deve parar o simulador antes de trocar o script.")
#             else:
#                 file = message.payload
#                 if not sp1.load_script(f"eva_scripts/{file}"):
#                     client.publish(error_topic, f"LOAD ERROR | Não foi possível encontrar o arquivo {file}.")
#                 else:
#                     sp1.initialize()
#                     start_var = True

#         elif message.command == Command.START:
#             if not sp1.start_script("simulator"):
#                 client.publish(error_topic, "START ERROR | O player não está no estado IDLE. Verifique se um script foi setado.")
#             else:
#                 start_var = False 

#         elif message.command == Command.RESET:
#             if sp1.get_state() == "BLOCKED":
#                 client.publish(f"BROKER/EVA/{config.SIMULATOR_BASE_TOPIC}/AUDIO_RESPONSE", "")
#                 # client.publish(f"BROKER/EVA/{config.SIMULATOR_BASE_TOPIC}/TALK_RESPONSE", "")
#                 # client.publish(f"BROKER/EVA/{config.SIMULATOR_BASE_TOPIC}/LISTEN_RESPONSE", "")
#                 # client.publish(f"BROKER/EVA/{config.SIMULATOR_BASE_TOPIC}/QRREAD_RESPONSE", "")
#                 # client.publish(f"BROKER/EVA/{config.SIMULATOR_BASE_TOPIC}/USEREMOTION_RESPONSE", "")
                
#             if not sp1.reset():
#                 client.publish(error_topic, f"RESET ERROR | Não foi possível encontrar reiniciar o script.")
#             else:
#                 start_var = True

#         elif message.command == Command.KILL:
#             play_var = False

#     if start_var:
#         continue

#     if sp1.get_state() == "PLAY":
#         sp1.play_next()
#     else:
#         client.publish(end_topic)
#         sp1.reset()
#         start_var = True



