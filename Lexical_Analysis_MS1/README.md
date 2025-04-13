# Milestone 1 - Lexical Analyzer

## Overview

This project implements a lexical analyzer (scanner) in Python that reads a source code file and converts it into a list of token streams. 
Each token stream represents a single line or statement in the code. 
The tokens follow a basic language syntax similar to the provided example in the milestone description.

----------------------------------------------------

## Files Included in Submission

- `lexer.ipynb`: Main Jupter Notebook Python code file containing the implementation of the lexical analyzer.
- `README.txt`: This file.
- `sample_input.txt`: A sample text file containing multiple lines of test code.

-----------------------------------------------------

## How It Works

The core component is the class `LexicalAnalyzer`, which includes:

### 🔹 `lexer(file_path)` funtion:

- **Input**: Path to a `source_input.txt` file containing source code.
- **Output**: A list of token streams (`tokens_stream`), one per statement or line.
- **Returns**: A list of lists, where each inner list represents a stream of tokens of specific code block.
- **Prints**: Each stream of tokens that represents specific code blok on a new line for clarity.

-----------------------------------------------------

###  Token Types Identified

We have added more Keywords and Operators to deal with different test cases as it was not mentioned in the MileStone 1 Description explictly :

- **Keywords**: `if`, `else`, `then`, `while`, `for`, `return`, `void`, `break`, `continue`, `elif`, `switch`, `case`, `print`
- **Identifiers**: Variable/function names (e.g., `x`, `y`, `myFunc` as any string combination except for the keywords identified)
- **Operators**: `+`, `-`, `*`, `/`, `%`, `==`, `!=`, `=`, `>=`, `<=`, `>`, `;`, `:`, `{`, `}`, `(`, `)`, `&&`, `||`,`**`
- **Literals**: Integer constants (e.g., `5`, `10`)


-----------------------------------------------------

### Implementation Detials :

1. `TokenRule Class`
    A helper class `TokenRule` is defined to encapsulate the regular expression pattern and its corresponding token type. Each rule is compiled using Python's `re` module for efficient matching.

2. `LexicalAnalyzer Class`
    The `LexicalAnalyzer` class initializes with predefined sets of keywords and operators. It defines a list of `TokenRule` instances to match different token types:

    - ***Keywords***: Matched using word boundaries to ensure exact matches.

    - ***Identifiers***: Variable names string starting with letter(s) (may be one letter , a word)

    - ***Numbers***: Sequences of Integer digits.

    - ***Operators***: Includes both single and multi-character operators.

    - ***Whitespace***: Ignored during tokenization.

3. **Input Scanning & Tokenization (`lexer(file_path)`)**:

This method performs the following steps which included inside the `LexicalAnalyzer Class`:
 
- Opens and reads the input file line by line.

- For each line, it iterates through the characters, attempting to match the longest possible token using the defined `TokenRule` patterns.

- Upon a successful match, it appends the token to the current line's token stream.

- After processing all lines, it returns a list of token streams, each corresponding to a line in the input file.

-----------------------------------------------------


###  Test File: 

The `sample_input.txt` file contains a variety of valid test cases, including:

1. Variable assignments

2. Arithmetic operations

3. Control structures (if, else, while, for, do-while, switch-case, return, break ,.etc)

4. Function definitions

5. Return statements

6. Print statements

-----------------------------------------------------


### Example Usage: 
```python
from lexer import LexicalAnalyzer

lexicalAnalyzer = LexicalAnalyzer()
token_stream = lexicalAnalyzer.lexer('sample_input.txt')

print("Lexical Analyzer Tokens Stream:")
for stream in token_stream:
    print(stream) 
```

### Example Output:

Lexical Analyzer Tokens Stream:
['ID(x)', '=', 'NUM(5)', '+', 'NUM(2)', ';']
['ID(z)', '=', 'ID(x)', '*', '(', 'ID(y)', '-', 'NUM(3)', ')', ';']
['KW(if)', 'ID(a)', '=', 'ID(b)', 'KW(then)', 'ID(a)', '=', 'ID(a)', '+', 'NUM(1)', ';', 'KW(else)', 'ID(b)', '=', 'ID(b)', '-', 'NUM(1)', ';']
['ID(x)', '=', 'ID(ALLAM)']
['ID(ALLAM)', '=', 'NUM(1)']
['ID(p)', '=', '(', 'ID(e)', '/', 'ID(l)', ')', '+', '(', 'ID(c)', '*', 'NUM(2)', ')', '-', 'ID(z)']
['KW(if)', 'ID(a)', '>', 'ID(b)', '&&', 'ID(c)', '<=', 'ID(d)', '||', 'ID(e)', '!=', 'ID(f)', 'KW(then)', 'ID(x)', '=', 'ID(x)', '-', 'NUM(1)', ';']
['ID(result)', '=', '(', 'ID(x)', '+', 'ID(y)', ')', '*', '(', 'ID(a)', '-', 'ID(b)', ')', '/', 'NUM(5)', ';']
['ID(total)', '=', '(', '(', 'ID(x)', '+', 'ID(y)', ')', '-', '(', 'ID(a)', '*', 'ID(b)', ')', ')', '/', 'NUM(10)', ';']
['KW(do)', 'ID(x)', '=', 'ID(x)', '-', 'NUM(1)', ';', 'KW(while)', 'ID(x)', '>', 'NUM(0)', ';']
['KW(for)', 'ID(i)', '=', 'NUM(0)', ';', 'ID(i)', '<=', 'NUM(10)', ';', 'ID(i)', '=', 'ID(i)', '+', 'NUM(1)', ';']
['KW(return)', 'ID(x)', '+', 'ID(y)', '*', 'ID(z)', ';']
['KW(switch)', '(', 'ID(x)', ')', 'KW(case)', 'NUM(1)', ':', 'ID(y)', '=', 'ID(y)', '+', 'NUM(1)', ';', 'KW(case)', 'NUM(2)', ':', 'ID(z)', '=', 'ID(z)', '-', 'NUM(1)', ';']
['KW(void)', 'ID(function)', '(', ')', '{', 'KW(return)', ';', '}']
['KW(break)', ';', 'KW(continue)', ';']
['KW(if)', 'ID(x)', '>=', 'ID(y)', '&&', 'ID(z)', '!=', 'NUM(0)', 'KW(then)', 'KW(return)', 'ID(z)', ';']
['KW(if)', 'ID(x)', '==', 'ID(y)', 'KW(then)', 'KW(return)', 'ID(x)', '*', 'ID(y)', ';']
['KW(if)', 'ID(x)', '!=', 'NUM(0)', 'KW(then)', 'KW(print)', '(', 'ID(nonZeroDigit)', ')']
