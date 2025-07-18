variable = {}
current_token = 0

def start_executor(parsed_token_list):
    global current_token
    current_token = 0
    executor(parsed_token_list)

def has_more_display_tokens(parsed_token_list):
    if current_token < len(parsed_token_list):
        next_token = parsed_token_list[current_token]
        return next_token['Type'] == 'OP' or next_token['Value'] == ','
    return False

def advance_token(parsed_token_list):
    global current_token
    if current_token < len(parsed_token_list):
        token = parsed_token_list[current_token]
        current_token += 1
        # print(token)
        return token['Type'], token['Value']
    return None, None

def peek_token(parsed_token_list):
    if current_token < len(parsed_token_list):
        return parsed_token_list[current_token]['Value']
    return None

def executor(parsed_token_list):
    token_type, token_value = advance_token(parsed_token_list)

    while current_token < len(parsed_token_list):
        token_type, token_value = advance_token(parsed_token_list)

        if token_value == "set":
            _, identifier = advance_token(parsed_token_list)
            _, equals = advance_token(parsed_token_list)
            if equals != "=":
                raise SyntaxError("Expected '=' after identifier in 'set' statement")
            
            _, value = advance_token(parsed_token_list)
            value = variable.get(value, value)
            try:
                value = float(value)
            except:
                pass 

            while has_more_display_tokens(parsed_token_list):
                _, op = advance_token(parsed_token_list)
                _, val = advance_token(parsed_token_list)
                val = variable.get(val, val)
                try:
                    val = float(val)
                except:
                    pass

                if op == "+":
                    value += val
                elif op == "-":
                    value -= val
                elif op == "*":
                    value *= val
                elif op == "/":
                    value /= val

            variable[identifier] = value
            print(f"New Identifier set: {identifier} = {variable[identifier]}")
        
        elif token_value == "display":
            _, value = advance_token(parsed_token_list)
            output = variable.get(value, value)  

            if has_more_display_tokens(parsed_token_list):
                _, _ = advance_token(parsed_token_list)
                _, display_var = advance_token(parsed_token_list)
                output += str(variable.get(display_var))

            print("Display Output:",output)
        elif token_value == "exit":
            print("Program exited.")
            break

        elif token_value == "NEWLINE":
            continue

        elif token_value == "define":
            _, add_var = advance_token(parsed_token_list)
            
        else:
            continue

