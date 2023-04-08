from typing import NamedTuple, Type
import re, os
import minify


# TODO: add fuzziness

class Exp:
    g_tab = 0

    def __init__(self, type, value, arg, line, column):
        self.type: str = type
        self.value: any = value
        self.arg: list = arg
        self.line: int = line  # FIXME: line nums are wrong because minify removes all newlines
        self.column: int = column

    def format_closure(self, tab_num):
        if self.type == 'CURL':
            if self.value == '{':
                Exp.g_tab += 1
            if self.value == '}':
                Exp.g_tab -= 1
            return ''
        if self.type == 'CLOSURE' and self.value != 'if':
            s = f'{self.type}({self.value} :\n'
            for i in self.arg:
                if i is not None:
                    s += '\t' * (Exp.g_tab + tab_num + 1) + i.format_closure(tab_num + 1) + '\n'
            return s + '\t' * tab_num + ')'
        else:
            return f'{self.type}({self.value}{(" | " + str(self.arg)) if self.arg else ""})'

    def __repr__(self):
        return self.format_closure(0)

    def __str__(self):
        return self.format_closure(0)


name = r'[a-zA-Z_-][\w-]*'  # for names of func/var and data types
keywords = {
    'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum', 'extern',
    'float', 'for', 'goto', 'if', 'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static',
    'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while'
}

func_declarations: dict[str, list[int, int]] = {}


def back_prop(var_name, line_num):
    print("=====back prop=====")
    print('looking for:', var_name, 'line_num:', line_num)
    ex: Exp = None
    truncated_min = "\n".join(min_file_arr[:line_num])
    truncated_code = re.split('[;{}]', truncated_min)
    for l in reversed(truncated_code):  # searching through full file
        print("testing:", [l])
        ex = eval(l, line_num)  # TODO: fix line_num
        # print(ex)
        if ex is None:
            continue
        if ex.type == 'NUMBER':
            break
        if ex.type == 'ASSIGN' and ex.value == var_name:
            # if ex.type == 'ASSIGN':
            #     ex = back_prop(min_file_arr.index(l), ex.arg)
            break
        if ex.type == 'FUNC_DEC':
            for i in ex.arg:
                if i.arg == var_name:
                    print("=====end=====")
                    return i
    print("=====end=====")
    return ex


