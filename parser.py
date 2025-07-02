from token_classifier import *
#Iterates through the json tokens for each token
#def getNextToken():

#Checks whether the id has already been declared or not
#def identifierExists(id):  

#Starts the parser to begin syntax checking
#def begin():

#Must define our own grammar rules, for ex declare x = 5 we would take the declar stmnt, then check if id is next, then check for =, then vcheck for value
test_tokens = ["declare", "x", "=", "5", "display", "x"]
token_index = 0

def current_token():
    return test_tokens[token_index] if token_index < len(test_tokens) else "EOF"

def advance():
    global token_index
    token_index += 1

def match_token(expected):
    if current_token() == expected:
        advance()
    else:
        raise SyntaxError(f"Expected: {expected}, got {current_token()}")

#General format of the statements
def declare_stmt():
    match_token("declare")
    #Check if following token is identifier (Need to add this functionality)
    match_token("=")
    #Check if following token is a valid value (Need to add functionality)

def stmt():
    token = current_token()
    if token == "declare":
        print()
        declare_stmt()
    elif token == "set":
        print()
        #set_stmt()
    elif token == "display":
        print()
        #displat_stmt()
    elif token == "if":
        print()
        #if_smt()
    elif token == "while":
        print()
        #while_stmt()
    else:
        raise SyntaxError(f"Unexpected statement start: {token}")

def stmt_list():
    while current_token() in ("declare", "set", "display", "if", "while"):
        stmt()

def program():
    stmt_list()
