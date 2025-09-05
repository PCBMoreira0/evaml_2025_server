from rich import print


def get_var_ref(var, memory):
    if var[0] == "$": # Is of type $, $n, or $-n
        if len(memory.var_dolar) == 0: # The memory for $ does not yet contain any elements. The program will exit.
            print('[b white on red blink] FATAL ERROR [/]: The [b white]"' + var +'"[/] variable [b reverse yellow] was not initialized [/]. Please, check your code.✋⛔️')
            exit(1)

        if len(var) == 1: # Is the dollar ($)
            return memory.var_dolar[-1]
        else: # May be of type $n or $-n
            if "-" in var: # $-n type
                indice = int(var[2:]) # Var dollar is of type $-n. then just take n and convert it to int
                try:
                    return memory.var_dolar[-(indice + 1)] 
                except IndexError:
                    print("[b white on red blink] FATAL ERROR [/]: [b yellow reverse] Unable to access the variable [/][b white] " + var + "[/] with the [b yellow reverse] index [/] used. Please, check your code.✋⛔️")
                    exit(1)
            else: # $n type
                indice = int(var[1:]) # Var dollar is of type $n. then just take n and convert it to int
                try:
                    return memory.var_dolar[(indice - 1)]
                except IndexError:
                    print("[b white on red blink] FATAL ERROR [/]: [b yellow reverse] Unable to access the variable [/][b white] " + var + "[/] with the [b yellow reverse] index [/] used. Please, check your code.✋⛔️")
                    exit(1)
    else: # It is a user-defined variable
        # Checks if the variable already exists.
        if (var not in memory.vars):
            return None # This value will be checked when processing the operation.
        else:
            return var # Returns the var name itself (which is the key) and is the reference to the value in the variables dictionary.


def get_var_value(value, memory):
    # Values ​​in var (var_value) can only be numbers, $ (of all types) and variables without # at the beginning.
    if value[0] == "$": # Is of type $, $n, or $-n
        if len(memory.var_dolar) == 0: # The memory for $ does not yet have any elements and needs to be reset
            # memory.var_dolar.append(["", ""])
            print('[b white on red blink] FATAL ERROR [/]: The [b white]"' + value +'"[/] variable [b reverse yellow] was not initialized [/]. Please, check your code.✋⛔️')
            exit(1)

        if len(value) == 1: # Is the dollar ($)
            var_aux = memory.var_dolar[-1][0]
        else: # May be of type $n or $-n
            if "-" in value: # $-n type
                indice = int(value[2:]) # Var dollar is of type $-n. then just take n and convert it to int
                try:
                    return  memory.var_dolar[-(indice + 1)][0]
                except IndexError:
                    print("[b white on red blink] FATAL ERROR [/]: [b yellow reverse] Unable to access the variable [/][b white] " + var + "[/] with the [b yellow reverse] index [/] used. Please, check your code.✋⛔️")
                    exit(1)
                
            else: # tipo $n
                indice = int(value[1:]) # Var dollar is of type $n. then just take n and convert it to int
                try:
                    return  memory.var_dolar[(indice - 1)][0]
                except IndexError:
                    print("[b white on red blink] FATAL ERROR [/]: [b yellow reverse] Unable to access the variable [/][b white] " + var + "[/] with the [b yellow reverse] index [/] used. Please, check your code.✋⛔️")
                    exit(1)
        
        try: # Tests if it is a number.
            int(var_aux)
            return var_aux
        except:
            print('[b white on red blink] FATAL ERROR [/]: You used a [b yellow reverse] string "' + var_aux + '" [/] as [b white]op2[/] of a [b pink]<counter>[/]. Please, check your code.✋⛔️')
            exit(1)

    else: # It's a user-defined var, but without the leading # or a number.
        # Checks if the operation is different from assignment and checks if var ... DOES NOT exist in memory
        if (value not in memory.vars): # Prevents an operation (other than assignment) from being performed on a variable that does not exist in memory.
            try: # Tests if it is a number.
                int(value) # Test.
                return value
            except:
                print("[b white on red blink] FATAL ERROR [/]: The variable [b white]" + value + "[/] [b yellow reverse] has not been declared [/]. Please, check your code.✋⛔️")
                exit(1)
        else:
            try: # Tests if it is a number.
                int(memory.vars[value])
                return memory.vars[value]
            except:
                print('[b white on red blink] FATAL ERROR [/]: You used a [b yellow reverse] string "' + memory.vars[value] + '" [/] as [b white]op2[/] of a [b pink]<counter>[/]. Please, check your code.✋⛔️')
                exit(1)
        
    
