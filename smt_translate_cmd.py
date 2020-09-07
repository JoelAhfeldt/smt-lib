from smtliblexer import Lexer
from smtParser import Parser
import re
from HLL_model import HLL_ast, hll_model


class Translator:
    # things to translate
    binop_int = ["+", "-", "*", "/", "=", ">", "<", "<=", ">="]
    boolean = ["true", "false"]
    binop_bool = ["and", "or", "xor"]
    divisible = re.compile(r"divisible_(?P<number>\d+)")

    assert_names = {}

    # get assert name from dictionary
    def get_new_assert_name(self, assert_lvl):
        assert_key = "_".join(assert_lvl)
        if assert_key in self.assert_names:
            self.assert_names[assert_key] += 1
            if assert_key == "":
                return "assertion_"+ str(self.assert_names[assert_key])
            else:
                return "assertion_" + assert_key + "_" + str(self.assert_names[assert_key])
        else:
            self.assert_names[assert_key] = 1
            if assert_key == "":
                return "assertion_1"
            else:
                return "assertion_" + assert_key + "_" + "1"

    # get all assertions on the current lvl
    def get_assertions(self, assert_lvl):
        assertions = []
        length = len(assert_lvl)
        for i in range(length+1):
            assert_key = "_".join(assert_lvl[0:i])
            if assert_key in self.assert_names:
                assert_nr = self.assert_names[assert_key]
                for j in range(1, assert_nr+1):
                    if assert_key == "":
                        assertions.append("assertion_"+str(j))
                    else:
                        assertions.append("assertion_" + assert_key + "_" + str(j))
        return assertions

    """
      Translating functions:
      ______________________
    """
    def translate_fun(self, cmd):
        # translate type of all variables
        trans_type = [self.translate_type(t.children[1].data) for t in cmd.children[2].children]
        var = [t.children[0].data for t in cmd.children[2].children]
        # translate fun definition
        fun_def = self.translate_tree(cmd.children[4])
        return [self.translate_type(cmd.children[3].data), cmd.children[1].data, trans_type, var, fun_def]

    def translate_const(self, cmd):
        if len(cmd.children) == 4:
            # check that its a constant function
            if len(cmd.children[2].children) == 0:
                return [self.translate_type(cmd.children[3].data), cmd.children[1].data]
        if len(cmd.children) == 3:
            return [self.translate_type(cmd.children[2].data), cmd.children[1].data]



    def translate_type(self, type):
        if type in ["int", "bool"]:
            return type
        else:
            return "float"

    def translate_assert(self, cmd, name=None):
        if len(cmd.children) == 2:
            translation = self.translate_tree(cmd.children[1])
            if name is None:
                return translation
            else:
                return [name, translation]

    # recursively traverses assertion tree and returns HLL formula
    def translate_tree(self, tree):
        if tree.has_children():
            # check if its a quant expr
            if tree.children[0].data in ["forall", "exist"]:
                quantvar = [self.translate_quantvar(c) for c in tree.children[1].children]
                expr = self.translate_tree(tree.children[2])
                return self.translate_quant(tree.children[0], quantvar, expr)
            else:
                # translate children
                trans_children = [self.translate_tree(c) for c in tree.children[1:]]
                op = tree.children[0].data  # Assuming operator in first element
                return self.translate_op(op, trans_children)

        else:
            return self.translate_node(tree)

    # checks what kind of formula and translates it
    def translate_op(self, op, children):
        if op == "+":
            return HLL_ast("+", "op", children)
        elif op == "-":
            return HLL_ast("-", "op", children)
        elif op == "*":
            return HLL_ast("*", "op", children)
        elif op == "/":
            return HLL_ast("/", "op", children)

        elif op == "=":
            return HLL_ast("=", "op", children)
        elif op == "<":
            return HLL_ast("<", "op", children)
        elif op == ">":
            return HLL_ast(">", "op", children)
        elif op == "<=":
            return HLL_ast("<=", "op", children)
        elif op == ">=":
            return HLL_ast(">=", "op", children)

        elif op == "not":
            return HLL_ast("~", "op", children)
        elif op == "and":
            return HLL_ast("&", "op", children)
        elif op == "or":
            return HLL_ast("#", "op", children)
        elif op == "xor":
            return HLL_ast("#!", "op", children)

        # floating point operators:
        elif op == "fb.abs":
            return HLL_ast("fb_abs", "op", children)
        elif op == "fb.neg":
            return HLL_ast("fb_neg", "op", children)
        elif op == "fb.add":
            return HLL_ast("fb_add", "op", children)
        elif op == "fb.sub":
            return HLL_ast("fb_sub", "op", children)
        elif op == "fb.mul":
            return HLL_ast("fb_mul", "op", children)
        elif op == "fb.div":
            return HLL_ast("fb_div", "op", children)
        elif op == "fb.fma":
            return HLL_ast("fb_fma", "op", children)
        elif op == "fb.sqrt":
            return HLL_ast("fb_sqrt", "op", children)
        elif op == "fb.rem":
            return HLL_ast("fb_rem", "op", children)
        elif op == "fb.roundToIntegral":
            return HLL_ast("fb_rti", "op", children)
        elif op == "fb.min":
            return HLL_ast("fb_min", "op", children)
        elif op == "fb.max":
            return HLL_ast("fb_max", "op", children)

        elif op == "fb.leq":
            return HLL_ast("fb_leq", "op", children)
        elif op == "fb.lt":
            return HLL_ast("fb_lt", "op", children)
        elif op == "fb.geq":
            return HLL_ast("fb_geq", "op", children)
        elif op == "fb.gt":
            return HLL_ast("fb_gt", "op", children)
        elif op == "fb.eq":
            return HLL_ast("fb_eq", "op", children)

        elif op == "fb.isNormal":
            return HLL_ast("fb_isNormal", "op", children)
        elif op == "fb.isSubnormal":
            return HLL_ast("fb_isSubnormal", "op", children)
        elif op == "fb.isZero":
            return HLL_ast("fb_isZero", "op", children)
        elif op == "fb.isInfinite":
            return HLL_ast("fb_isInfinite", "op", children)
        elif op == "fb.isNaN":
            return HLL_ast("fb_isNan", "op", children)
        elif op == "fb.isPositive":
            return HLL_ast("fb_isPositive", "op", children)
        elif op == "fb.isNegative":
            return HLL_ast("fb_isNegative", "op", children)

        elif self.divisible.match(op):  # rewrite formula as a % n = 0
            child_n = HLL_ast(match.group("number"), "var")
            div = HLL_ast("%", "op", children.append(child_n))
            child_0 = HLL_ast("0", "var")
            return HLL_ast("=", [div, child_0])

    def translate_node(self, node):
        return HLL_ast(node.data, "var")

    def translate_quant(self, quant, var, expr):
        if quant == "forall":
            return HLL_ast("ALL", "quant", [var, expr])
        elif quant == "exist":
            return HLL_ast("SOME", "quant", [var, expr])

    def translate_quantvar(self,var):
        if var[1] == "int":
            return var[0]+":[-10000,10000]"
        if var[1] == "bool":
            return var[0]+":[true,false]"


    def cmd_transl(self, commands, hll_model, assert_lvl=None):
        # Keep track of if this is the top-level call

        initial_call = assert_lvl is None

        # Add local set of assert names

        local_asserts = set()

        # keeps track of the number of push commands at this level
        push_nr = 0

        if initial_call:
            # Sets the next assert name
            assert_lvl = []

        # Main command loop

        while True:

            cmd = pop_next_command(commands)

            if is_assert(cmd):
                # Get and register new assert_name

                assert_name = self.get_new_assert_name(assert_lvl)

                translation = self.translate_assert(cmd, assert_name)

                hll_model.assertions.append(translation)

                # Add the assert to 'hll_model' as a definition

                # (of the variable named by 'assert_name')...

            elif is_check_sat(cmd):

                    # Get all relevant assert names in sorted order
                    relevant_asserts = self.get_assertions(assert_lvl)

                    children = [HLL_ast(rel_assert, "var") for rel_assert in relevant_asserts]

                    hll_model.proofobl.append(HLL_ast("~", "op", [HLL_ast("&", "op", children)]))

                    # Add the proof obligation “not (rel_ass_1 and rel_ass_2 and...and rel_ass_n)”

                    # to 'hll_model’

                    # Continue with other commands

            elif is_declare_fun(cmd):
                translation = self.translate_const(cmd)
                hll_model.constants.append(translation)
                return

            elif is_define_fun(cmd):
                translation = self.translate_fun(cmd)
                hll_model.funs.append(translation)

            elif is_declare_const(cmd):
                translation = self.translate_const(cmd)
                hll_model.constants.append(translation)



            elif is_exit(cmd):
                return

            elif is_pop(cmd):

                if initial_call:
                    error()  # Should be 'exit' and not 'pop'

                return

            elif is_push(cmd):
                push_nr = push_nr + 1
                new_assert_lvl = assert_lvl.copy()
                new_assert_lvl.append(str(push_nr))

                self.cmd_transl(commands, hll_model, new_assert_lvl)

            else:
                print(cmd.children[0].data+" is currently not a supported command")


