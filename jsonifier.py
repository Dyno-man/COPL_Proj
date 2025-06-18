# Need to take the tokens after being read into a list, and convert them into token objects
# After the conversion they need to be appended to a json file 
from token_classifier import *
import json 

dummy_thicc_token_temp = []

class Token:
    def __init__(self, type, token):
        self.type = type
        self.token = token

    def get_token(self):
        return [self.type, self.token]


# i is the string in the tokens list
def jsonifier(tokens):
    for i in dummy_thicc_token_temp:
        if i in KEYWORDS:
            dummy_thicc_token_temp.append(Token("Keyword", i))
        elif i in LITERAL_TYPES:
            dummy_thicc_token_temp.append(Token("Literal", i))
        elif i in OPERATORS:
            dummy_thicc_token_temp.append(Token("Operator", i))
        elif i in DELIMITERS:
            dummy_thicc_token_temp.append(Token("Delimiter", i))
        else:
            dummy_thicc_token_temp.append(Token("Identifier", i))
    
    return dummy_thicc_token_temp

def create_json_doc():
    token = {}
    for i in dummy_thicc_token_temp:
            token += { "Type" : i.type, "Token": i.token}

    try:
        with open("Token_JSON.json", 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    

    with open("Token_JSON.json", 'w') as f:
        json.dump(token, f, indent=4)
        
