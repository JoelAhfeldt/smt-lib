import re
from collections import deque


class Token:

    def __init__(self, content, type=None):
        self.type = type
        self.content = content

    def __str__(self):
        string = "content: "+self.content+" type: "+self.type
        return string



class Lexer:
    reserved_words_g = r"\! _ | as BINARY DECIMAL exists HEXADECIMAL forall let match NUMERAL]"

    reserved_words_c = ["assert", "check-sat", "check-sat-assuming", "declare-const", "declare-datatype",
                        "declare-datatypes", "declare-fun", "declare-sort", "define-fun", "define-fun-rec", "define-sort",
                        "echo", "exit", "get-assertions" "get-assignment", "get-info", "get-model", "get-option",
                        "get-proof", "get-unsat-assumptions", "get-unsat-core", "get-value","pop", "push", "reset",
                        "reset-assertions", "set-info", "set-logic", "set-option"]
    simplesymb = r"[a-zA-Z~!@$%^&*_+=<>.?/-][0-9a-zA-Z~!@$%^&*_+=<>.?/-]*"<,
    tokentype = {"<decimal>": r"(([1-9][0-9]*)\.([0-9]+))",
                 "<numeral>": r"0|([1-9][0-9]*)",
                 "<hexadecimal>": r"#x[0-9a-fA-F]+",
                 "<binary>": r"#b[01]+",
                 "<string>": r"\".*\"",
                 "<space>": r"\s+",
                 "<symbol>": simplesymb,
                 "<keyword>": r":"+simplesymb,
                 "<parenthesis>": r"\(|\)",
                 "<comment>": r";.*"}


    def create_reg(self):
        reg = r""
        for i in self.tokentype.keys():
            reg = reg + r"(?P" + i +self.tokentype.get(i)+r")|"
            #print(reg)
        reg = re.compile(reg)
        return reg

    def lex(self, text, reg):
        index = 0
        tokens = deque()
        while index < len(text):
            match = reg.match(text, index)
            index = match.end()
            if match.lastgroup is None:
                print("Ingen matchning hittades på plats "+str(index)+", tecken: "+text[index])
                break
            if match.lastgroup != "space" and match.lastgroup != "comment":
                token = Token(match.group(), match.lastgroup)
                #print(token)
                tokens.append(token)
        return tokens
