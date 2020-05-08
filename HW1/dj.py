import numpy as np
import itertools
import oracle
import argparse

from pyquil import Program, get_qc
from pyquil.gates import *
from pyquil.latex import * 

def getUf(n, balanced, reload):
    if not reload:
        path = 'uf/dj/{}{}.npy'.format('bal' if balanced else 'const', n)
        U_f = np.load(path)
    else:
        U_f = oracle.uf(n, 1, oracle.Algos.DJ, oracle.DJ.BALANCED if balanced else oracle.DJ.CONSTANT)
    return U_f

def check_valid(m_bits, balanced):
    return set(m_bits) == set([0,1]) if balanced else set(m_bits) == set([0])

def qc_program(n, t, reload, balanced, v):
    p = Program()
    p.defgate('U_f', getUf(n, balanced, reload))
    qc = get_qc('9q-square-qvm')
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
        if not check_valid(measured_bits, False):
            return False
    return True

parser = argparse.ArgumentParser(description='CS239 - Spring 20 - Deustch-Josza', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--num", "-n", type=int, default=4, help="Set size of input string")
parser.add_argument("--trials", "-t", type=int, default=10, help="Set num of trials")
parser.add_argument("--reload", "-r", type=bool, default=False, help='Reload new U_f matrix')
parser.add_argument("--balanced", "-b", type=bool, default=False, help='Set whether f(x) is balanced or constant')
parser.add_argument("--verbose", "-v", type=bool, default=False, help='Print out measured bits and steps')
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

    ret =  qc_program(n, t, r, b, v)
    print("Implemented Deutsch-Josza Algorithm {}\n".format('Success!!!' if ret else 'Fail :('))