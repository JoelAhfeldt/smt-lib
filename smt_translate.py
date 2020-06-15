from smtliblexer import Lexer
from smtParser import Parser

class Translator:
    binop = ["+", "-", "*", "/", "="]

    def translate_tree(self, tree):
        if tree.children.has_children:
            if tree.children[0].has_children:
                self.translate_node(tree)
        for node in tree.children:
            self.translate_tree(node)


    def translate_node(self, node):
        result = ""
        if node.children[0] in self.binop:
            result = self.translate_binop(node)
        elif node.children[0] in self.binop:
            result = self.translate_binop(node)




    def translate_binop(self, node):
        length = len(node.children)
        if length >= 3:
            list = []
            for i in range(1, length):
                list.append(node.children[i].data)
            operator = node.children[0].data
            return operator.join(list)
        else:
            return node.children[1].data + " " + node.children[0].data + " " + node.children[2].data

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
