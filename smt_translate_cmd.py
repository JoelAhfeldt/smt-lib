from collections import ChainMap
import re


class Translator:
    # things to translate
    binop_int = ["+", "-", "*", "/", "=", ">", "<", "<=", ">="]
    boolean = ["true", "false"]
    binop_bool = ["and", "or", "xor"]
    divisble = re.compile(r"divisible_(?P<number>\d+")

    assert_names = {}

    #get assert name from dictionary
    def get_new_assert_name(self, assert_lvl):
        assert_lvl = "_".join(assert_lvl)
        if assert_lvl in self.assert_names:
            self.assert_names[assert_lvl] += 1
            return "assertion_"+assert_lvl+"_"+self.assert_names[assert_lvl]
        else:
            self.assert_names[assert_lvl] = 1
            return "assertion_"+assert_lvl+"_"+"1"

    #get all assertions on the current lvl
    def get_assertions(self, assert_lvl):
        assertions = []
        length = len(assert_lvl)
        for i in range(0, length):
            assert_lvl = "_".join(assert_lvl[0:i])
            assert_nr = self.assert_names[assert_lvl]
            for j in range(0, assert_nr):
                assertions.append(assertion_+assert_lvl+"_"+j)


    """
    Translating functions:
    ______________________
    """

    def translate_assert(self, cmd, name=None):
        if len(cmd.children) == 2:
            translation = self._translate_tree(cmd.child[1])
            if name is None:
                return translation
            else:
                return [name, translation]

    # recursively traverses assertion tree and returns HLL formula
    def _translate_tree(self, tree):
        if tree.has_children():
            length = len(tree.children)
            for i in range(1, length, 1):
                node = tree.children[-i]
                if node.has_children():
                    self._translate_tree(node)
        self.translate_node(tree)
        data = tree.data[1,len(tree.data)]
        return data

    # checks what kind of formula and translates it
    def translate_node(self, node):
        data = node.children[0].data

        if data in self.binop_int:
            self.translate_binop_int(node)

        elif data == "ite":
            node.data = "if " + node.children[1].data + \
                        " then " + node.children[2].data + \
                        " else " + node.children[3].data

        elif data in self.boolean:
            node.data = data

        elif data in self.binop_bool:
            self.translate_binop_bool(node)

        elif data == "not":
            node.data = "~" + node.children[1].data

        # checks if data matches regular expression
        elif self.divisible.match(data):
            match = self.divisible.match(data)

            # divisible if remainder is 0
            node.data = node.children[1].data + " % " + match.group("number") + " = 0"
        node.data = "(" + node.data + ")"

    def translate_binop_bool(self, node):
        if node.children[0].data == "and":
            operation = " & "
        elif node.children[0].data == "or":
            operation = " # "
        elif node.children[0].data == "xor":
            operation = " #! "
        length = len(node.children)
        list = []
        for i in range(1, length):
            list.append(node.children[i].data)
        node.data = operation.join(list)

    def translate_binop_int(self, node):
        length = len(node.children)
        list = []
        for i in range(1, length):
            list.append(node.children[i].data)
        operator = node.children[0].data
        node.data = operator.join(list)


    #Main translation loop, traverses and translates all commands

    def cmd_transl(self, commands, hll_model, assert_lvl=None, prev_def_asserts=None):
        # Keep track of if this is the top-level call

        initial_call = prev_def_asserts is None

        # Add local set of assert names

        local_asserts = set()

        # keeps track of the number of push commands at this level
        push_nr = 0

        # Set up the ChainMap 'defined_asserts' containing the full current set of assert names

        if initial_call:

            # defined_asserts = ChainMap(local_asserts)
            # Sets the next assert name
            assert_lvl = []


        else:

        # defined_asserts = defined_asserts.new_child(local_asserts)

        # Main command loop

        while True:

            cmd = pop_next_command(commands)

            if is_assert(cmd):

                if initial_call:
                    translation = self.translate_assert(cmd)
                    # add translation as a constraint

                    .

                    .

                    else:

                    # Get and register new assert_name

                    assert_name = self.get_new_assert_name(assert_lvl)

                    #local_asserts.add(assert_name)

                    translation = self.translate_assert(cmd, assert_name)

                    hll_model.assertions.append(translation)

                    # Add the assert to 'hll_model' as a definition

                    # (of the variable named by 'assert_name')...

                    .

                    .

                elif is_check_sat(cmd):

                    # Get all relevant assert names in sorted order

                    relevant_asserts = sorted(defined_asserts)

                    # Add the proof obligation “not (rel_ass_1 and rel_ass_2 and...and rel_ass_n)”

                    # to 'hll_model’

                    .

                    .

                    # Continue with other commands

                    .

                    .

                    elif is_exit(cmd):
                    return



                elif is_pop(cmd):

                    if initial_call:
                        error()  # Should be 'exit' and not 'pop'

                    return

                elif is_push(cmd):
                    push_nr = + 1
                    assert_lvl.append(push_nr)

                    self.cmd_transl(commands, hll_model, assert_lvl  # defined_asserts)

def is_assert(cmd):
    if cmd.children[0].data == "assert":
        return True
    else:
        return False

def is_pop(cmd):
    if cmd.children[0].data == "pop":
        return True
    else:
        return False

def is_push(cmd):
    if cmd.children[0].data == "push":
        return True
    else:
        return False

def is_check_sat(cmd):
    if cmd.children[0].data == "check sat":
        return True
    else:
        return False
