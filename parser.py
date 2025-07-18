from token_classifier import *
import json

# ========================
# CONFIGURATION & GLOBALS
# ========================
KEYWORDS = SCLTokens.KEYWORDS
KEYWORDS_WITHOUT_IDENTIFIERS = SCLTokens.KEYWORDS_WITHOUT_IDENTIFIERS
KEYWORDS_WITH_IDENTIFIERS = SCLTokens.KEYWORDS_WITH_IDENTIFIERS
LITERAL_TYPES = SCLTokens.LITERAL_TYPES
OPERATORS = SCLTokens.OPERATORS
DELIMITERS = SCLTokens.DELIMITERS
IDENTIFIERS = SCLTokens.IDENTIFIERS

index = 0
file = "SCL/welcome.scl_TOKEN_JSON.json"
tokens = []

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def build_expr_tree():
    operators = []
    operands = []

    def precedence(op):
        return {"=": 0, "+": 1, "-": 1, "*": 2, "/": 2}.get(op, -1)

    def apply_operator():
        op = operators.pop()
        right = operands.pop()
        left = operands.pop()
        operands.append(Node(op, left, right))

    while current_token() not in (";", "EOF", "then", "do", ")", ","):
        tok = current_token()
        if tok.isdigit() or tok.replace(".", "", 1).isdigit():
            operands.append(Node(tok))
            advance()
        elif tok.isidentifier():
            operands.append(Node(tok))
            advance()
        elif tok in ("+", "-", "*", "/"):
            while operators and precedence(operators[-1]) >= precedence(tok):
                apply_operator()
            operators.append(tok)
            advance()
        elif tok == "(":
            operators.append(tok)
            advance()
        elif tok == ")":
            while operators and operators[-1] != "(":
                apply_operator()
            operators.pop()  # Remove "("
            advance()
        else:
            break

    while operators:
        apply_operator()

    return operands[0] if operands else None

def inorder_traversal(node):
    if node is None:
        return
    inorder_traversal(node.left)
    print(f"{node.value}", end=' ')
    inorder_traversal(node.right)



# =====================
# TOKEN LOADING (JSON)
# =====================
def loadJSON(fileName):
    global tokens
    with open(fileName, 'r') as file:
        data = json.load(file)

    singComm = False
    multiComm = False

    for i in data:
        type = i['Type']
        value = i['Value']

        if type == "KEYWORD" and value == "description":
            multiComm = True
            continue
        elif type == "KEYWORD" and value == "//":
            singComm = True
            continue
        elif type == "KEYWORD" and value == "*/":
            multiComm = False
            continue
        elif type == "NEWLINE" and value == "\\n":
            singComm = False
            continue

        if singComm or multiComm:
            continue

        tokens.append(i)

loadJSON(file)

# =====================
# TOKEN NAVIGATION
# =====================
def current_token():
    return tokens[index]['Value'] if index < len(tokens) else "EOF"

def advance():
    global index
    index += 1

def getNextToken():
    global index
    index += 1
    return tokens[index]

def match_token(expected):
    if current_token() == expected:
        advance()
    else:
        raise SyntaxError(f"Expected: {expected}, got {current_token()}")

# ======================================
# IDENTIFIER HANDLING & HELPER FUNCTIONS
# ======================================
def identifierExists(identifier):
    if identifier in IDENTIFIERS:
        return True
    else:
        IDENTIFIERS.append(identifier)
        return False

def check_Keyword(identifier):
    return (
        identifier in KEYWORDS or
        identifier in KEYWORDS_WITHOUT_IDENTIFIERS or
        identifier in KEYWORDS_WITH_IDENTIFIERS or
        identifier in LITERAL_TYPES or
        identifier in OPERATORS
    )

def validate_identifier(identifier):
    if check_Keyword(identifier):
        raise SyntaxError("Invalid identifier: matches a keyword")

    for character in identifier:
        if not character.isalpha() and character != "_":
            raise SyntaxError("Invalid identifier: must be alphabetic or underscore")
    return True

# ========================
# GRAMMAR RULES / PARSING
# ========================
def expr():
    term()
    while current_token() in ("+", "-", "*", "/"):
        advance()
        term()

def term():
    tok = current_token()
    if tok.isdigit():
        advance()
    elif tok.isidentifier():
        if not identifierExists(tok):
            raise SyntaxError(f"Undeclared identifier '{tok}'")
        advance()
    else:
        raise SyntaxError(f"Invalid expression term: {tok}")

