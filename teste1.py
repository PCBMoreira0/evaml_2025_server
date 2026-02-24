from script_engine import ScriptEngine
from paho.mqtt import client as mqtt_client
import os
sp1 = ScriptEngine() # Empty state.
start_var = True

if not (sp1.load_script("eva_scripts/tabuada_nova_evaml.xml")): # If file was loaded, it is in a Not_Init state.
    # We have a problem with the file.
    exit(1)

sp1.initialize() # After initialization it is in Idle state.

client = mqtt_client.Client()
client.connect("host.docker.internal", 1883, 60) # Connect to the MQTT broker.
topic = f"EVA/{os.getenv("USER_ID")}/START"
client.subscribe(topic) # Subscribe to the topic that will receive messages from the terminal.

def on_message(client, userdata, message):
    if message.topic == topic:
        sp1.start_script("simulator") # Start the script execution when a message is received on the "EVA/START" topic.
        global start_var
        start_var = False 

client.on_message = on_message # Set the callback function for received messages.

while(start_var): # Keep the script running until it is stopped by the "stop" command.
    client.loop() # Process network events and dispatch callbacks.

client.disconnect() # Disconnect from the MQTT broker.

while sp1.get_state() == "PLAY": # It is in Play until the script finish. When finished, it will be in Idle state, again.
    sp1.play_next()



