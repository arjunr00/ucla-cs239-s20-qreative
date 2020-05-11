import numpy as np
import os
import itertools
import oracle
import argparse

from pyquil import Program, get_qc
from pyquil.quil import DefGate
from pyquil.gates import X, H

class Algo():
    def measure(self, result, n, t, args):
        """
        Determines whether measured results are valid.
        **Uses algorithm specific check_valid function**

        Args: 
            result: result from after qc.run_and_measure(p, trials)
            n: number of bits
            t: number of trials
            args: balance flag

        Returns:
            True: if all results are valid
            False: if any results are invalid
        """
        if v:
            print("\n====================================")
            print("Measured Qubit State Accross Trials:\n")
            print(result)
            print("====================================\n")
            
        for i in range(t):
            measured_bits = [result[q][i] for q in range(1,n+1)]
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
        """
        We implemented a method to save our generated matrices to save compute time. 
        In doing so, we saved our U_f functions in the directory 'uf/{algo}/'. 

        __getUf allows you to either load a corresponding matrix Uf if it exists or load a new matrix that is balanced or constant

        **oracle.uf is a wrapper function in our oracle.py file (Generates a bit mapping and a U_f matrix)**

        Args: 
            n: number of bits
            balanced: balance flag
            reload: flag to reload U_f
            v: verbose flag

        Returns:
            Uf matrix for loaded or generated constant or balanced
        """
        path = 'uf/dj/{}{}.npy'.format('bal' if balanced else 'const', n)
        if not os.path.exists(path) or reload:                  # If path to oracle doesn't exist or reload flag => generate new U_f
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
        """
        Check if measured bits are valid. (Function similar to BV)
            If function is constant and all bits are 0 then true, else false
            If function is balanced and there is an even split of 0 and 1 then true, else false

        Args: 
            m_bits: measured bits from Algo.measure()
            balanced: true if balanced, false if constant

        Returns:
            True: if bits match function
            False: if any bit is off
        """
        return not all(x == 0 for x in m_bits) if balanced else all(x == 0 for x in m_bits)

    def qc_program(self, n, t, reload, b, v):
        """
        Quantum Circuit Program for Deutsch-Josza. Same as the one for Bernstein-Vazirani except with balanced flag.

        Args: 
            n: number of bits
            t: number of trials
            reload: flag to reload a_list
            b: balance flag
            v: verbose flag

        Returns:
            Array of results from qc.run_and_measure
        """
        qc = get_qc(str(n+1)+'q-qvm')               # set qvm based on input n, add one for helper qubit
        qc.compiler.client.timeout = 1000000        # set timeout to be massive because it takes a while to compile

        U_f_def = DefGate('U_f', self.__getUf(n, b, reload, v))
        U_f = U_f_def.get_constructor()             # U_f obtained above in __getUf

        p = Program()
        p += U_f_def
        p += X(0)
        p += (H(i) for i in range(n+1))
        p += U_f(*(tuple(range(n+1)[::-1])))        # We have to reverse ordering of U_f because |q0> is helper qubit
        p += (H(i) for i in range(1,n+1))

        if v:
            print("===========================")
            print("**Running Quantum Program**")
            print("===========================\n")
            
        results = qc.run_and_measure(p, trials=t)
        return self.measure(results, n, t, b)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CS239 - Spring 20 - Deustch-Josza', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.set_defaults(reload=False, balanced=False, verbose=False)
    parser.add_argument("--num", "-n", type=int, default=4, help="Set size of input string")
    parser.add_argument("--trials", "-t", type=int, default=2, help="Set num of trials")
    parser.add_argument("--reload", "-r", action="store_true", help='Reload new U_f matrix')
    parser.add_argument("--balanced", "-b", action="store_true", help='Set whether f(x) is balanced or constant')
    parser.add_argument("--verbose", "-v", action="store_true", help='Print out measured bits and steps')
    args = parser.parse_args()

    # Assign local variables to args and intialize DJ object
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
