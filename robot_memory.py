# Is equivalent to the $ of the original Eva software.
# Is a list of results.
var_dolar = []

# Stack of return nodes, used in script execution.
node_stack = []

# Contains the results of a comparison with the <case>. Can be True, False, or None.
flag_case = None

# <switch> element operator.
op_switch = None

# Eva ram (a key/value dictionary)
vars = {}

# Contains the association between the element names and their modules.
# The key is the element tag and the value is a list with two elements:
# 1) the number of occurrences of the element in the script.
# 2) the object that points to the imported module.
tab_modules = {}

# This table must contain all elements with "id", that is, those that can be called by a <goto> or by a <useMacro>.
tab_ids = {}

# This table stores the count of sequence numbers from event logs.
log_seq_numbers = {}

# Script Player execution mode (default = terminal).
running_mode = 'terminal'

# Stores a response from the physical robot. It can be an STT text, an expression, etc.
robot_response = None

# Stores the state of the physical robot.
robot_state = "free"

# Default voice type
default_voice = None
default_voice_pitch_shift = None