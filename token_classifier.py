KEYWORDS = [
    "import", "use", "symbol", "forward", "interface", "struct", "structype",
    "function", "main", "implementations", "begin", "endfun", "if", "then", "else", "endif",
    "for", "to", "downto", "do", "endfor", "while", "endwhile", "repeat", "until", "endrepeat",
    "case", "mwhen", "default", "mendcase", "constants", "variables", "define", "description",
    "persistent", "static", "accessor", "mutator", "precondition", "potcondition",
    "parameters", "alters", "preserves", "produces", "consumes", "value", "equop",
    "return", "call", "input", "display", "displayn", "read", "write", "from", "to",
    "mfile", "mclose", "mopen", "break", "exit", "of", "array", "pointer", "using"
]

KEYWORDS_WITHOUT_IDENTIFIERS = [
    "import", "use", "forward", "implementations", "begin", "endfun",
    "if", "then", "else", "endif", "for", "to", "downto", "do", "endfor",
    "while", "endwhile", "repeat", "until", "endrepeat", "case", "mwhen",
    "default", "mendcase", "constants", "variables", "description", "persistent",
    "static", "accessor", "mutator", "precondition", "potcondition",
    "parameters", "alters", "preserves", "produces", "consumes",
    "value", "equop", "return", "display", "displayn", "from", "break",
    "exit", "array", "pointer"
]

KEYWORDS_WITH_IDENTIFIERS = [
    "symbol",       
    "interface",    
    "struct",       
    "structype",    
    "function",     
    "define",       
    "mfile",        
    "mclose",       
    "main",         
    "read",         
    "write",        
    "input",        
    "output",       
    "call",         
    "endfun",       
    "of",           
    "using",        
]

LITERAL_TYPES = ["icon", "hcon", "fcon", "string", "letter", "mtrue", "mfalse"]

OPERATORS = [
    "+", "-", "*", "/", "%", "&", "|", "^", "<<", ">>",
    "=", "==", "!=", "<", "<=", ">", ">=", ".", ",", ":", ";"
]

DELIMITERS = ["(", ")", "[", "]", "{", "}"]

IDENTIFIERS = []
