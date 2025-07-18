import sys
import os
from scl_scanner import tokenize
from jsonifier import create_json_doc
from executor import *

#For the purposes of this assignment to run the code do python3 main.py SCL/welcome.scl

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <file.scl>")
        return

    scl_file = sys.argv[1]

    if not os.path.isfile(scl_file):
        print(f"File not found: {scl_file}")
        return

    # Read the .scl file
    with open(scl_file, 'r') as f:
        code = f.read()

    # Run scanner/tokenizer
    tokens_list, identifiers = tokenize(code)
    create_json_doc(tokens_list, scl_file)
    from parser import loadJSON, start, tokens

    # Load tokens into the parser
    json_file = scl_file + "_Token_JSON.json"
    loadJSON(json_file)

    # Parse and execute the code
    print("=== Parsing & Execution ===")
    token_list = start()
    # for token in token_list:
    #     print(token)
    print("=== Done ===")

    print("=== Starting Executor ===")
    start_executor(token_list)
    print("=== Done ===")

if __name__ == "__main__":
    main()
