class RobotMemory():
    def __init__(self):
        # Is equivalent to the $ of the original Eva software.
        # Is a list of results.
        self.var_dolar = []

        # Stack of return nodes, used in script execution.
        self.node_stack = []

        # Contains the results of a comparison with the <case>. Can be True, False, or None.
        self.flag_case = None

        # <switch> element operator.
        self.op_switch = None

        # Eva ram (a key/value dictionary)
        self.vars = {}

        # This table stores the count of sequence numbers from event logs.
        self.log_seq_numbers = {}

        # This table must contain all elements with "id", that is, those that can be called by a <goto> or by a <useMacro>.
        self.tab_ids = {} # Identify scrpit elements

        # Script Player execution mode (default = terminal).
        self.running_mode = 'terminal'

        # Stores a response from the physical robot. It can be an STT text, an expression, etc.
        self.robot_response = None

        # Stores the state of the physical robot.
        self.robot_state = "free"

        # Default voice type
        self.default_voice = None
        self.default_voice_pitch_shift = None


    def reset_memory(self):
        # 
        self.var_dolar = []
        self.node_stack = []
        self.flag_case = None
        self.op_switch = None
        self.vars = {}
        self.log_seq_numbers = {}
        self.running_mode = 'terminal'
        self.robot_response = None
        self.robot_state = "free"
