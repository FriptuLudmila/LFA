from tokens import Token
from token_type import TokenType
import re


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.tokens = []

    def error(self):
        raise Exception('Invalid character')

    def tokenize(self):
        # Regular expressions for tokens
        token_specification = [
            (TokenType.INTEGER, r'\d+'),
            (TokenType.PLUS, r'\+'),
            (TokenType.MINUS, r'\-'),
            (TokenType.MUL, r'\*'),
            (TokenType.DIV, r'\/'),
            (TokenType.LPAREN, r'\('),
            (TokenType.RPAREN, r'\)'),
            (TokenType.EOF, r'\Z')
        ]

        # Create a regex that matches the token specifications
        token_regex = '|'.join(f'(?P<{tok.name}>{pattern})' for tok, pattern in token_specification)
        for mo in re.finditer(token_regex, self.text):
            kind = mo.lastgroup
            value = mo.group()
            tok_type = TokenType[kind]
            if tok_type == TokenType.INTEGER:
                value = int(value)  # Convert to integer
            self.tokens.append(Token(tok_type, value))

        self.tokens.append(Token(TokenType.EOF, None))
