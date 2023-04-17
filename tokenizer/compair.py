from lex import Evaluator

solution = Evaluator()
solution.preproc("solution.c")
ans, jump_to = solution.eval(solution.code[1], 2, set())
arr = []

i = 0
while i < len(ans.arg):
    exp, jump_to = solution.eval(ans.arg[i], i + 3, set(), suppress=True)
    arr.append(exp)
    print("==")
    # print(arr[i])
    i += 1
    if jump_to != 0:
        i = jump_to
ans.arg = arr

print(ans)

# ============
student = Evaluator()
student.preproc("student.c")

ans, jump_to = student.eval(student.code[1], 2, set())
arr = []

i = 0
while i < len(ans.arg):
    exp, jump_to = student.eval(ans.arg[i], i + 3, set(), suppress=True)
    arr.append(exp)
    print("==")
    # print(arr[i])
    i += 1
    if jump_to != 0:
        i = jump_to
ans.arg = arr

print(ans)