def parse():
    lexer = Lexer()
    reg = lexer.create_reg()
    f = open("test.txt")
    text = f.read()

    tokens = lexer.lex(text, reg)
    parser = Parser()

    trees = parser.parse(tokens)
    translate = Translator()
    hll = hll_model()
    translate.cmd_transl(trees, hll)
    file = open("model.hll", "w")
    hll.write_hll(file)

    '''
    print(hll.constraints[0].print_HLL())
    for asserts in hll.assertions:
        print(asserts[0])
        print(asserts[1].print_HLL())
    for obl in hll.proofobl:
        print(obl.print_HLL())
    '''

# Main translation loop, traverses and translates all commands
#'''

#'''

def is_define_sort(cmd):
    if cmd.children[0].data == "define-sort":
        return True
    else:
        return False


def is_define_funs_rec(cmd):
    if cmd.children[0].data == "define-funs-rec":
        return True
    else:
        return False


def is_define_fun_rec(cmd):
    if cmd.children[0].data == "define-fun-rec":
        return True
    else:
        return False


def is_define_fun(cmd):
    if cmd.children[0].data == "define-fun":
        return True
    else:
        return False


def is_declare_sort(cmd):
    if cmd.children[0].data == "declare-sort":
        return True
    else:
        return False


def is_declare_fun(cmd):
    if cmd.children[0].data == "declare-fun":
        return True
    else:
        return False


def is_declare_datatypes(cmd):
    if cmd.children[0].data == "declare-datatypes":
        return True
    else:
        return False

def is_declare_datatype(cmd):
    if cmd.children[0].data == "declare-datatype":
        return True
    else:
        return False


def is_declare_const(cmd):
    if cmd.children[0].data == "declare-const":
        return True
    else:
        return False


def is_assert(cmd):
    if cmd.children[0].data == "assert":
        return True
    else:
        return False


def is_exit(cmd):
    if cmd.children[0].data == "exit":
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
    if cmd.children[0].data == "check-sat":
        return True
    else:
        return False


def pop_next_command(commands):
    command = commands[0]
    commands.pop(0)
    return command


parse()
