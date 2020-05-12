import numpy as np
import os
import itertools
import oracle
import argparse
import random
import time

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
            measured_bits = [result[q][i] for q in range(1,n+1)]
            measured_bits = measured_bits[::-1]
            if v:
                print("====================================")
                print("Measured State for Iteration {}:\n".format(i+1))
                print(measured_bits)
                print("====================================\n")
            if not self.check_valid(measured_bits, args):
                return False
        return True

class BV(Algo):
    def __load_a_list(self, n, reload):
        if not os.path.exists('uf/bv'):
            os.makedirs('uf/bv')
        path = 'uf/bv/a_list.npy'
        if os.path.exists(path):
            a_list = np.load('uf/bv/a_list.npy', allow_pickle=True).item()
        else:
            a_list = {}
        if reload or n not in a_list.keys():
            a_list[n] = a = np.random.randint(low=0, high=2, size=n)
        else:
            a = a_list[n]
        np.save(path, a_list, allow_pickle=True)
        return a

    def __getUf(self, n, reload, v):
        path = 'uf/bv/bv{}.npy'.format(n)
        self.a = self.__load_a_list(n, reload)
        self.b = random.randint(0,1)
        if v:
            print("Alpha is as follows: ")
            print(self.a)
            print()
            print("Beta is as follows: ")
            print(self.b)
            print()
        if not os.path.exists(path) or reload:
            U_f = oracle.uf(n, 1, algo=oracle.Algos.BV, func=(self.a, self.b))
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

    def check_valid(self, m_bits, args):
        return all(self.a[i] == m_bits[i] for i in m_bits)

    def qc_program(self, n, t, reload, v):
        qc = get_qc(str(n+1)+'q-qvm')
        qc.compiler.client.timeout = 1000000

        U_f_def = DefGate('U_f', self.__getUf(n, reload, v))
        U_f = U_f_def.get_constructor()

        p = Program()
        p += U_f_def
        p += X(0)
        p += (H(i) for i in range(n+1))
        p += U_f(*(tuple(range(n+1)[::-1])))
        p += (H(i) for i in range(1,n+1))
        
        if v:
            print("===========================")
            print("**Running Quantum Program**")
            print("===========================\n")
            
        results = qc.run_and_measure(p, trials=t)
        return self.measure(results, n, t, None)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CS239 - Spring 20 - Bernstein-Vazirani', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.set_defaults(reload=False, balanced=False, verbose=False)
    parser.add_argument("--num", "-n", type=int, default=4, help="Set size of input string")
    parser.add_argument("--trials", "-t", type=int, default=2, help="Set num of trials")
    parser.add_argument("--reload", "-r", action="store_true", help='Reload new U_f matrix')
    parser.add_argument("--verbose", "-v", action="store_true", help='Print out measured bits and steps')
    args = parser.parse_args()

    n = args.num
    t = args.trials
    r = args.reload
    v = args.verbose
    bv = BV()

    print("=======================================================")
    print("         Testing Bernstein-Vazirani Algorithm          ")
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

    start = time.time()
    ret =  bv.qc_program(n, t, r, v)
    end = time.time()
    print("Implemented Bernstein-Varizani Algorithm {}\n".format('Success!!!' if ret else 'Fail :('))
    print(f'(Took {end - start:.2f} s to complete.)')
