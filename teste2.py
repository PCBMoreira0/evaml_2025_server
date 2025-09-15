from script_engine import ScriptEngine

sp2 = ScriptEngine()

if not (sp2.load_script("eva_scripts/pcb2_evaml.xml")):
    # We have a problem with the file.
    exit(1)

sp2.initialize(False)

sp2.start_script("terminal-plus")

while sp2.get_state() == "PLAY":
    sp2.play_next()

