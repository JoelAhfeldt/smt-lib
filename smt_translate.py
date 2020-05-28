from smtliblexer import Lexer
from smtParser import Parser

def main():
    lexer = Lexer()
    reg = lexer.create_reg()
    f = open("test.txt")
    text = f.read()
    tokens = lexer.lex(text, reg)
    parser = Parser()
    parser.parse(tokens)
    for tree in parser.trees:
        tree.print_tree()

main()
