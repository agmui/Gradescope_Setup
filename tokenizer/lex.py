from typing import NamedTuple, Type
import re, os
import minify


class Exp:
    def __init__(self, type, value, arg, line, column):
        self.type: str = type
        self.value: any = value
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
        ex = eval(l, line_num)  # TODO: fix line_num
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


def eval(expression: str, line_num: int, just_kind: bool = False) -> Exp:
    name = r'[a-zA-Z_-][\w-]*'  # for names of func/var and data types
    token_specification = [
        ('NEWLINE', r'\n'),  # Line endings
        ('SKIP', r'[ \t{}]+'),  # Skip over spaces and tabs
        ('ASSIGN', fr'({name})=(.*)'),  # Assignment operator
        ('NUMBER', r'^(\d+(\.\d*)?)'),  # Integer or decimal number
        # ('BOOL', r'^(true|false)'),  # bool
        # ('END',      r';'),            # Statement terminator
        ('FUNC', r'(return) ?(.*)'),  # return
        ('CLOSURE', fr'{name} ({name})\((.*)\)'),  # function declaration TODO: add if, for, and while loop
        ('CLOSURE', fr'(if|for|while)\((.*)\)'),  # function declaration TODO: add if, for, and while loop
        ('DEC', fr'(^{name} {name})'),  # declare variable
        ('FUNC', fr'({name})\((.*)\)'),  # function call
        ('VAR', fr'({name})'),  # Variable (that needs to be derived)
        # ('OP', r'[+\-*/]'),  # Arithmetic operators TODO: add comparators
        ('MISMATCH', r'.'),  # Any other character
    ]
    line_start = 0
    print("input:", [expression])
    if expression == '':
        return None
    for tokens in token_specification:
        kind = tokens[0]
        regex = tokens[1]
        arg: any = None
        if m := re.search(regex, expression):
            column = m.start() - line_start
            value: any = None
            if kind != "SKIP" and kind != "NEWLINE":
                print("exp:", [expression], "| groups:", m.groups(), 'kind:', kind, )
                value: any = m[1]  # TODO move
            match kind:
                case "FUNC":
                    arg = m.group(2)
                    if not just_kind and arg:
                        arg = eval(arg, line_num)
                case 'CLOSURE':
                    arg = m.group(2)
                    if not just_kind and arg:
                        # TODO: handle arg conditions for loops and ifs
                        args = re.findall(fr'({name} {name})', m.group(2))
                        arr = []
                        for i in args:  # evaluate each argument individually
                            arr.append(eval(i, line_num))
                        arg = arr
                # case 'DEC':
                #     value = m[1]
                #     if just_kind:
                #         return t
                #     print(t)
                #     return t
                case 'VAR':
                    if value in keywords:
                        break
                    t = back_prop(m[1], line_num)
                    return t
                case 'ASSIGN':
                    arg = m[2]
                    if not just_kind:
                        arg = eval(arg, line_num)
                case 'NUMBER':
                    value = float(value) if '.' in value else int(value)
                case 'BOOL':
                    value = "true" == value
                case 'NEWLINE':
                    line_num -= 1
                    line_start = m.end()
                    continue
                case 'SKIP':
                    continue
                case 'MISMATCH':
                    raise RuntimeError(f'{value!r} unexpected on line {line_num}')
            t = Exp(kind, value, arg, line_num, column)
            print(t)
            return t


# os.system("gcc test.c")
f = open('test.c')
file = f.read()
f.close()
file_arr = file.split('\n')
min_file_arr = minify.minify_source(file_arr)
min_file = "\n".join(min_file_arr)
code = re.split('[;{}]', min_file)
# code = re.split('[;{}]', file)
print("code", code)
ans = []
for i, line in enumerate(reversed(code)):
    print("------")
    line_num = len(code) - i
    ans.append(eval(line, line_num))

print("=====")
for i in ans:
    print(i)
