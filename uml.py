# from graphviz import Digraph

# # Criar diagrama UML de estados atualizado
# dot = Digraph("StateMachine", format="png")

# # Configurações de estilo do GRAFO (vertical)
# dot.attr(rankdir="TB", size="8")

# # --- Novas configurações de estilo dos NÓS ---
# dot.attr("node", shape="box", style="filled", fillcolor="lightblue", fontname="Helvetica", color="darkblue", fontcolor="black")

# # Nó inicial UML (círculo preto)
# dot.node("start", shape="point")

# # Estados
# dot.node("empty", "empty")
# dot.node("not_init", "not_init")
# dot.node("idle", "idle")
# dot.node("play", "play")
# dot.node("blocked", "blocked")

# # Transições
# dot.edge("start", "empty")
# dot.edge("empty", "not_init", label="load_script")
# dot.edge("not_init", "idle", label="initialize")
# dot.edge("idle", "play", label="start_script")
# dot.edge("idle", "not_init", label="load_script")
# dot.edge("play", "not_init", label="load_script")
# dot.edge("play", "idle", label="fim/reset")
# dot.edge("play", "blocked", label="start module")
# dot.edge("blocked", "play", label="finish module")

# # Renderizar
# dot.render("state_machine_with_style", format="png", cleanup=True)

from graphviz import Digraph

# Criar diagrama UML de estados atualizado
dot = Digraph("StateMachine", format="png", graph_attr={'dpi': '300'})

# Configurações de estilo do GRAFO (vertical)
dot.attr(rankdir="LR", size="8")

# Configurações de estilo dos NÓS
dot.attr("node", shape="box", style="filled", fillcolor="lightblue", fontname="Helvetica", color="darkblue", fontcolor="black")

# Nó inicial UML (círculo preto)
dot.node("start", shape="point")

# Estados
dot.node("empty", "empty")
dot.node("not_init", "not_init")
dot.node("idle", "idle")
dot.node("play", "play")
dot.node("blocked", "blocked")

# Transições
dot.edge("start", "empty")
dot.edge("empty", "not_init", label="load_script")
dot.edge("not_init", "idle", label="initialize")
dot.edge("idle", "play", label="start_script")

# Autotransição para play_next()
dot.edge("play", "play", label="play_next")

dot.edge("idle", "not_init", label="load_script")
dot.edge("play", "not_init", label="load_script")

dot.edge("play", "idle", label="finish_script/reset_player")
dot.edge("play", "blocked", label="run_module")
dot.edge("blocked", "play", label="end_module")

# Renderizar
dot.render("lr_state_machine_with_autotransition", format="png", cleanup=True)