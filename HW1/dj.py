import numpy as np
import os
import itertools
import oracle
import argparse

from pyquil import Program, get_qc
from pyquil.quil import DefGate
from pyquil.gates import X, H
from pyquil.latex import * 

class Algo():
    def measure(self, result, n, t, args):
        if v:
            print("\n====================================")
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
            if not self.check_valid(measured_bits, args):
                return False
        return True

class DJ(Algo):
    def __getUf(self, n, balanced, reload, v):
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

    def check_valid(self, m_bits, balanced):
        return not all(x == 0 for x in m_bits) if balanced else all(x == 0 for x in m_bits)

    def qc_program(self, n, t, reload, balanced, v):
        path = "compiled_programs/dj/{}{}".format('bal' if balanced else 'const', n)

        qc = get_qc(str(n+1)+'q-qvm')
        qc.compiler.client.timeout = 1000000

        U_f_def = DefGate('U_f', self.__getUf(n, balanced, reload, v))
        U_f = U_f_def.get_constructor()

        p = Program()
        p += U_f_def
        p += X(0)
        p += (H(i) for i in range(n+1))
        p += U_f(*(tuple(range(n+1))))
        p += (H(i) for i in range(1,n+1))

        # if not os.path.exists(path) or reload:
        #     with open(path, 'wb+') as c:
        #         ep = qc.compile(p)
        #         c.write(ep)
        #         c.close()
        # else:
        #     ep = open(path, rb)
        # if v:
        #     print("===========================")
        #     print("   **Compiling Program**   ")
        #     print("===========================\n")
        # ep = qc.compile(p)
        # print(ep)
        if v:
            print("===========================")
            print("**Running Quantum Program**")
            print("===========================\n")
        # results = []
        # for i in range(t):
        #     if v:
        #         print("     Measuring Result For [{}]".format(i+1))
        #     result = qc.run(ep)
        #     print(result)
        #     results.append(result)
            
        results = qc.run_and_measure(p, trials=t)
        return self.measure(results, n, t, balanced)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CS239 - Spring 20 - Deustch-Josza', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.set_defaults(reload=False, balanced=False, verbose=False)
    parser.add_argument("--num", "-n", type=int, default=4, help="Set size of input string")
    parser.add_argument("--trials", "-t", type=int, default=2, help="Set num of trials")
    parser.add_argument("--reload", "-r", action="store_true", help='Reload new U_f matrix')
    parser.add_argument("--balanced", "-b", action="store_true", help='Set whether f(x) is balanced or constant')
    parser.add_argument("--verbose", "-v", action="store_true", help='Print out measured bits and steps')
    args = parser.parse_args()

    n = args.num
    t = args.trials
    r = args.reload
    b = args.balanced
    v = args.verbose
    dj = DJ()

    print("=======================================================")
    print("Testing Deutsch-Josza Algorithm on {} Function".format('Balanced' if b else 'Constant'))
    if v:
        print("\n   Running with bit string of size n = {}".format(n))
        print("                  number of trials t = {}".format(t))
        print("                   reload U_f matrix = {}".format(r))
    print("=======================================================\n")

    if int(n) > 9:
        print("Haha so we run out of heap space with something bigger than 9...\n Try something smaller :)")
        ret = input("Would you like to continue? [y/n]: ")
        if ret == 'n' or ret == 'N':
            print("Good Choice :)")
            exit()

    ret =  dj.qc_program(n, t, r, b, v)
    print("Implemented Deutsch-Josza Algorithm {}\n".format('Success!!!' if ret else 'Fail :('))