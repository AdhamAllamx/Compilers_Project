# ============================================
# ◆ Compiler Project – Milestone 2: Syntax Analysis (Parser)
# ============================================

#  Using PLY (Python Lex-Yacc)

# Script Structure:
# 1. Importing Lexer from Milestone 1
# 2. AST Node Classes
# 3. Parser Implementation (PLY)
# 4. Lexer Adapter and Token Mapping
# 5. Running the Parser (Input -> AST)
# ============================================

# --------------------------------------------
# 1️ Importing Lexer from Milestone 1
# --------------------------------------------

from Lexer import tokenize  # We will use the tokenize() function from our Milestone 1 Lexer

# --------------------------------------------
# 2️ AST Node Classes (For building AST tree)
# --------------------------------------------

# class ASTNode:
#     pass

# class Program(ASTNode):
#     def __init__(self, statements):
#         self.statements = statements
#     def __repr__(self):
#         return f"Program({self.statements})"

# class VarDecl(ASTNode):
#     def __init__(self, var_type, var_name):
#         self.var_type = var_type
#         self.var_name = var_name
#     def __repr__(self):
#         return f"VarDecl(type={self.var_type}, name={self.var_name})"

# class Assignment(ASTNode):
#     def __init__(self, var_name, expr):
#         self.var_name = var_name
#         self.expr = expr
#     def __repr__(self):
#         return f"Assignment(name={self.var_name}, expr={self.expr})"

# class BinOp(ASTNode):
#     def __init__(self, left, op, right):
#         self.left = left
#         self.op = op
#         self.right = right
#     def __repr__(self):
#         return f"BinOp({self.left}, '{self.op}', {self.right})"

# class Num(ASTNode):
#     def __init__(self, value):
#         self.value = value
#     def __repr__(self):
#         return f"Num({self.value})"

# class Str(ASTNode):
#     def __init__(self, value):
#         self.value = value
#     def __repr__(self):
#         return f"Str({self.value})"

# class Var(ASTNode):
#     def __init__(self, name):
#         self.name = name
#     def __repr__(self):
#         return f"Var({self.name})"

# --------------------------------------------
# 3️ Parser Implementation using PLY
# --------------------------------------------

import ply.yacc as yacc
import sys

# 3.1 Tokens used (must match Lexer tokens)
tokens = (
    'ID', 'NUM', 'STRING',
    'ADDITION','SUBTRACTION','DIVISION','MULTIPLICATION', 'EQUALS', 'SEMI',
    'INT', 'STRING_TYPE'
)

# 3.2 Token regex (PLY needs these for single-character operators)
t_PLUS = r'\+'
t_EQUALS = r'='
t_SEMI = r';'
t_ignore = ' \t'

# 3.3 Grammar rules

def p_program(p):
    '''program : stmt_list'''
    p[0] = ('program', p[1])

def p_stmt_list_multiple(p):
    '''stmt_list : stmt stmt_list'''
    p[0] = [p[1]] + p[2]

def p_stmt_list_single(p):
    '''stmt_list : stmt'''
    p[0] = [p[1]]

def p_stmt_var_decl(p):
    '''stmt : var_decl SEMI'''
    p[0] = p[1]

def p_stmt_assignment(p):
    '''stmt : assignment SEMI'''
    p[0] = p[1]

def p_var_decl(p):
    '''var_decl : type ID'''
    p[0] = ('var_decl', p[1], p[2])

def p_type(p):
    '''type : INT
            | STRING_TYPE'''
    p[0] = p[1]

def p_assignment(p):
    '''assignment : ID EQUALS expr'''
    p[0] = ('assign', p[1], p[3])

def p_expr_addition(p):
    '''expr : expr ADDITION term'''
    p[0] = ('+', p[1], p[3])

def p_expr_subtraction(p):
    '''expr : expr SUBTRACTION term'''
    p[0] = ('-', p[1], p[3])

def p_expr_multiplication(p):
    '''expr : expr MULTIPLICATION term'''
    p[0] = ('*', p[1], p[3])   

