import numpy as np
import os
import itertools
import oracle
import argparse

from pyquil import Program, get_qc
from pyquil.quil import DefGate
from pyquil.gates import X, H
from pyquil.latex import * 


def black_box(n, balanced):
    """
    Unitary representation of the black-box operator on (n+1)-qubits
    """
    d_bb = black_box_map(n, balanced=balanced)
    # initialize unitary matrix
    N = 2**(n+1)
    unitary_rep = np.zeros(shape=(N, N))
    # populate unitary matrix
    for k, v in d_bb.items():
        unitary_rep += np.kron(projection_op(k), np.eye(2) + v*(-np.eye(2) + np.array([[0, 1], [1, 0]])))
        
    return unitary_rep

def projection_op(qub_string):
    """
    Creates a projection operator out of the basis element specified by 'qub_string', e.g.
    '101' -> |101> <101|
    """
    ket = qubit_ket(qub_string)
    bra = np.transpose(ket)  # all entries real, so no complex conjugation necessary
    proj = np.kron(ket, bra)
    return proj


def qubit_ket(qub_string):
    """
    Form a basis ket out of n-bit string specified by the input 'qub_string', e.g.
    '001' -> |001>
    """
    e0 = np.array([[1], [0]])
    e1 = np.array([[0], [1]])
    d_qubstring = {'0': e0, '1': e1}

    # initialize ket
    ket = d_qubstring[qub_string[0]]
    for i in range(1, len(qub_string)):
        ket = np.kron(ket, d_qubstring[qub_string[i]])
    
    return ket

def black_box_map(n, balanced):
    """
    Black-box map, f(x), on n qubits represented by the vector x
    """
    qubs = qubit_strings(n)

    # assign a constant value to all inputs if not balanced
    if not balanced:
        const_value = np.random.choice([0, 1])
        d_blackbox = {q: const_value for q in qubs}

    # assign 0 to half the inputs, and 1 to the other inputs if balanced
    if balanced:
        # randomly pick half the inputs
        half_inputs = np.random.choice(qubs, size=int(len(qubs)/2), replace=False)
        d_blackbox = {q_half: 0 for q_half in half_inputs}
        d_blackbox_other_half = {q_other_half: 1 for q_other_half in set(qubs) - set(half_inputs)}
        d_blackbox.update(d_blackbox_other_half)
    
    return d_blackbox

def qubit_strings(n):
    qubit_strings = []
    for q in itertools.product(['0', '1'], repeat=n):
        qubit_strings.append(''.join(q))
    return qubit_strings


class Algo():
    def measure(self, result, n, t, args):
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

    def qc_program(self, n, t, reload, b, v):
        qc = get_qc(str(n+1)+'q-qvm')
        qc.compiler.client.timeout = 1000000

        U_f_def = DefGate('U_f', self.__getUf(n, b, reload, v))
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
