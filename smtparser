from node import Node

class Parser:
    trees = []

    def parseSexpr(self, tokens, node):
        token = tokens.popleft()
        #print(token.content)
        if token.content != "(" and token.content != ")":
            child = Node(token.content)
            node.add_child(child)
            return tokens
        elif token.content == "(":
            child = Node()
            node.add_child(child)
            tokens = self.parse_rest_expr(tokens, child)
            return tokens

    def parse_rest_expr(self, tokens, node):
        if tokens[0].content == ")":
            token=tokens.popleft()
            #print(token.content)
            return tokens
        else:
            tokens = self.parseSexpr(tokens, node)
            tokens = self.parse_rest_expr(tokens, node)
            return tokens



    def parse(self,tokens):
        token_count = 0
        while len(tokens)>0:
            token_count = token_count + 1
            if tokens[0].content == "(":
                root = Node()
                self.parseSexpr(tokens, root)
                self.trees.append(root.children[0])
            else:
                print("expected '(' but found "+token[0].content+" at token "+token_count)
                break