def p_expr_DIVISION(p):
    '''expr : expr DIVISION term'''
    p[0] = ('/', p[1], p[3])    

def p_expr_term(p):
    '''expr : term'''
    p[0] = p[1]

def p_term_num(p):
    '''term : NUM'''
    p[0] = ('num', p[1])

def p_term_id(p):
    '''term : ID'''
    p[0] = ('var', p[1])

def p_term_string(p):
    '''term : STRING'''
    p[0] = ('str', p[1])

def p_error(p):
    if p:
        raise SyntaxError(f"Syntax error at '{p.value}'")
    else:
        raise SyntaxError("Syntax error at EOF")

# 3.4 Build the parser
parser = yacc.yacc()

# --------------------------------------------
# 4️ Lexer Adapter and Token Mapping
# --------------------------------------------

class PlyLexerAdapter:
    def __init__(self, adapted_tokens):
        self.tokens = adapted_tokens
        self.index = 0

    def token(self):
        if self.index >= len(self.tokens):
            return None  # No more tokens

        type_, value = self.tokens[self.index]
        self.index += 1

        # Create a dummy PLY token object
        tok = yacc.YaccSymbol()
        tok.type = type_
        tok.value = value
        tok.lineno = 0
        tok.lexpos = 0
        return tok

def adapt_tokens_for_ply(token_stream):
    adapted_tokens = []

    # Map keywords/operators to PLY token names
    token_type_map = {
        'int': 'INT',
        'string': 'STRING_TYPE',
        '+': 'ADDITION',
        '=': 'EQUALS',
        '-': 'SUBTRACTION',
        '*': 'MULTIPLICATION',
        '/': 'DIVISION',
        '%': 'MODULUS',
        '==': 'EQUALS',
        '!=': 'NOT_EQUALS',
        '<=': 'LESS_EQUAL',
        '>=': 'GREATER_EQUAL',
      
        ';': 'SEMI'
    }

    for token_line in token_stream:
        for token in token_line:
            if token.startswith('KW('):
                value = token[3:-1]  
                ply_type = token_type_map.get(value, 'KW')
                adapted_tokens.append((ply_type, value))

            elif token.startswith('ID('):
                value = token[3:-1]
                adapted_tokens.append(('ID', value))

            elif token.startswith('NUM('):
                value = token[4:-1]
                adapted_tokens.append(('NUM', value))

            elif token.startswith('STRING('):
                value = token[7:-1]
                adapted_tokens.append(('STRING', value))

            elif token in token_type_map:
                ply_type = token_type_map[token]
                adapted_tokens.append((ply_type, token))

            else:
                # Unknown tokens can be ignored or handled
                pass

    return adapted_tokens

# --------------------------------------------
# 5️ Running the Parser (Input -> AST)
# --------------------------------------------

file_path = 'sample_input.txt'

# Step 1: Tokenize using Lexer (Milestone 1)
raw_tokens = tokenize(file_path)
print("Lexical Analyzer Tokens Stream:")
for stream in raw_tokens:
    print(stream)

# Step 2: Adapt tokens for PLY
adapted_tokens = adapt_tokens_for_ply(raw_tokens)


# Step 3: Create Lexer Adapter
lexer_adapter = PlyLexerAdapter(adapted_tokens)

# Step 4: Parse and get AST
ast = parser.parse(lexer=lexer_adapter)


import pprint

def custom_ast_print(ast):
    """Print AST in desired format"""
    print("('program',")
    statements = ast[1]
    for i, stmt in enumerate(statements):
        print(f"   {stmt}", end="")
        if i < len(statements) - 1:
            print(",")
        else:
            print()
    print(")")

print("\nAST from Parser:")
custom_ast_print(ast)

def print_ast(node, indent=0):
    prefix = "  " * indent
    if isinstance(node, tuple):
        # First element is the node type or operator
        print(f"{prefix}{node[0]}")
        for child in node[1:]:
            print_ast(child, indent + 1)
    elif isinstance(node, list):
        for item in node:
            print_ast(item, indent)
    else:
        print(f"{prefix}{node}")
print('this is the case after visualization')
print_ast(ast)