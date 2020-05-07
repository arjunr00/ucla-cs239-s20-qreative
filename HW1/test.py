import oracle

def f(x):
    # n = 2
    ans = {
        '0': '1',
        '1': '0',
    }
    return ans[x]

U_f = oracle.generate(f, 1, 1)
print(U_f)
assert oracle.is_unitary(U_f)