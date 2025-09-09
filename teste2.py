from script_engine import ScriptEngine

sp2 = ScriptEngine()
sp2.load_script("eva_scripts/pcb2_evaml.xml")
sp2.initialize(False)

sp2.start_script()

while sp2.get_state() == "PLAY":
    sp2.play_next()

# Simula um Do-While no Python
# while True:
#     sp2.play_next("terminal-plus")
#     if sp2.get_state() == "IDLE":
#         break


