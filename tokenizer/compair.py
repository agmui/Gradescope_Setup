from lex import Evaluator

e = Evaluator()
e.preproc("solution.c")
# e.eval(e.code[0], 1, {})
ans = e.eval(e.code[1], 2, set())
arr = []
for i, a in enumerate(ans.arg):
    arr.append(e.eval(a, i + 3, set()))
    print("==")
    print(arr[i])
ans.arg = arr
print(ans)
# e.preproc("student.c")
