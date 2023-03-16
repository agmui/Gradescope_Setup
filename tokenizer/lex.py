from typing import NamedTuple, Type
import re
import minify


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


def back_prop(var_name, line_num):
    print("=====back prop=====")
    print('looking for:', var_name, 'line_num:', line_num)
    ex: Exp = None
    truncated_min = "\n".join(min_file_arr[:line_num])
    truncated_code = re.split('[;{}]', truncated_min)
    for l in reversed(truncated_code):  # searching through full file
        ex = eval(l, line_num, just_kind=True)  # TODO: fix line_num
        print(ex)
        if ex is None:
            continue
        if ex.type == 'NUMBER':
            break
        if (ex.type == 'ASSIGN' or ex.type == 'DEC') and ex.value == var_name:
            # if ex.type == 'ASSIGN':
            #     ex = back_prop(min_file_arr.index(l), ex.arg)
            break
    print("=====end=====")
    return ex


def eval(expression: str, line_num, just_kind: bool = False):
    name = r'[a-zA-Z_-][\w-]*'  # for names of func/var and data types
    token_specification = [
        ('NEWLINE', r'\n'),  # Line endings
        ('SKIP', r'[ \t{}]+'),  # Skip over spaces and tabs
        ('ASSIGN', fr'({name})=(.*)'),  # Assignment operator
        ('NUMBER', r'^(\d+(\.\d*)?)'),  # Integer or decimal number
        # ('END',      r';'),            # Statement terminator
        ('FUNC', r'(return) ?(.*)'),  # return
        ('CLOSURE', fr'^{name} ({name})\((.*)\)'),  # function declaration
        ('DEC', fr'(^{name} {name})'),  # declare variable
        ('FUNC', fr'({name})\((.*)\)'),  # function call
        ('VAR', fr'({name})'),  # Variable (that needs to be derived)
        # ('OP', r'[+\-*/]'),  # Arithmetic operators TODO: add comparators
        # ('MISMATCH', r'.'),  # Any other character
    ]
    print("input:", [expression])
    column = 0
    if expression == '':
        return
    for reg_try in token_specification:
        kind = reg_try[0]
        regex = reg_try[1]
        if m := re.search(regex, expression):
            if kind != "SKIP" and kind != "NEWLINE":
                print("exp:", [expression], "| groups:", m.groups(), 'kind:', kind, )
            match kind:
                case "FUNC":
                    t = Exp(kind, m[1], m.group(2), line_num, column)
                    if just_kind:
                        return t
                    if t.arg:
                        t.arg = eval(t.arg, line_num)
                    print(t)
                    return t
                case 'CLOSURE':
                    t = Exp(kind, m[1], m.group(2), line_num, column)
                    if just_kind:
                        return t
                    arg = m.group(2)
                    if arg:
                        arg = re.findall(fr'({name} {name})', m.group(2))
                        t.arg = eval(arg, line_num)
                    print(t)
                    return t
                case 'DEC':
                    t = Exp(kind, m[1], [], line_num, column)
                    if just_kind:
                        return t
                    print(t)
                    return t
                case 'VAR':
                    # t = Exp(kind, m[1], [], line_num, column)
                    t = back_prop(m[1], line_num)
                    if just_kind:
                        return t
                    print(t)
                    return t
                case 'ASSIGN':
                    t = Exp(kind, m[1], m[2], line_num, column)
                    # t.arg = back_prop(line_num-1, t.arg)
                    t.arg = eval(t.arg, line_num)
                    if just_kind:
                        return t
                    print(t)
                    return t
                case 'NUMBER':
                    t = Exp(kind, m[1], [], line_num, column)
                    if just_kind:
                        return t
                    print(t)
                    return t
                case 'NEWLINE':
                    line_num -= 1
                    continue
                case 'SKIP':
                    continue


f = open('test.c')
file = f.read()
f.close()
file_arr = file.split('\n')
min_file_arr = minify.minify_source(file_arr)
min_file = "\n".join(min_file_arr)
code = re.split('[;{}]', min_file)
# code = re.split('[;{}]', file)
print("code",code)
ans = []
for i, line in enumerate(reversed(code)):
    print("------")
    line_num = len(code) - i
    ans.append(eval(line, line_num))

print("=====")
for i in ans:
    print(i)
