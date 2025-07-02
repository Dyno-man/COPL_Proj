import os
import sys
import re
from jsonifier import *

KEYWORDS = SCLTokens.KEYWORDS
KEYWORDS_WITHOUT_IDENTIFIERS = SCLTokens.KEYWORDS_WITHOUT_IDENTIFIERS
KEYWORDS_WITH_IDENTIFIERS = SCLTokens.KEYWORDS_WITH_IDENTIFIERS
LITERAL_TYPES = SCLTokens.LITERAL_TYPES
OPERATORS = SCLTokens.OPERATORS
DELIMITERS = SCLTokens.DELIMITERS
IDENTIFIERS = SCLTokens.IDENTIFIERS

# Combine regex patterns
token_specification = [
    ("KEYWORD",    r"//|\*/"),
    ("NUMBER",     r'\d+(\.\d+)?'),
    ("STRING",     r'"[^"\n]*"'),
    ("APOSTROPHE", r"'[^'\n]*'"),
    ("ID",         r'[A-Za-z_]\w*'),
    ("OP",         '|'.join(map(re.escape, OPERATORS))),
    ("DELIM",      '|'.join(map(re.escape, DELIMITERS))),
    ("NEWLINE",    r'\n'),
    ("SKIP",       r'[ \t]+'),
    ("MISMATCH",   r'.')
]


token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

def tokenize(code):
    tokens = []
    identifiers = set()

    # Iterate over every match in regex pattern
    for match in re.finditer(token_regex, code):
        type = match.lastgroup
        value = match.group()

        if type == "NUMBER": # Handles numbers
            value = float(value) if '.' in value else int(value)
        elif type == "STRING": # Handles string literals
            type = "STRING_LITERAL"
            value = value.strip('"')
        elif type == "ID": # Handles identifiers and keywords
            if value in KEYWORDS:
                type = "KEYWORD"
            elif value in LITERAL_TYPES:
                type = "LITERAL"
            else:
                type = "IDENTIFIER"
                identifiers.add(value)
        elif type == "SKIP" or type == "NEWLINE": # Skips whitespace
            continue
        elif type == "MISMATCH": # Handles mismatched characters
            raise RuntimeError(f'Unexpected character: {value!r}')

        # Add token to list
        tokens.append({"Type": type, "Value": value})
        # print(f'Token: {type}, Value: {value}')

    return tokens, sorted(identifiers)

def main():
    sclFile = sys.argv[1]

    if os.path.isfile(sclFile):
        with open(sclFile, 'r') as f:
            code = f.read()

        tokens, identifiers = tokenize(code)
        create_json_doc(tokens, sclFile)

    else:
        files = os.listdir(sclFile)
        for file in files:
            if file.endswith('.scl'):
                with open((sclFile + "/" + file), 'r') as f:
                    code = f.read()
                tokens, identifiers = tokenize(code)
                create_json_doc(tokens, file)
    print(identifiers)


if __name__ == "__main__":
    main()
