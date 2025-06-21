# Need to take the tokens after being read into a list, and convert them into token objects
# After the conversion they need to be appended to a json file 
from token_classifier import SCLTokens
import json 

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def get_token(self):
        return [self.type, self.value]
    

# i is the string in the tokens list
def jsonifier(tokens):
    token_temp = []
    for token in tokens:
        if token in SCLTokens.KEYWORDS:
            token_temp.append(Token("Keyword", token["Value"]))
        elif token in SCLTokens.LITERAL_TYPES:
            token_temp.append(Token("Literal", token["Value"]))
        elif token in SCLTokens.OPERATORS:
            token_temp.append(Token("Operator", token["Value"]))
        elif token in SCLTokens.DELIMITERS:
            token_temp.append(Token("Delimiter", token["Value"]))
        else:
            token_temp.append(Token("Identifier", token["Value"]))
    
    return token_temp

def create_json_doc(tokens, filename):
    tokens = jsonifier(tokens)
    token_json = []
    for token in tokens:
        token_json.append(dict(Type=token.type, Value=token.value))
    
    with open(filename +"_Token_JSON.json", 'w') as f:
        json.dump(token_json, f, indent=4)
        
