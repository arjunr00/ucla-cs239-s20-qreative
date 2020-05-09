import numpy as np
import os
import itertools
import oracle
import argparse

from pyquil import Program, get_qc
from pyquil.gates import *
# from pyquil.latex import * 

def getUf(n, balanced, reload, v):
    path = 'uf/dj/{}{}.npy'.format('bal' if balanced else 'const', n)
    if not os.path.exists(path) or reload:
        U_f = oracle.uf(n, 1, oracle.Algos.DJ, oracle.DJ.BALANCED if balanced else oracle.DJ.CONSTANT)
        if v:
            print("New matrix U_f saved to path: "+path)
        np.save(path, U_f)
    else:
        U_f = np.load(path)
    if v:
        print("Matrix U_f is as follows: ")
        print(U_f)
        print()

    return U_f

def check_valid(m_bits, balanced):
    return not all(x == 0 for x in m_bits) if balanced else all(x == 0 for x in m_bits)

def qc_program(n, t, reload, balanced, v):
    p = Program()
    p.defgate('U_f', getUf(n, balanced, reload, v))
    qc = get_qc(str(n+1)+'q-qvm')
    qc.compiler.client.timeout = 1000000

    p.inst(X(n))
    p.inst(H(i) for i in range(n+1))
    p.inst(('U_f',) + tuple(range(n+1)))
    p.inst(H(i) for i in range(n))

    result = qc.run_and_measure(p, trials=t)
    if v:
        print("====================================")
        print("Measured Qubit State Accross Trials:\n")
        print(result)
        print("====================================\n")

    for i in range(t):
        measured_bits = [result[q][i] for q in range(n)]
        if v:
            print("====================================")
            print("Measured State for Iteration {}:\n".format(i+1))
            print(measured_bits)
            print("====================================\n")
        if not check_valid(measured_bits, balanced):
            return False
    return True

parser = argparse.ArgumentParser(description='CS239 - Spring 20 - Deustch-Josza', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.set_defaults(reload=False, balanced=False, verbose=False)
parser.add_argument("--num", "-n", type=int, default=4, help="Set size of input string")
parser.add_argument("--trials", "-t", type=int, default=10, help="Set num of trials")
parser.add_argument("--reload", "-r", action="store_true", help='Reload new U_f matrix')
parser.add_argument("--balanced", "-b", action="store_true", help='Set whether f(x) is balanced or constant')
parser.add_argument("--verbose", "-v", action="store_true", help='Print out measured bits and steps')
args = parser.parse_args()

if __name__ == "__main__":
    n = args.num
    t = args.trials
    r = args.reload
    b = args.balanced
    v = args.verbose

    print("=======================================================")
    print("Testing Deutsch-Josza Algorithm on {} Function".format('Balanced' if b else 'Constant'))
    if v:
        print("\n   Running with bit string of size n = {}".format(n))
        print("                  number of trials t = {}".format(t))
        print("                   reload U_f matrix = {}".format(r))
    print("=======================================================\n")

    # if int(n) > 8:
    #     print("Haha so we would havent found out how to make a qvm of more than 9 qubits...\ Try something smaller :)")
    #     exit()

    ret =  qc_program(n, t, r, b, v)
    print("Implemented Deutsch-Josza Algorithm {}\n".format('Success!!!' if ret else 'Fail :('))
