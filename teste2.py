from script_engine import ScriptEngine

sp2 = ScriptEngine()
sp2.load_script("eva_scripts/pcb2_evaml.xml")
sp2.initialize(False)

sp2.start_script("terminal-plus")

while sp2.get_state() == "PLAY":
    sp2.play_next()

