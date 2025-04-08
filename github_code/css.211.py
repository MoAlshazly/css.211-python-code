# A lexical analyzer system for simple arithmetic expressions in Python
import sys
import string

# Global declarations
# Variables
char_class = None  # Stores the character class of the current character
lexeme = ""      # Stores the characters of the current token (lexeme)
next_char = None  # Stores the next character from the input
lex_len = 0      # Stores the length of the current lexeme
token = None       # Stores the token code (not currently used)
next_token = None  # Stores the token code of the next token
input_string = ""  # Stores the input string directly

# Character classes
LETTER = 0
DIGIT = 1
UNKNOWN = 99

# Token codes
INT_LIT = 10
IDENT = 11
ASSIGN_OP = 20  # Not used in this simple example
ADD_OP = 21
SUB_OP = 22
MULT_OP = 23
DIV_OP = 24
LEFT_PAREN = 25
RIGHT_PAREN = 26
EOF = -1  # End of file marker

# Index to keep track of the current position in the input string
input_index = 0

# Function to add next_char to lexeme
def add_char():
    global lexeme, next_char, lex_len
    if lex_len <= 98:
        lexeme += next_char  # Append the character to the lexeme string
        lex_len += 1
    else:
        print("Error - lexeme is too long")

# Function to get the next character of input and determine its character class
def get_char():
    global next_char, char_class, input_string, input_index
    if input_index < len(input_string):
        next_char = input_string[input_index]
        input_index += 1
        if next_char.isalpha():
            char_class = LETTER
        elif next_char.isdigit():
            char_class = DIGIT
        else:
            char_class = UNKNOWN
    else:
        next_char = None
        char_class = EOF  # End of file

# Function to call get_char until it returns a non-whitespace character
def get_non_blank():
    global next_char
    while next_char is not None and next_char.isspace():
        get_char()

# lookup - a function to lookup operators and parentheses and return the token
def lookup(char):
    global next_token, lexeme
    if char == '(':
        add_char()
        next_token = LEFT_PAREN
    elif char == ')':
        add_char()
        next_token = RIGHT_PAREN
    elif char == '+':
        add_char()
        next_token = ADD_OP
    elif char == '-':
        add_char()
        next_token = SUB_OP
    elif char == '*':
        add_char()
        next_token = MULT_OP
    elif char == '/':
        add_char()
        next_token = DIV_OP
    else:
        add_char()
        next_token = EOF  # If an unknown character, treat as end of file (error condition for simple example)
    return next_token

# lex - a simple lexical analyzer for arithmetic expressions
def lex():
    global lexeme, lex_len, next_token, char_class
    lex_len = 0      # Reset lexeme length
    lexeme = ""      # Reset the lexeme string
    get_non_blank()  # Skip leading whitespace

    if char_class == LETTER:
        add_char()  # Add the first letter to the lexeme
        get_char()  # Get the next character
        while char_class == LETTER or char_class == DIGIT:  # Continue reading letters/digits
            add_char()
            get_char()
        next_token = IDENT  # Assign the IDENT token code
    elif char_class == DIGIT:
        add_char()  # Add the first digit to the lexeme
        get_char()  # Get the next character
        while char_class == DIGIT:  # Continue reading digits
            add_char()
            get_char()
        next_token = INT_LIT  # Assign the INT_LIT token code
    elif char_class == UNKNOWN:
        if next_char is not None:
            lookup(next_char)  # Lookup the operator/parenthesis
            get_char()  # Get the next character
        else:
            next_token = EOF
            lexeme = "EOF"
    elif char_class == EOF:
        next_token = EOF
        lexeme = "EOF"
    else:
        next_token = EOF
        lexeme = ""

    print(f"Next token is: {next_token}, Next lexeme is {lexeme}")
    return next_token

# main driver
if __name__ == "__main__":
    # You can directly define the input string here in Colab
    input_string = "(12 + var1) * 5 - 3 / abc"

    # Initialize the input string and get the first character
    input_index = 0
    get_char()

    while next_token != EOF:
        lex()  # Perform lexical analysis

    print("\nLexical analysis complete.")