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
    dummy_thicc_token_temp = []
    for token in tokens:
        if token in SCLTokens.KEYWORDS:
            dummy_thicc_token_temp.append(Token("Keyword", token["Value"]))
        elif token in SCLTokens.LITERAL_TYPES:
            dummy_thicc_token_temp.append(Token("Literal", token["Value"]))
        elif token in SCLTokens.OPERATORS:
            dummy_thicc_token_temp.append(Token("Operator", token["Value"]))
        elif token in SCLTokens.DELIMITERS:
            dummy_thicc_token_temp.append(Token("Delimiter", token["Value"]))
        else:
            dummy_thicc_token_temp.append(Token("Identifier", token["Value"]))
    
    return dummy_thicc_token_temp

def create_json_doc(tokens):
    token = jsonifier(tokens)
    # for i in token:
    #         token += { "Type" : i.type, "Value": i.token}
    
    with open("Token_JSON.json", 'w') as f:
        json.dump(token, f, indent=4)
        
