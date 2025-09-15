from script_engine import ScriptEngine

sp1 = ScriptEngine()

if not (sp1.load_script("eva_scripts/tabuada_nova_evaml.xml")):
    # We have a problem with the file.
    exit(1)

sp1.initialize()

sp1.start_script()

while sp1.get_state() == "PLAY":
    sp1.play_next()