def eval(expression: str, line_num: int, just_kind: bool = False, suppress=False) -> Exp:
    token_specification = [
        ('NEWLINE', r'\n'),  # Line endings
        ('SKIP', r'([ \t{}]+)'),  # Skip over spaces and tabs
        ('CLOSURE', fr'^(if|for|while)\((.*)\)'),  # if and loops
        ('OP', r'([\w-])([><]=?|==)([\w-])'),  # comparators
        ('ASSIGN', fr'({name})=(.*)'),  # Assignment operator
        ('OP', r'([\w+-])([+\-*/])([\w+-])'),  # Arithmetic operators
        # ('BOOL', r'^(true|false)'),  # bool
        ('FUNC', r'(return) ?(.*)'),  # return
        ('FUNC_DEC', fr'{name} ({name})\((.*)\)'),  # function declaration
        ('DEC', fr'(^{name}) ({name})'),  # declare variable
        ('FUNC', fr'({name})\((.*)\)'),  # function call
        ('VAR', fr'({name})'),  # Variable (that needs to be derived)
        ('CURL', r'([\{\}])'),  # FIXME:
        ('NUM', r'^(\d+(\.\d*)?)'),  # Integer or decimal number
        ('MISMATCH', r'.'),  # Any other character
    ]
    line_start = 0
    if expression == '':
        return None
    if not suppress and (expression != '' or expression != '\n'):
        print("input:", [expression])
    for tokens in token_specification:
        kind = tokens[0]
        regex = tokens[1]
        arg: any = None
        if m := re.search(regex, expression):
            column = m.start() - line_start
            value: any = None
            if kind != "SKIP" and kind != "NEWLINE":
                if not suppress:
                    print("exp:", [expression], "| groups:", m.groups(), 'kind:', kind, )
                value: any = m[1]  # TODO move
            match kind:
                case "FUNC_DEC":
                    arr = []
                    for i in m.group(2).split(','):
                        arr.append(eval(i, line_num))
                    arg = arr
                case "FUNC":
                    arg = m.group(2)
                    if not just_kind and arg:
                        if m.group(1) in func_declarations:
                            print("found:", expression)
                            start, end = func_declarations[m.group(1)]
                            print('code', code[start:end + 1])
                            kind = 'CLOSURE'
                            arg = code[start + 1:end]  # TODO: contains \n and empty lines
                            print("========evaluating func call============")
                            arr = []
                            for i in arg:
                                jump_line_num = func_declarations[value]
                                arr.append(eval(i, jump_line_num[0]-1))  # FIXME: line_num wrong
                            arg = arr
                            print("========= end of eval =================")
                        else:
                            arg = eval(arg, line_num)
                case 'CLOSURE':
                    arg = m.group(2)
                    if not just_kind and arg:
                        # handles arg conditions for loops and ifs
                        args = re.findall(fr'(\w[><=]?=?\w?)', m.group(2))
                        arr = []
                        for i in args:  # evaluate each argument individually
                            arr.append(eval(i, line_num))
                        arg = arr
                case 'DEC':
                    value = m.group(1)
                    arg = m.group(2)
                case 'VAR':
                    if value in keywords:
                        break
                    t = back_prop(m[1], line_num)
                    return t
                case 'ASSIGN':
                    arg = m[2]
                    if not just_kind:
                        arg = eval(arg, line_num)
                        # return arg  # TODO: maybe keep to remove all assigns
                case 'NUM':
                    value = float(value) if '.' in value else int(value)
                # case 'BOOL':
                #     value = "true" == value
                case 'OP':
                    value = m[2]
                    arg1, arg2 = m[1], m[3]
                    if m[1] != '+' or m[1] != '-':
                        arg1 = eval(m[1], line_num)
                    if m[3] != '+' or m[3] != '-':
                        arg2 = eval(m[3], line_num)
                    arg = [arg1, arg2]
                case 'NEWLINE':
                    line_num -= 1
                    line_start = m.end()
                    expression = expression.replace('\n', '')  # FIXME: needs to only replace the first newline
                    continue
                case 'SKIP':
                    # expression.replace(m[0], '')  # TODO: test if this works
                    continue
                case 'MISMATCH':
                    raise RuntimeError(f'{value!r} unexpected on line {line_num}')
            t = Exp(kind, value, arg, line_num, column)
            if not suppress:
                print(t)
            return t


# os.system("gcc test.c")
f = open('test.c')
file = f.read()
f.close()
file_arr = file.split('\n')
min_file_arr = minify.minify_source(file_arr)
min_file_arr[:] = [i for i in min_file_arr if i != '']  # remove all empty lines

# ====================first scan ====================
min_file = "\n".join(min_file_arr)
code = re.split('([;{}])', min_file)
code[:] = [i for i in code if i != ';']  # remove semicolons
curr_func = ""
curly_num = 0
for line_num, line in enumerate(code):
    exp = re.search(fr'{name} ({name})\((.*)\)', line)
    if exp and curly_num == 0:
        func_declarations[exp[1]] = [line_num + 1, None]
        curr_func = exp[1]
    elif re.search(r'{', line):
        curly_num += 1
    elif re.search(r'}', line):
        curly_num -= 1
        if curly_num == 0:
            func_declarations[curr_func][1] = line_num
print("func declarations:", func_declarations)
# ========================================

min_file = "\n".join(min_file_arr[:12])
# min_file = "\n".join(min_file_arr[9:11])
# min_file = "\n".join(min_file_arr)
truncated_code = re.split('([;{}])', min_file)
truncated_code[:] = [i for i in truncated_code if i != ';']  # remove semicolons
print("code", truncated_code)
ans = []
for i, line in enumerate(reversed(truncated_code)):
    line_num = len(truncated_code) - i
    print("------", line_num, "------")
    ans.append(eval(line, line_num))

print("=====")
for i in ans:
    if i:
        print(i)
