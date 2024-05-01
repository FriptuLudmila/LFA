from lexer import Lexer
from parser import Parser
from ast import print_ast


text = "7 + (10 - 3) * 2"
lexer = Lexer(text)
lexer.tokenize()
parser = Parser(lexer)
ast = parser.parse()

print("Tokens:")
for token in lexer.tokens:
    print(token)

print("\nAST:")
print_ast(ast)