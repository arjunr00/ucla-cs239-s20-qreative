import numpy as np
import argparse
import math
import os
import oracle
import time

from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram
from qiskit.quantum_info.operators import Operator

def get_z0(n):
    m = np.identity(2**n)
    m[0][0] = -1
    m *= -1
    return m

def get_zf(n, reload, verbose):
    path = f'uf/grover/grover{n}.npy'
    if not reload and os.path.exists(path):
        Z_f = np.load(path)
    else:
        if verbose: 
            print(f'Getting new Zf .. ', end='', flush=True)
        Z_f = oracle.uf(n, 1, algo=oracle.Algos.GROVER)
        if verbose:
            print('done')
    return Z_f

def check_validity(n, qubits, verbose):
    FPATH = 'uf/grover/f_list.npy'
    # If the matrix has been reloaded, assume the user has access to f
    # and so doesn't need to be told whether the algorithm was correct.
    if not os.path.exists(FPATH):
        return True

    f = np.load(FPATH, allow_pickle=True).item()[n]
    if verbose:
        print(f'    => f({qubits}) = {f[qubits]}')
    return f[qubits] == '1'

def qc_program(n, reload, verbose):
    N = 2**n
    sqrtN = math.sqrt(N)

    # For "very large" N, this is a good approximation
    k = math.floor((math.pi * sqrtN)/4)
    if verbose:
        print('====================================')
        # U+2248 is the Unicode encoding for approximately equal to
        # U+230A is the Unicode encoding for left floor
        # U+230B is the Unicode encoding for right floor
        # U+03C0 is the Unicode encoding for lowercase pi
        # U+221A is the Unicode encoding for sqrt
        # U+207f is the Unicode encoding for ^n
        print(f'[k \u2248 \u230a(\u03c0\u221aN)/4\u230b = {k}\t(N = 2\u207f = 2^{n})]\n')

    z0 = Operator(get_z0(n))
    zf = Operator(get_zf(n, reload, verbose))

    simulator = Aer.get_backend('qasm_simulator')
    circuit = QuantumCircuit(n+1, n)

    # Intialize
    circuit.x(n)
    circuit.h(range(n+1))
    
    # Loop
    for i in range(k):
        circuit.append(zf, range(n+1)[::-1])
        circuit.h(range(n))
        circuit.append(z0, range(n)[::-1])
        circuit.h(range(n))

    circuit.measure(range(n), range(n))
    if verbose: 
        print(f'Executing Circuit .. ', end='', flush=True)
    job = execute(circuit, simulator, shots=1)
    if verbose: 
        print('done')
    results = job.result().get_counts(circuit)
    qubits = [str(i) for i in results.keys()][0][::-1]

    if verbose:
        print(f'Measured Qubits: {qubits}')
        print('====================================\n')
    return check_validity(n, qubits, verbose)


parser = argparse.ArgumentParser(description='CS239 - Spring 20 - Grover', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.set_defaults(reload=False, verbose=False)
parser.add_argument("--num", "-n", type=int, default=4, help="Set length of input bitstring")
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

    # Store times
    TIMES_FILE = 'times/grover.csv'

    with open(TIMES_FILE, 'r') as file:
        times = file.readlines()

    lineno = n
    line=times[lineno].split(',')
    line[1] = f'{end - start:.4f}\n'
    times[lineno] = ','.join(line)

    with open(TIMES_FILE, 'w') as file:
        file.writelines(times)
