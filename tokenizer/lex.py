from typing import NamedTuple, Type
import re, os
import minify


# NOTE: the line numbers are based on the filter.c line-numbers not the original file
# TODO: add fuzziness

class Exp:
    g_tab = 0

    def __init__(self, type, value, arg, line, column):
        self.type: str = type
        self.value: any = value
        self.arg: list = arg  # FIXME
        self.line: int = line
        self.column: int = column

    def format(self, tab_num=0):
        s = ""
        if self.type == 'FUNC':
            s += f'{self.type}({self.value} :\n' + '\t' * tab_num
            if self.arg.type == 'CLOSURE':  # divide between normal func calls and while,if...
                return self.format_closure(s, tab_num, self.arg)
            else:
                return f'{self.type}({self.value}{(" | " + str(self.arg)) if self.arg else ""})'
        if self.type == 'CLOSURE':  # and self.value != 'if':
            return self.format_closure(s, tab_num, self)
        else:
            return f'{self.type}({self.value}{(" | " + str(self.arg)) if self.arg else ""})'

    def format_closure(self, s, tab_num, exp):
        s += f'{exp.type}(\n'
        for i in exp.arg:
            if i is not None:
                s += '\t' * (Exp.g_tab + tab_num + 1) + i.format(tab_num + 1) + '\n'
        return s + '\t' * tab_num + ')'

    def __repr__(self):
        return self.format()

    def __str__(self):
        return self.format()


name = r'[a-zA-Z_-][\w-]*'  # for names of func/var and data types
keywords = {
    'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum', 'extern',
    'float', 'for', 'goto', 'if', 'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static',
    'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while'
}

func_declarations: dict[str, list[int, int]] = {}


# TODO: replace with LUT
def back_prop(var_name, line_num, past_calls):
    print("=====back prop=====")
    print('looking for:', var_name, 'line_num:', line_num)
    line_num -= 1
    ex: Exp = None
    truncated_code = code[:line_num]
    # truncated_min = "\n".join(min_file_arr[:line_num])
    # truncated_code = re.split('[;{}]', truncated_min)
    curl_count = 0
    for l in reversed(truncated_code):  # searching from line_num to top of page
        # print("testing:", [l])
        if l == '{' or l == '}':
            print("found curl")
            # for closures backprop should only exit closures and never enter one
            if l == '}':  # skipping a closure
                curl_count += 1
            elif curl_count != 0:  # and (ex.value == '{' or ex.type == 'FUNC_DEC'):  # exiting a closure
                curl_count -= 1
            continue
        if curl_count > 0:  # currently inside a closure so it needs to ignore all the code
            print("skip")
            continue

        ex: Exp = eval(l, line_num, past_calls, just_kind=True)
        arr = []
        if ex.type != "exp":
            arr = [ex]
        else:
            ex: Exp = eval(l, line_num, past_calls, just_kind=False)
            arr = ex.arg
        for j in arr:
            if j is None:
                continue
            if j.type == 'NUMBER':
                # break
                print("=====end=====")
                return j
            if j.type == 'ASSIGN' and j.value == var_name:
                # if j.type == 'ASSIGN':
                #     j = back_prop(min_file_arr.indj(l), j.arg)
                # break
                print("=====end=====")
                return j
            if j.type == 'FUNC_DEC':
                for i in j.arg:
                    if i.arg == var_name:
                        print("=====end=====")
                        return i
    print("=====end=====")
    return ex


