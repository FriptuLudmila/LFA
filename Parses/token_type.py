from enum import Enum


# Define token types using Enum
class TokenType(Enum):
    INTEGER = 'INTEGER'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MUL = 'MUL'
    DIV = 'DIV'
    LPAREN = 'LPAREN'  # (
    RPAREN = 'RPAREN'  # )
    EOF = 'EOF'