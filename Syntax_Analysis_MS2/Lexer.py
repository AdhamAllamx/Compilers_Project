# -------------------------------
# ◆ Compiler Project – Milestone 1: Lexical Analysis (Scanner)
# -------------------------------


import re 
import os



# -------------------------------
# 1️ Define the Token Rule Class
# -------------------------------

class TokenRule:
    def __init__(self, pattern, token_type):
        self.token_type = token_type
        self.pattern = re.compile(pattern)

# -------------------------------
# 2️ Define the LexicalAnalyzer Class
# -------------------------------

class LexicalAnalyzer : 
    def __init__(self):
        # 2.1 Supported keywords
        self.keywords = {'if', 'else', 'then', 'while', 'do', 'for', 'return', 'void', 'break',
                         'continue', 'elif', 'switch', 'case', 'print', 'int', 'string'}

        # 2.2 Supported operators
        self.operators = {'+', '-', '*', '**', '/', '%', '==', ':', '!=', '<=', '>=', '&&', '||',
            '=', ';', '>', '{', '}', '(', ')'}

        # 2.3 Tokenization rules
        self.rules = [
            TokenRule( r'\b(if|else|then|while|do|for|return|void|break|continue|elif|switch|case|print|int|string)\b','KW'),
            TokenRule(r'[a-zA-Z_][a-zA-Z0-9_]*', 'ID'),   # Identifiers
            TokenRule(r'\d+', 'NUM'),                     # Numbers
            TokenRule(r'".*?"', 'STRING'),                # Strings
            TokenRule(r'\s+', None),                      # Ignore whitespace
            TokenRule( r'\*\*|\+|\-|\*|\/|%|==|:|!=|<=|>=|&&|\|\||=|;|>|\{|\}|\(|\)','OP')  # Operators 
            ]

    # -------------------------------
    # 3️ Lexer method
    # -------------------------------
    def lexer(self, file_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_dir, file_path)

        all_tokens_stream = []

        with open(full_path, 'r') as file:
            lines = file.readlines()

        for line_index, line in enumerate(lines, start=1):
            curr_index = 0
            length = len(line)
            tokens_stream = []

            while curr_index < length:
                token_found = False

                for rule in self.rules:
                    match = rule.pattern.match(line, curr_index)
                    if match:
                        token_found = True
                        token = match.group(0)

                        match rule.token_type:
                            case 'KW':
                                if token in self.keywords:
                                    tokens_stream.append(f'KW({token})')
                            case 'ID':
                                tokens_stream.append(f'ID({token})')  
                            case 'NUM': 
                                tokens_stream.append(f'NUM({token})')
                            case 'OP':
                                if token in self.operators:
                                    tokens_stream.append(f'{token}')
                            case 'STRING':
                                tokens_stream.append(f'STRING({token})')
                            case None:
                                pass  # Skipping spaces

                        curr_index += len(token)
                        break

                if not token_found:
                    # Skip unknown or invalid characters
                    curr_index += 1

            if tokens_stream:
                all_tokens_stream.append(tokens_stream)

        return all_tokens_stream

# -------------------------------
# 4️ Helper function to call lexer from parser
# -------------------------------

def tokenize(file_path):
    lexicalAnalyzer = LexicalAnalyzer()
    token_stream = lexicalAnalyzer.lexer(file_path)
    return token_stream