def condition():
    left = current_token()
    if not left.isidentifier() or not identifierExists(left):
        raise SyntaxError(f"Invalid condition left-hand: {left}")
    advance()

    if current_token() not in ("=", "!=", "<", ">", "<=", ">="):
        raise SyntaxError(f"Expected relational operator, got '{current_token()}'")
    advance()

    right = current_token()
    if not right.isdigit() and not right.isidentifier():
        raise SyntaxError(f"Invalid right-hand side of condition: {right}")
    if right.isidentifier() and not identifierExists(right):
        raise SyntaxError(f"Undeclared identifier in condition: {right}")
    advance()


def define_stmt():
    match_token("define")

    identifier = current_token()
    validate_identifier(identifier)
    identifierExists(identifier)
    advance()

    next_tok = current_token()

    if next_tok == "=":
        match_token("=")
        value = current_token()
        if value.isdigit() or (value.startswith('"') and value.endswith('"')):
            advance()
        else:
            raise SyntaxError(f"Invalid value: {value}")

    elif next_tok == "of":
        advance()
        match_token("type")
        type_name = current_token()
        if type_name.lower() not in ("double", "integer", "string", "char"):
            raise SyntaxError(f"Unsupported type: {type_name}")
        advance()
    else:
        raise SyntaxError(f"Expected '=' or 'of' after identifier, got '{next_tok}'")


def set_stmt():
    global index

    match_token("set")
    identifier = current_token()
    validate_identifier(identifier)
    if not identifierExists(identifier):
        raise SyntaxError(f"Identifier '{identifier}' not declared")
    advance()

    match_token("=")

    print("DEBUG: Starting expression collection at:", current_token())

    expr_tokens = []
    while index < len(tokens):
        tok = tokens[index]
        token_type = tok["Type"]
        token_val = str(tok["Value"])

        if token_type in ("NUMBER", "IDENTIFIER", "OP") or token_val in ("+", "-", "*", "/", "(", ")", "="):
            expr_tokens.append(token_val)
            index += 1
        else:
            break

    print("Collected expression tokens:", expr_tokens)

    temp_tokens = [{"Type": "EXPR", "Value": val} for val in expr_tokens]
    old_tokens = tokens[:]
    old_index = index

    tokens[:] = temp_tokens
    index = 0

    tree = build_expr_tree()

    print("Inorder Traversal of Expression:")
    inorder_traversal(tree)
    print()

    tokens[:] = old_tokens
    index = old_index



def display_stmt():
    match_token("display")
    identifier = current_token()
    if not identifierExists(identifier):
        raise SyntaxError(f"Identifier '{identifier}' not declared")
    advance()

def if_stmt():
    match_token("if")
    condition()
    match_token("then")
    stmt_list()
    match_token("endif")

def while_stmt():
    match_token("while")
    condition()
    match_token("do")
    stmt_list()
    match_token("endwhile")

def display_stmt():
    match_token("display")

    while True:
        token_obj = tokens[index]
        token_type = token_obj["Type"]
        token_value = token_obj["Value"]

        if token_type == "STRING_LITERAL":
            advance()
        elif token_type == "IDENTIFIER":
            if not identifierExists(token_value):
                raise SyntaxError(f"Undeclared identifier in display: {token_value}")
            advance()
        else:
            raise SyntaxError(f"Invalid display argument: {token_value}")

        if current_token() == ",":
            advance()
        else:
            break

def exit_stmt():
    match_token("exit")


def stmt():
    token_type = tokens[index]['Type']
    token_value = tokens[index]['Value']

    if token_value == "define":
        define_stmt()
    elif token_value == "set":
        set_stmt()
    elif token_value == "display":
        display_stmt()
    elif token_value == "if":
        if_stmt()
    elif token_value == "while":
        while_stmt()
    elif token_value == "exit":
        exit_stmt()
    else:
        raise SyntaxError(f"Unexpected statement start: {token_value}")


def stmt_list():
    while index < len(tokens):
        token_value = current_token()
        token_type = tokens[index]["Type"]

        if token_value in ("define", "set", "display", "if", "while", "exit") and token_type == "KEYWORD":
            stmt()
        else:
            advance()

def begin():
    stmt_list()

def start():
    token_list = []
    for token in tokens:
        token_list.append(token)
        print(token)
    begin()
    return token_list
# ===================
# EXECUTION / DEBUG
# ===================
if __name__ == "__main__":
    for token in tokens:
        print(token)
    begin()
    print("Parsing complete.")
