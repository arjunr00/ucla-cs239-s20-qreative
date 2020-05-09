import numpy as np
import argparse
import math
import os
import oracle
import time

from pyquil import Program, get_qc
from pyquil.quil import DefGate
from pyquil.gates import H, X
from pyquil.latex import *

def z0(n):
    m = np.identity(2**n)
    m[0][0] = -1
    m *= -1
    return m

def getZf(n, reload):
    if not reload:
        path = f'uf/grover/grover{n}.npy'
        Z_f = np.load(path)
    else:
        Z_f = oracle.uf(n, 1, algo=oracle.Algos.GROVER)

    return Z_f

def check_valid(n, x, verbose):
    FPATH = 'uf/grover/f_dict.npy'
    # If the matrix has been reloaded, assume the user has access to f
    # and so doesn't need to be told whether the algorithm was correct.
    if not os.path.exists(FPATH):
        return True

    f = np.load(FPATH, allow_pickle=True).item()[n]
    if verbose:
        print(f'    => f({x}) = {f[x]}')
    return f[x] == '1'

def qc_program(n, reload, verbose):
    N = 2**n
    sqrtN = math.sqrt(N)

    # For "very large" N, this is a good approximation
    k = math.floor((math.pi * sqrtN)/4)
    if verbose:
        print('====================================')
        # U+2248 is the Unicode encoding for approximately equal to
        # U+03C0 is the Unicode encoding for lowercase pi
        # U+221A is the Unicode encoding for sqrt
        # U+207f is the Unicode encoding for ^n
        print(f'k \u2248 (\u03c0\u221aN)/4 = {k}\t(N = 2\u207f = 2^{n})\n')

    Z_0_def = DefGate('Z_0', z0(n))
    Z_0 = Z_0_def.get_constructor()
    Z_f_def = DefGate('Z_f', getZf(n, reload))
    Z_f = Z_f_def.get_constructor()

    qc = get_qc(f'{str(2*n)}q-qvm')
    qc.compiler.client.timeout = 1000000

    p = Program()
    p += Z_0_def
    p += Z_f_def
    p += X(n)
    p += (H(i) for i in range(n+1))
    for i in range(k):
        p += Z_f(*(tuple(range(n+1))))
        p += (H(i) for i in range(n))
        p += Z_0(*(tuple(range(n))))
        p += (H(i) for i in range(n))

    result = qc.run_and_measure(p, trials=1)
    qubits = "".join(str(b) for b in [result[q][0] for q in range(n)])

    if verbose:
        print(f'Measured Qubits: {qubits}')

    correct = check_valid(n, qubits, verbose)

    if verbose:
        print('====================================\n')

    return correct

parser = argparse.ArgumentParser(description='CS239 - Spring 20 - Grover', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.set_defaults(reload=False, verbose=False)
parser.add_argument("--num", "-n", type=int, default=2, help="Set length of input bitstring")
parser.add_argument("--reload", "-r", action="store_true", help='Reload new U_f matrix')
parser.add_argument("--verbose", "-v", action="store_true", help='Print out measured bits and steps')
args = parser.parse_args()

if __name__ == '__main__':
    n = args.num
    r = args.reload
    v = args.verbose

    print('=======================================================')
    print('Testing Grover\'s Algorithm')
    if v:
        print(f'\n   Running with bit string of size n = {n},')
        print(f'                   reload U_f matrix = {r}')
    print('=======================================================\n')

    start = time.time()
    ret = qc_program(n, r, v)
    end = time.time()

    if ret is True:
        ret_str = "Success!"
    else:
        ret_str = "Fail :("

    print(f'Grover\'s Algorithm: {ret_str}')
    print(f'(Took {end - start:.2f} s to complete.)')
