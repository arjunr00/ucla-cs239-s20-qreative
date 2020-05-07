import numpy as np
import itertools
import random

def init_bit_mapping(n, dj=False, bv=False, simon=False, balanced=False):
    qubits = []
    for i in itertools.product(['0','1'], repeat=n):            # https://stackoverflow.com/questions/1457814/get-every-combination-of-strings
        qubits.append(''.join(i))
    if dj:
        if not balanced:        # Constant: f(x) returns 0 or 1 for all x
            val = np.random.choice(['0','1'])
            oracle_map = {i: val for i in qubits}
        else:
            val1 = random.sample(qubits, k=int(len(qubits)/2))
            val0 = set(qubits) - set(val1)
            oracle_map = {i: '1' for i in val1}
            temp = {i: '0' for i in val0}
            oracle_map.update(temp)
    return oracle_map

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
        A (2^n)x(2^m) matrix U_f which represents the quantum oracle corresponding
        to f.
    """

    # Accumulator to hold the value of the summation
    U_f=np.zeros((2**(n+m),2**(n+m)))
    for xb in range(0, int(2**(n+m))):
        # Convert index to binary and split it down the middle
        x  = f'{xb:0{n+m}b}'[:int(n)]
        b  = f'{xb:0{n+m}b}'[int(n):]
        # Apply f to x
        fx = f[x]
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