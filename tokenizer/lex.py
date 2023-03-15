from typing import NamedTuple, Type
import re


class Exp:
    def __init__(self, type, value, arg, line, column):
        self.type: str = type
        self.value: str = value
        self.arg: list = arg
        self.line: int = line
        self.column: int = column

    def __repr__(self):
        return f'{self.type}({self.value}{(" | " + str(self.arg)) if self.arg else ""})'

    def __str__(self):
        return f'{self.type}({self.value}{(" | " + str(self.arg)) if self.arg else ""})'


keywords = {
    'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum', 'extern',
    'float', 'for', 'goto', 'if', 'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static',
    'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while'
}


def back_prop(line_num):
    print("=====back prop=====")
    for line in reversed(file_arr[:line_num]):
        line = re.split('[;{}]', line)
        print(line)
        l = eval(line, line_num)[0]
        if l.type == 'ASSIGN' or l.type == 'DEC':
            break
    print("=====back prop=====")
    return l


def eval(code_arr: list, line_num):
    name = r'[a-zA-Z_-][\w-]*'  # for names of func/var and data types
    token_specification = [
        ('NEWLINE', r'\n'),  # Line endings
        ('SKIP', r'[ \t{}]+'),  # Skip over spaces and tabs
        ('ASSIGN', fr'({name})=(.*)'),  # Assignment operator
        # ('END',      r';'),            # Statement terminator
        ('FUNC', r'(return) ?(.*)'),  # return
        ('CLOSURE', fr'^{name} ({name})\((.*)\)'),  # function declaration
        ('DEC', fr'(^{name} {name})'),  # declare variable
        ('FUNC', fr'({name})\((.*)\)'),  # function call
        ('VAR', fr'({name})'),  # Variable (that needs to be derived)
        ('NUMBER', r'(\d+(\.\d*)?)'),  # Integer or decimal number
        # ('OP', r'[+\-*/]'),  # Arithmetic operators TODO: add comparators
        # ('MISMATCH', r'.'),  # Any other character
    ]
    ans = []
    print("input:", code_arr)
    for line in reversed(code_arr):
        if line == '':
            continue
        for reg_try in token_specification:
            kind = reg_try[0]
            regex = reg_try[1]
            if m := re.search(regex, line):
                print("group:", m.groups(), 'kind:', kind, "line:", [line])
                column = 0
                match kind:
                    case "FUNC":
                        t = Exp(kind, m[1], m.group(2), line_num, column)
                        if t.arg:
                            t.arg = eval([t.arg], line_num)
                        print(t)
                        ans.append(t)
                        break
                    case 'CLOSURE':
                        t = Exp(kind, m[1], m.group(2), line_num, column)
                        arg = m.group(2)
                        if arg:
                            arg = re.findall(fr'({name} {name})', m.group(2))
                            t.arg = eval(arg, line_num)
                        print(t)
                        ans.append(t)
                        break
                    case 'DEC':
                        print(Exp(kind, m[1], [], line_num, column))
                        ans.append(Exp(kind, m[1], [], line_num, column))
                        break
                    case 'VAR':
                        # t = Exp(kind, m[1], [], line_num, column)
                        t = back_prop(line_num)
                        print(t)
                        ans.append(t)
                        break
                    case 'ASSIGN':
                        t = Exp(kind, m[1], m[2], line_num, column)
                        print(t)
                        ans.append(t)
                        break
                    case 'NUMBER':
                        ans.append(int(m[1]))
                        break
                    case 'NEWLINE':
                        line_num -= 1
                        continue
                    case 'SKIP':
                        continue

    return ans


f = open('test.c')
file = f.read()
f.close()
file_arr = file.split('\n')
# for token in tokenize(file):
#     print(token)
code = re.split('[;{}]', file)
ans = eval(code, len(file_arr) - 1)
print("====================")
for i in ans:
    print(i)
