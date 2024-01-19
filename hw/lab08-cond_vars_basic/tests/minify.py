import re

# Ops: ops that may be spaced out in the code but we can trim the whitespace before and after
# Spaced ops are operators that we need to append with one trailing space because of their syntax (e.g. keywords).
# NB: theses ops are the SUPPORTED ones and these lists may not be complete as per the Standard
OPS = [
    '+', '-', '*', '/', '%', '++', '--',
    '+=', '-=', '*=', '/=', '%=', '=', '==', '!=',
    '&&', '||', '!', '&', '|', '^', '<<', '>>',
    '<', '>', '<=', '>=', '<<=', '>>=', '&=', '|=', '^=', ',',
    '(', ')', '{', '}', ';', 'else', ':', '::', '?'
]
SPACED_OPS = ['else']
UNARY_OPS = ["+", "-", "&", "!", "*"]
PREPROCESSOR_TOKEN = '#'


def remove_everything_between(subs1, subs2, line):
    regex = re.compile(subs1 + r'.*' + subs2)
    return regex.sub('', line)


def remove_everything_before(subs, line):
    regex = re.compile(r'.*' + subs)
    return regex.sub('', line)


def remove_everything_past(subs, line):
    regex = re.compile(subs + r'.*')
    return regex.sub('', line)


def remove_multiline_comments(lines):
    start, end = '/*', '*/'
    escaped_start, escaped_end = '/\*', '\*/'
    in_comment = False
    newlines = []
    for line in lines:
        if not in_comment:
            start_pos = line.find(start)
            if start_pos != -1:
                in_comment = True
                end_pos = line.find(end)
                # inline multiline comment
                if start_pos < end_pos:
                    line = remove_everything_between(escaped_start, escaped_end, line)
                    in_comment = False
                else:
                    line = remove_everything_past(escaped_start, line)
        else:
            end_pos = line.find(end)
            if end_pos != -1:
                line = remove_everything_before(escaped_end, line)
                in_comment = False
                start_pos = line.find(start)
                # start of another comment on the same line
                if start_pos != -1:
                    line = remove_everything_past(escaped_start, line)
                    in_comment = True
            else:
                line = ''
        newlines.append(line)
    return newlines


def remove_inline_comments(lines):
    return map(lambda x: remove_everything_past('//', x), lines)


def minify_operator(op):
    """Returns a function applying a regex to strip away spaces on each side of an operator
    Makes a special escape for operators that could be mistaken for regex control characters."""
    to_compile = " *{} *".format(re.escape(op))
    regex = re.compile(to_compile)
    repl = op
    if op in SPACED_OPS:
        repl += " "
    return lambda string: regex.sub(repl, string)


def fix_spaced_ops(lines):
    """This will walk the spaced ops list and search the text for all "[OP] {" sequences occurrences
    and replace them by "[OP]{" since there is no operator in the C syntax for which the spacing
    between the op and the '{' is mandatory.
    We do this because to manage spaced ops that may or may not be used with braces (e.g. "else"),
    we may have added unnecessary spaces (e.g. because the brace was on next line),
    so we can fix it here."""
    for i in range(len(lines)):
        for op in SPACED_OPS:
            pattern = "{} {{".format(op)  # {{ for literal braces
            repl = "{}{{".format(op)
            lines[i] = re.sub(pattern, repl, lines[i])
    return lines


def fix_unary_operators(lines):
    """Ops processing can have eliminated necessary space when using unary ops
    e.g. "#define ABC -1" becomes "#define ABC-1", because the unary '-' is being
    mistaken for a binary '-', so the space has been trimmed.
    We can fix this kind of thing here, but it pretty much highlights the limits of such
    a parser..."""
    regex_unary_ops = '[{}]'.format(''.join(UNARY_OPS))
    regex_unary_ops = re.escape(regex_unary_ops)
    # Use capture groups to separate, e.g. in "#define MACROVALUE", "#define MACRO" from "VALUE"
    # pattern will detect problems like "#define FLUSH-2"
    # Format braces here -----------v
    pattern = "^(#[a-z]+ +[\w\d]+)([{}][\w\d]+)$".format(regex_unary_ops)
    # Simply add one more space between macro name and value
    repl = r'\1' + " " + r'\2'
    # Process each preprocessor line and modify it inplace as we need to keep order
    for (idx, line) in enumerate(lines):
        if is_preprocessor_directive(line):
            for op in UNARY_OPS:
                line = re.sub(pattern, repl, line)
            lines[idx] = line
    return lines


def is_preprocessor_directive(line):
    return line.startswith(PREPROCESSOR_TOKEN)


def clear_whitespace_first_pass(lines):
    """Given a list of lines, clears all leading/trailing whitespace"""
    lines = map(lambda x: x.replace('\t', ' '), lines)
    # specify only spaces so it doesn't strip newlines
    lines = map(lambda x: x.strip(' '), lines)
    return list(lines)


def minify_source(lines):
    """
    The main function where the minification happens.
    Main steps:
    - clear leading/trailing whitespace and add newlines back again to
    preprocessor directives lines
    - minify operators that can be used without spaces
    - fix unary operators that we could have taken for binary operators (e.g. -)
    - re-concatening all lines and final fixes to possible over-spacing
    """

    # Things to do BEFORE processing spaced ops:
    # - erase leading and trailing whitespace
    # so they stay on their own line even minified
    lines = clear_whitespace_first_pass(lines)

    # for each operator: remove space on each side of the op, on every line.
    # Escape ops that could be regex control characters.
    for op in OPS:
        lines = map(minify_operator(op), lines)
    lines = remove_inline_comments(lines)
    lines = remove_multiline_comments(lines)
    # Finally convert all remaining multispaces to a single space
    multi_spaces = re.compile(r'[  ]+ *')
    lines = list(map(lambda string: multi_spaces.sub(' ', string), lines))
    # Ops processing can have eliminated necessary space when using unary ops
    # e.g. "#define ABC -1" becomes "#define ABC-1", so we can fix it here
    lines = fix_unary_operators(lines)

    # There is no syntactic requirement of an operator being spaced from a '{' in C so
    # if we added unnecessary space when processing spaced ops, we can fix it here
    lines = fix_spaced_ops(lines)
    return lines


if __name__ == '__main__':
    file = open('main.c')
    file_arr = file.read().split('\n')
    file.close()
    for i in minify_source(file_arr):
        print(i)
    minify_source(file_arr)
