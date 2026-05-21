from script_engine import ScriptEngine
from paho.mqtt import client as mqtt_client
import os
sp1 = ScriptEngine() # Empty state.
start_var = True
play_var = True

if not (sp1.load_script("eva_scripts/pcb2_evaml.xml")):
    exit(1)

sp1.initialize()

client = mqtt_client.Client()
client.connect("host.docker.internal", 1883, 60) 
start_topic = f"BROKER/EVA/{os.getenv("USER_ID")}/START"
set_script_topic = f"BROKER/EVA/{os.getenv("USER_ID")}/SET_SCRIPT"
reset_topic = f"BROKER/EVA/{os.getenv("USER_ID")}/RESET"
kill_topic = f"BROKER/EVA/{os.getenv("USER_ID")}/KILL"
end_topic = f"EVA/BROKER/{os.getenv("USER_ID")}/END_SCRIPT"
error_topic = f"EVA/BROKER/{os.getenv("USER_ID")}/ERROR"

client.subscribe(start_topic) 
client.subscribe(set_script_topic) 
client.subscribe(kill_topic) 

def on_message(client : mqtt_client.Client, userdata, message):
    global start_var
    if message.topic == start_topic:
        sp1.start_script("simulator")
        start_var = False 
    elif message.topic == set_script_topic:
        if(sp1.get_state() == "PLAY"):
            client.publish(error_topic, "RUNNING ERROR | Você deve para o simulador antes de trocar o script.")
            return
        start_var = True
        sp1.reset()
        if not sp1.load_script(f"eva_scripts/{message.payload.decode("utf-8")}"):
            client.publish(error_topic, "LOAD ERROR | Houve um erro inesperado ao carregar o script.")
            return
        sp1.initialize()
    elif message.topic == reset_topic:
        start_var = True
        sp1.reset()
    elif message.topic == kill_topic:
        global play_var
        play_var = False


client.on_message = on_message 
client.loop_start()

while play_var: 
    while(start_var):
        pass

    if sp1.get_state() == "PLAY":
        sp1.play_next()
    else:
        client.publish(end_topic)
        sp1.reset()
        start_var = True



