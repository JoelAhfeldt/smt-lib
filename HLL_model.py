class hll_model:
    constants = []
    funs = []
    assertions = []
    constraints = []
    proofobl = []

    def __init__(self):
        self.assertions = []

    def write_constants(self, file):
        file.write("constants:\n")
        for constant in self.constants:
            file.write(constant[1]+" "+constant[0]+"\n")

    def write_declarations(self, file):
        file.write("declarations:\n")
        for assertion in self.assertions:
            file.write("bool "+assertion[0]+"\n")
        for constant in self.constants:
            file.write(constant[0]+" "+constant[1])


    def write_definitions(self, file):
        file.write("declarations:\n")
        for assertion in self.assertions:
            file.write(assertion[0]+" := " + assertion[1].print_HLL()+"\n")

    def write_constraints(self, file):
        file.write("declarations:\n")


    def write_proof_obl(self, file):
        file.write("proof obligations:\n")
        for obl in self.proofobl:
            file.write(obl.print_HLL()+"\n")


    def write_hll(self, file):
        self.write_constants(file)
        self.write_declarations(file)
        self.write_definitions(file)
        self.write_constants(file)
        self.write_proof_obl(file)



class HLL_ast:
    def __init__(self, value, node_type, children=None):
        self.value = value
        self.node_type = node_type
        if children is None:
            self.children = []
        else:
            self.children = children

    def print_HLL(self):
        if self.node_type == "op":
            if self.value in ["&", "#", "!#, +"]:
                length = len(self.children)
                list = []
                j = " "+self.value+" "
                for i in range(0, length):
                    list.append(self.children[i].value)
                text = j.join(list)
            elif self.value == "~":
                text = self.value+self.children[0].print_HLL()
            else:
                text = self.children[0].print_HLL()
                for child in self.children[1:]:
                    text = text + self.value + child.print_HLL()
            return "("+text+")"
        elif self.node_type == "var":
            return self.value
