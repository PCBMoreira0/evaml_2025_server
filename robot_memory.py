class RobotMemory(): # 
    def __init__(self):
        # Is equivalent to the $ of the original Eva VPL software.
        # Is a list of results.
        self.var_dolar = []

        # Eva ram (a key/value dictionary)
        self.vars = {}

        # Stack of return nodes, used in script execution.
        self.node_stack = []

        # Contains the results of a comparison with the <case>. Can be True, False, or None.
        self.flag_case = None

        # <switch> element operator.
        self.op_switch = None

        # Script Player execution mode (default = terminal).
        self.running_mode = 'terminal'

        # Stores a response from the physical robot. It can be an STT text, an expression, etc.
        self.robot_response = None

        # Stores the state of the physical robot.
        self.robot_state = "free"

        # This table stores the count of sequence numbers from event logs.
        # Format {"log_name" : "number"}
        self.log_seq_numbers = {}

        # This table must contain all elements with "id", that is, those that can be called by a <goto> or by a <useMacro>.
        # Format {"Element name" : ["element_type (str)", <elment_reference>]}
        self.tab_ids = {} # Identify scrpit elements
        
        # Default voice type
        self.default_voice = None


    # Setters and Getters 
    def setDollar(self, value):
        self.var_dolar.append(value)

    def getDollar(self):
        return self.var_dolar
    
    def setVar(self, var_name, value):
        self.vars[var_name] = value

    def getVar(self, var_name):
        return self.vars[var_name]
    
    def get_node_stack(self):
        return self.node_stack
    
    def node_stack_push(self, value):
        self.node_stack.append(value)

    def node_stack_empty(self):
        self.node_stack = []

    def node_stack_reverse(self):
        self.node_stack.reverse()

    def node_stack_pop(self):
        return self.node_stack.pop()

    def node_stack_last(self):
        return self.node_stack[-1]
    
    def set_flag_case(self, value):
        self.flag_case = value

    def get_flag_case(self):
        return self.flag_case

    def set_op_switch(self, value):
        self.op_switch = value

    def get_op_switch(self):
        return self.op_switch

    def set_running_mode(self, mode):
        self.running_mode = mode

    def get_running_mode(self):
        return self.running_mode
    
    def set_robot_response(self, response):
        self.robot_response = response

    def get_robot_response(self):
        return self.robot_response

    def set_robot_state(self, state):
        self.robot_state = state

    def get_robot_state(self):
        return self.robot_state
    
    def set_log_seq_numbers(self, log_name, seg_number):
        self.log_seq_numbers[log_name] = seg_number

    def get_log_seq_numbers(self, log_name):
        return self.log_seq_numbers[log_name]
    
    def set_tab_ids(self, tab_ids): # The complete table.
        self.tab_ids = tab_ids

    def set_tab_ids_elemen_obj_ref(self, element_name, element_type, element_obj_ref):
        self.tab_ids[element_name] = [element_name, element_obj_ref]

    def get_tab_ids(self): # The complete table.
        return self.tab_ids

    def get_tab_ids_elemen_obj_ref(self, element_name):
        return self.tab_ids[element_name][1] # The obj_reference is the second element from list.
    
    def set_default_voice(self, voice_type):
        self.default_voice = voice_type

    def get_default_voice(self):
        return self.default_voice
    
    def set_default_voice_pitch_shift(self, value):
        self.default_voice_pitch_shift = value

    def get_default_voice_pitch_shift(self):
        return self.default_voice_pitch_shift
    
    def reset_memory(self): # 
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
