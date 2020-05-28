class Node:
    def __init__(self, data=None):
        self.data = data
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

    def print_tree(self):
        text=""
        text=self.print_tree_rec(text)
        print(text)

    def print_tree_rec(self,text):
        if len(self.children) == 0:
            text = text + self.data + " "
        else:
            text = text + "("
            for child in self.children:
                text = child.print_tree_rec(text)
            text = text + ")"
        return text

    def check_tree(self, functions, fix):
        if len(self.children) != 0:
            if self.children(0) in functions:
                fix.append(self)
            else:
                for node in self.children:
                    check_tree(node, functions)

    def fix_chainable(self):
        leng = len(self.children)
        for i in range(1, leng - 1):
            new_children = [self.children[0], self.children[i], self.children[i + 1]]
            self.children[i] = Node()
            self.children[i].children = new_children
        self.children[0] = Node("and")
        self.children.remove(self.children[leng-1])
        if len(self.children) > 3:
            self.fix_chainable()
