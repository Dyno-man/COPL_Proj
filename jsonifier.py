# Need to take the tokens after being read into a list, and convert them into token objects
# After the conversion they need to be appended to a json file 
from token_classifier import SCLTokens
import json 


def create_json_doc(tokens, filename):
    # tokens = jsonifier(tokens)
    token_json = []
    for token in tokens:
        print(f'Token: {token['Type']}, Value: {token['Value']}')
        token_json.append(dict(Type=token['Type'], Value=token['Value']))
    
    with open(filename +"_Token_JSON.json", 'w') as f:
        json.dump(token_json, f, indent=4)
        