def eval(expression: str, line_num: int, past_calls: set, just_kind: bool = False, suppress=False) -> Exp:
    token_specification = (  # TODO: maybe move out of func
        # ('NEWLINE', r'\n'),  # Line endings
        ('SKIP', r'([ \t{}]+)'),  # FIXME: picks up curls? # Skip over spaces and tabs
        ('STRING', r'(\".*\")'),
        # ('CLOSURE', fr'^(if|for|while|do|else)\((.*)\)'),  # if and loops
        ('OP', r'([\w+-]*)?([+-]{2})([\w+-]*)?'),
        ('OP', fr'([\w-]*)([><]=?)([\w-]*)'),  # comparators
        ('ASSIGN', fr'{name}?\*? ?({name})=(.*)'),  # Assignment operator # TODO: types gets lost, EX: int y = x;
        ('FUNC', fr'(\({name}\*?\))(\(?.*\)?)'),  # casts
        ('OP', fr'([\w-]*)([+\-*/])([\w-]*)'),  # Arithmetic operators
        # ('BOOL', r'^(true|false)'),  # bool
        ('FUNC', r'(return) ?(.*)'),  # return
        ('FUNC_DEC', fr'{name} ({name})\((.*)\)'),  # function declaration
        ('DEC', fr'(^{name}) ({name})'),  # declare variable
        ('FUNC', fr'({name})\((.*)\)'),  # function call
        ('VAR', fr'({name})'),  # Variable (that needs to be derived)
        ('CLOSURE', r'([\{])'),
        ('CURL', '(\})'),
        ('NUM', r'^(\d+(\.\d*)?)'),  # Integer or decimal number
        ('EXP', r'(.*)')  # any unevaluated expressions
        # ('MISMATCH', r'.'),  # Any other character
    )
    line_start = 0
    if expression == '':
        return None
    if not suppress and (expression != '' or expression != '\n'):
        print("input:", [expression], "line num:", line_num)
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
                        arr.append(eval(i, line_num, past_calls))
                    arg = arr
                case "FUNC":
                    arg = m.group(2)
                    if not just_kind:  # and arg:
                        func_name = m.group(1)
                        if func_name in past_calls:  # protect against cyclic calls
                            print("cyclic/recursive call to", func_name)
                            kind = "recursive_call"
                        elif func_name in func_declarations:
                            arr = []
                            for i in m[2].split(','):
                                arr.append(eval(i, line_num, past_calls))
                            value = (m[1], arr)  # TODO: call eval on all the args when calling a func
                            past_calls.add(func_name)
                            print("found:", expression)
                            start, end = func_declarations[func_name]
                            # ==
                            print('code', code[start:end + 1])
                            # kind = 'CLOSURE'
                            arg = code[start + 1:end]  # TODO: contains \n and empty lines
                            # ==
                            print("========evaluating func call============")

                            if line_num < start or line_num > end:  # TODO: move up
                                arg = eval(code[start], start + 1, past_calls)
                            else:
                                print("recursive call to", func_name)
                                kind = "recursive_call"
                            print("========= end of eval =================")
                        else:
                            if func_name != 'while' and func_name != 'if' and func_name != 'for':  # dont add while, if, for, in past_calls
                                past_calls.add(func_name)
                            arg = eval(arg, line_num, past_calls)
                case 'CLOSURE':
                    # arg = m.group(2)
                    curl_count = 1
                    if not just_kind:
                        arr = []
                        i = line_num + 1
                        print("start closure")
                        while code[i - 1] != '}' or curl_count > 0:
                            e = eval(code[i - 1], i, past_calls)
                            if e.value != '}':  # To prevent curl token from being added
                                arr.append(e)

                            if e.type == "CLOSURE":  # jump if its is an inline closure(while, if...)
                                i += len(e.arg) + 1
                            else:
                                i += 1

                            if code[i - 1] == '{':
                                curl_count += 1
                            elif code[i - 1] == '}':
                                curl_count -= 1
                        print("end closure")
                        arg = arr
                case 'DEC':
                    value = m.group(1)
                    arg = m.group(2)
                case 'VAR':
                    if value in keywords:
                        break
                    t = back_prop(m[1], line_num, past_calls)
                    return t
                case 'ASSIGN':
                    arg = m[2]
                    if not just_kind:
                        arg = eval(arg, line_num, past_calls)
                        # return arg  # TODO: maybe keep to remove all assigns
                case 'NUM':
                    value = float(value) if '.' in value else int(value)
                # case 'BOOL':
                #     value = "true" == value
                case 'OP':
                    value = m[2]
                    arg1, arg2 = m[1], m[3]
                    if not just_kind:
                        if not (m[1] == '+' or m[1] == '-'):
                            arg1 = eval(m[1], line_num, past_calls)
                        if not (m[3] == '+' or m[3] == '-'):
                            arg2 = eval(m[3], line_num, past_calls)
                    arg = [arg1, arg2]
                # case 'NEWLINE':
                #     line_num -= 1
                #     line_start = m.end()
                #     expression = expression.replace('\n', '')  # FIXME: needs to only replace the first newline
                #     continue
                case 'SKIP':
                    # expression.replace(m[0], '')  # TODO: test if this works
                    continue
                case 'MISMATCH':
                    raise RuntimeError(f'{value!r} unexpected on line {line_num}')
            t = Exp(kind, value, arg, line_num, column)
            if not suppress:
                print(t)
            if m.end() - m.start() != len(expression):  # splitting the expression if only a part of it is understood
                arg = [t]
                if m.start() != 0:  # if there is something before
                    arg = [eval(expression[:m.start()], line_num, past_calls), t]
                if m.end() != len(expression):  # if there is something before
                    arg.append(eval(expression[m.end():], line_num, past_calls))
                return Exp("exp", expression, arg, line_num, column)
            return t


code = None


def preproc(file_name):
    global code
    # os.system("gcc test.c")
    f = open(file_name)
    file = f.read()
    f.close()
    file_arr = file.split('\n')
    min_file_arr = minify.minify_source(file_arr)
    min_file_arr[:] = [i for i in min_file_arr if i != '']  # remove all empty lines

    min_file = "".join(min_file_arr)
    code = re.split('([;{}])', min_file)
    code = [i for i in code if not (i == ';' or i == '')]  # remove semicolons
    # ==================== first scan ====================
    curr_func = ""
    curly_num = 0
    for line_num, line in enumerate(code):
        exp = re.search(fr'{name}\*? ({name})\((.*)\)', line)
        if exp and curly_num == 0:
            func_declarations[exp[1]] = [line_num + 1, None]
            curr_func = exp[1]
        elif re.search(r'{', line):
            curly_num += 1
        elif re.search(r'}', line):
            curly_num -= 1
            if curly_num == 0:
                func_declarations[curr_func][1] = line_num  # +1
    print("func declarations:", func_declarations)
    # ========================================

    f = open("filter.c", "w")
    f.write("\n".join(code))
    f.close()

    offset = func_declarations['main'][0] - 1
    truncated_code = code[offset:]
    print("code", truncated_code)
    ans = []
    # for i, line in enumerate(truncated_code):
    #     line_num = i + offset+1
    #     print("------", line_num, "------")
    #     ans.append(eval(line, line_num, set()))
    print("------", offset + 1, "------")
    ans.append(eval(code[offset], offset + 1, set()))
    print("------", offset + 2, "------")
    ans.append(eval(code[offset + 1], offset + 2, set()))

    print("\n=== ANS ===")
    for i in ans:
        if i:
            print(i)


if __name__ == '__main__':
    preproc("test.c")
