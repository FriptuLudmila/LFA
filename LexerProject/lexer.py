import re

TOKEN_TYPES = [
    ('FLOAT', r'\d+\.\d+'),
    ('INTEGER', r'\d+'),
    ('STRING', r'"[^"]*"|\'[^\']*\''),
    ('COMMENT', r'//.*|/\*[\s\S]*?\*/'),
    ('OPERATOR', r'[\+\-\*/=<>!]=?|&&|\|\|'),
    ('IDENTIFIER', r'[a-zA-Z_]\w*'),
    ('BRACE', r'[\{\}\(\)\[\]]'),
    ('PUNCTUATION', r'[;:,\.]'),
    ('WHITESPACE', r'\s+'),
    ('UNKNOWN', r'.')
]


class Lexer:
    def __init__(self, text):
        self.text = text
        self.tokens = []

    def tokenize(self):
        while self.text:
            for token_type, pattern in TOKEN_TYPES:
                regex = re.compile(pattern)
                match = regex.match(self.text)
                if match:
                    value = match.group(0)
                    if token_type != 'WHITESPACE' and token_type != 'COMMENT':  # Ignore whitespace and comments
                        self.tokens.append((token_type, value))
                    self.text = self.text[len(value):]
                    break
            else:
                raise Exception('LexerError: Unknown token')

        return self.tokens


# Example
code = """
// This is a comment
x = 100 + 20.5
y = "Hello, world!"
if (x > 100) { y = "Large"; }
"""
lexer = Lexer(code)
tokens = lexer.tokenize()
print(tokens)