def node_processing(node, memory, client_mqtt):
    """ Função de tratamento do nó """

    # Get the operator.
    op = node.get("op")

    # Gets the variable reference in the robot's memory. It can be a list (from a $) or a string (the variable's key in memory).
    # A list, because each element of $ has a value and a source (a listen, a qrread, etc.).
    var_ref = get_var_ref(node.get("var"), memory)

    # Values ​​can be numbers and references to $, $n, $-n, and #some_var.
    var_value = get_var_value(node.get("value") , memory) 

    # Start processing operations.
    if op == "=": # Perform the assignment
        if isinstance(var_ref, list): # If it's a list, then it's a reference to a $ type.
            var_ref[0] = var_value
            var_ref[1] = "<counter>" # Updates the source of the $ variable, which becomes the <counter>
            print('[b white]State:[/] [b white]Assigning[/] the value [b white]' + var_ref[0] + '[/] to the variable [b white]' + node.get("var") + "[/].")
        else: # It is a string that represents the key to the user variables dictionary.
            memory.vars[node.get("var")] = var_value
            print('[b white]State:[/] [b white]Assigning[/] the value [b white]' + str(var_value) + '[/] to the variable [b white]' + node.get("var") + "[/].")

    elif op == "+": # Perform the addition
        if isinstance(var_ref, list): # If it is a list, then it is a reference to a type of $.
            op1 = int(var_ref[0])
            op2 = var_value
            var_ref[0] = str(op1 + op2)
            var_ref[1] = "<counter>" # Update the source of the $ variable
            print('[b white]State:[/] [b white]Adding[/] the [b white]op1(' + node.get("var") + ')=' + str(op1) + '[/] and [b white]op2(' + node.get("value")  + ')=' + str(var_value) + '[/]. [b white]The result is ' + var_ref[0] + '[/].')
        else: # It is a string that represents the key to the user variables dictionary.
            if var_ref == None: # Variável não inicializada, o programa pára.
                print('[b white on red blink] FATAL ERROR [/]: The variable[b white] "' + node.get("var") + '"[/] [b reverse yellow] was not initialized [/]. Please, check your code.✋⛔️')
                exit(1)
            aux = memory.vars[var_ref]
            memory.vars[var_ref] = str(int(memory.vars[var_ref]) + int(var_value))
            print('[b white]State:[/] [b white]Adding[/] the [b white]op1(' + node.get("var") + ')=' + str(aux) + '[/] and [b white]op2(' + node.get("value")  + ')=' + str(var_value) + '[/]. [b white]The result is ' + str(memory.vars[var_ref]) + '[/].')
            
    elif op == "-": # Perform the addition
        if isinstance(var_ref, list): # If it is a list, then it is a reference to a type of $.
            op1 = int(var_ref[0])
            op2 = var_value
            var_ref[0] = str(op1 - op2)
            var_ref[1] = "<counter>" # Update the source of the $ variable
            print('[b white]State:[/] [b white]Subtracting[/] the [b white]op1(' + node.get("var") + ')=' + str(op1) + '[/] and [b white]op2(' + node.get("value")  + ')=' + str(var_value) + '[/]. [b white]The result is ' + var_ref[0] + '[/].')
        else: # It is a string that represents the key to the user variables dictionary.
            if var_ref == None: # Variable not initialized, program stops.
                print('[b white on red blink] FATAL ERROR [/]: The variable[b white] "' + node.get("var") + '"[/] [b reverse yellow] was not initialized [/]. Please, check your code.✋⛔️')
                exit(1)
            aux = memory.vars[var_ref]
            memory.vars[var_ref] = str(int(memory.vars[var_ref]) - int(var_value))
            print('[b white]State:[/] [b white]Adding[/] the [b white]op1(' + node.get("var") + ')=' + str(aux) + '[/] and [b white]op2(' + node.get("value")  + ')=' + str(var_value) + '[/]. [b white]The result is ' + str(memory.vars[var_ref]) + '[/].')
            
    elif op == "*": # Perform the product
        if isinstance(var_ref, list): # If it is a list, then it is a reference to a type of $.
            op1 = int(var_ref[0])
            op2 = var_value
            var_ref[0] = str(op1 * op2)
            var_ref[1] = "<counter>" # Update the source of the $ variable
            print('[b white]State:[/] [b white]Multiplying[/] the [b white]op1(' + node.get("var") + ')=' + str(op1) + '[/] and [b white]op2(' + node.get("value")  + ')=' + str(var_value) + '[/]. [b white]The result is ' + var_ref[0] + '[/].')
        else: # It is a string that represents the key to the user variables dictionary.
            if var_ref == None: # Variable not initialized, program stops.
                print('[b white on red blink] FATAL ERROR [/]: The variable[b white] "' + node.get("var") + '"[/] [b reverse yellow] was not initialized [/]. Please, check your code.✋⛔️')
                exit(1)
            aux = memory.vars[var_ref]
            memory.vars[var_ref] = str(int(memory.vars[var_ref]) * int(var_value))
            print('[b white]State:[/] [b white]Multiplying[/] the [b white]op1(' + node.get("var") + ')=' + str(aux) + '[/] and [b white]op2(' + node.get("value")  + ')=' + str(var_value) + '[/]. [b white]The result is ' + str(memory.vars[var_ref]) + '[/].')

    elif op == "/": # Performs the division (it was /=) but I changed it to //= (integer division)
        if isinstance(var_ref, list): # If it is a list, then it is a reference to a type of $.
            op1 = int(var_ref[0])
            op2 = var_value
            var_ref[0] = str(op1 // op2)
            var_ref[1] = "<counter>" # Update the source of the $ variable
            print('[b white]State:[/] [b white]Dividing[/] the [b white]op1(' + node.get("var") + ')=' + str(op1) + '[/] and [b white]op2(' + node.get("value")  + ')=' + str(var_value) + '[/]. [b white]The result is ' + var_ref[0] + '[/].')
        else: # It is a string that represents the key to the user variables dictionary.
            if var_ref == None: # Variable not initialized, program stops.
                print('[b white on red blink] FATAL ERROR [/]: The variable[b white] "' + node.get("var") + '"[/] [b reverse yellow] was not initialized [/]. Please, check your code.✋⛔️')
                exit(1)
            aux = memory.vars[var_ref]
            memory.vars[var_ref] = str(int(memory.vars[var_ref]) // int(var_value))
            print('[b white]State:[/] [b white]Dividing[/] the [b white]op1(' + node.get("var") + ')=' + str(aux) + '[/] and [b white]op2(' + node.get("value")  + ')=' + str(var_value) + '[/]. [b white]The result is ' + str(memory.vars[var_ref]) + '[/].')

    elif op == "^": # Calculating op1 to the power of op2.
        if isinstance(var_ref, list): # If it is a list, then it is a reference to a type of $.
            op1 = int(var_ref[0])
            op2 = var_value
            var_ref[0] = str(op1 ** op2)
            var_ref[1] = "<counter>" # Update the source of the $ variable
            print('[b white]State:[/] [b white]Calculating op1(' + node.get("var") + ')=' + str(op1) + ' [/] to the [b white]power[/] of [b white]op2(' + node.get("value")  + ')=' + str(var_value) + '[/]. [b white]The result is ' + var_ref[0] + '[/].')
        else: # It is a string that represents the key to the user variables dictionary.
            if var_ref == None: # Variável não inicializada, o programa pára.
                print('[b white on red blink] FATAL ERROR [/]: The variable[b white] "' + node.get("var") + '"[/] [b reverse yellow] was not initialized [/]. Please, check your code.✋⛔️')
                exit(1)
            aux = memory.vars[var_ref]
            memory.vars[var_ref] = str(int(memory.vars[var_ref]) ** int(var_value))
            print('[b white]State:[/] [b white]Calculating op1(' + node.get("var") + ')=' + str(aux) + ' [/]to the [b white]power[/] of [b white]op2(' + node.get("value")  + ')=' + str(var_value) + '[/]. [b white]The result is ' + str(memory.vars[var_ref]) + '[/].')

    elif op == "%": # Calculate the module
        if isinstance(var_ref, list): # If it is a list, then it is a reference to a type of $.
            op1 = int(var_ref[0])
            op2 = var_value
            var_ref[0] = str(op1 % op2)
            var_ref[1] = "<counter>" # Update the source of the $ variable
            print('[b white]State:[/] [b white]Calculating the modulus of division between[/] the [b white]op1(' + node.get("var") + ')=' + str(op1) + '[/] and [b white]op2(' + node.get("value")  + ')=' + str(var_value) + '[/]. [b white]The result is ' + var_ref[0] + '[/].')
        else: # It is a string that represents the key to the user variables dictionary.
            if var_ref == None: # Variable not initialized, program stops.
                print('[b white on red blink] FATAL ERROR [/]: The variable[b white] "' + node.get("var") + '"[/] [b reverse yellow] was not initialized [/]. Please, check your code.✋⛔️')
                exit(1)
            aux = memory.vars[var_ref]
            memory.vars[var_ref] = str(int(memory.vars[var_ref]) % int(var_value))
            print('[b white]State:[/] [b white]Calculating the modulus of division between[/] the [b white]op1(' + node.get("var") + ')=' + str(aux) + '[/] and [b white]op2(' + node.get("value")  + ')=' + str(var_value) + '[/]. [b white]The result is ' + str(memory.vars[var_ref]) + '[/].')
            

    return node # It returns the same node