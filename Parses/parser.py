from token_type import *
from tokens import *
from ast import *

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.current_token = None
        self.pos = -1
        self.advance()

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = Token(TokenType.EOF, None)

    def error(self):
        raise Exception('Invalid syntax')

    def parse(self):
        return self.expression()

    def expression(self):
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current_token
            self.advance()
            node = BinOp(left=node, op=op, right=self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            op = self.current_token
            self.advance()
            node = BinOp(left=node, op=op, right=self.factor())
        return node

    def factor(self):
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.advance()
            return Num(token)
        elif token.type == TokenType.LPAREN:
            self.advance()
            node = self.expression()
            if self.current_token.type != TokenType.RPAREN:
                self.error()
            self.advance()
            return node
        else:
            self.error()
