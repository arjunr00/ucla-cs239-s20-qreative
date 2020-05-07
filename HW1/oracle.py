import numpy as np

def gen_matrix(f, n, m):
    """
    Generates the quantum oracle corresponding to f, where f is defined as:
        f : {0,1}^n -> {0,1}^m

    Let x and b be bitstrings of length n. Let (*) represent the tensor product
    and + represent bitwise XOR. Then:
        U_f = Sum(|x><x| (*) |b + f(x)><b|)
    Here, `Sum` sums over all bitstrings xb.

    Args:
        f: The function as defined above.
        n: The dimension of f's domain.
        m: The dimension of f's range.

    Returns:
        A (2^n)x(2^m) matrix U_f which represents the quantum oracle corresp-
        onding to f.
    """

    # Accumulator to hold the value of the summation
    U_f=np.zeros((2**(n+m),2**(n+m)))
    for xb in range(0, int(2**(n+m))):
        # Convert index to binary and split it down the middle
        x  = f'{xb:0{n+m}b}'[:int(n)]
        b  = f'{xb:0{n+m}b}'[int(n):]
        # Apply f to x
        fx = f(x)
        # Calculate b + f(x)
        bfx = f'{int(b, 2) ^ int(fx, 2):0{n}b}'

        # Vector representations of x, b, and b+f(x)
        xv = np.zeros((2**n,1))
        xv[int(x, 2)] = 1.
        bv = np.zeros((2**m,1))
        bv[int(b, 2)] = 1.
        bfxv = np.zeros((2**m,1))
        bfxv[int(bfx, 2)] = 1.

        # Accumulate (|x><x| (*) |b + f(x)><b|) into the sum
        # (*) is the tensor product
        U_f = np.add(np.kron(np.outer(xv, xv), np.outer(bfxv, bv)), U_f)

    return U_f

def is_unitary(m):
    return np.allclose(np.eye(len(m)), m.dot(m.T.conj()))

def f(x):
    # n = 3
    # s = 110
    ans = {
        '000': '101',
        '001': '010',
        '010': '000',
        '011': '110',
        '100': '000',
        '101': '110',
        '110': '101',
        '111': '010',
    }
    return ans[x]

def g(x):
    # n = 2
    # s = 11
    ans = {
        '00': '01',
        '01': '11',
        '10': '11',
        '11': '00'
    }
    return ans[x]

def h(x):
    # n = 2
    ans = {
        '0': '1',
        '1': '0',
    }
    return ans[x]

# Tests
U_f = gen_matrix(f, 3, 3)
assert is_unitary(U_f)
U_g = gen_matrix(g, 2, 2)
assert is_unitary(U_g)
U_h = gen_matrix(h, 1, 1)
assert is_unitary(U_h)
