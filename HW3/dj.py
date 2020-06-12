print('Loading dependencies .. ', end='', flush=True)
import argparse
import oracle
import os
import matplotlib
import numpy as np
import time
from qiskit.quantum_info.operators import Operator
from qiskit import QuantumCircuit,execute,Aer
print('done\n', flush=True)

def getUf(n, f_type, reload, v):
    """
    We implemented a method to save our generated matrices to save compute time.
    In doing so, we saved our U_f functions in the directory 'uf/{algo}/'.

    getUf allows you to either load a matrix U_f if it exists or generate a new matrix that is balanced or constant

    **oracle.uf is a wrapper function in our oracle.py file (Generates a bit mapping and a U_f matrix)**

    Args:
        n: number of bits
        balanced: balance flag
        reload: flag to reload U_f
        v: verbose flag

    Returns:
        Uf matrix for loaded or generated constant or balanced
    """
    path = f'uf/dj/{"const" if f_type == oracle.DJ.CONSTANT else "bal"}{n}.npy'
    if not os.path.exists(path) or reload:                  # If path to oracle doesn't exist or reload flag => generate new U_f
        U_f = oracle.uf(n, 1, oracle.Algos.DJ, f_type)
        if v:
            print("New matrix U_f saved to path: "+path, flush=True)
        np.save(path, U_f)
    else:
        U_f = Operator(np.load(path))
    if v:
        print(f'Matrix U_f is: \n{U_f}\n', flush=True)

    return U_f

def generate_circuit(n, f_type, reload, v):
    SAVEDIR = 'plots/'
    CIRCUIT_FILENAME = f'dj_{n}.pdf'

    if (v): print('Getting U_f .. ', end='', flush=True)
    U_f = getUf(n, f_type, reload, v)
    if (v): print('done', flush=True)

    if (v): print('Creating circuit .. ', end='', flush=True)
    circuit = QuantumCircuit(n+1, n)

    circuit.x(n)
    for i in range(n+1):
        circuit.h(i)

    circuit.append(U_f, list(range(n+1))[::-1])

    for i in range(n):
        circuit.h(i)

    # Map the quantum measurement to the classical bits
    circuit.measure(list(range(n)), list(range(n)))
    if (v): print('done\n', flush=True)

    if v:
        print('Circuit:', flush=True)
        print(circuit.draw('text'), flush=True)
        circuit.draw('mpl')
        print(f'Saving circuit to {CIRCUIT_FILENAME} .. ', end='', flush=True)
        if not os.path.exists(SAVEDIR):
            os.mkdir(SAVEDIR)

        matplotlib.pyplot.savefig(f'{SAVEDIR}{CIRCUIT_FILENAME}')
        print('done\n', flush=True)
    return circuit

def run_circuit(circuit, s):
    if v: print(f'Loading simulator .. ', end='', flush=True)
    simulator = Aer.get_backend('qasm_simulator')
    if v: print('done')
    if v: print(f'Running job .. ', end='', flush=True)
    job = execute(circuit, simulator, shots=s)
    result = job.result()
    if v: print('done')
    return result.get_counts(circuit)

def check_valid(counts, shots, f_type):
    n = len(list(counts.keys())[0])
    if f_type == oracle.DJ.CONSTANT:
        return '0'*n in counts and counts['0'*n] == shots
    else:
        return '0'*n not in counts or counts['0'.n] != shots

parser = argparse.ArgumentParser(description='CS239 - Spring 20 - Deustch-Josza on Qiskit', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.set_defaults(reload=False, balanced=False, verbose=False)
parser.add_argument("--num", "-n", type=int, default=2, help="Set size of input string")
parser.add_argument("--shots", "-s", type=int, default=100, help="Set num of shots")
parser.add_argument("--reload", "-r", action="store_true", help='Reload new U_f matrix')
parser.add_argument("--balanced", "-b", action="store_true", help='Set whether f(x) is balanced or constant')
parser.add_argument("--verbose", "-v", action="store_true", help='Print out measured bits and steps')
args = parser.parse_args()

# Assign local variables to args and intialize DJ object
n = args.num
s = args.shots
r = args.reload
b = args.balanced
f_type = oracle.DJ.BALANCED if args.balanced else oracle.DJ.CONSTANT
v = args.verbose

print("=======================================================", flush=True)
print(f"Testing Deutsch-Josza Algorithm on {'Balanced' if b else 'Constant'} Function", flush=True)
if v:
    print(f"\n   Running with bit string of size n = {n}", flush=True)
    print(f"                   number of shots s = {s}", flush=True)
    print(f"                   reload U_f matrix = {r}", flush=True)
print("=======================================================\n", flush=True)

start = time.time()
circuit = generate_circuit(n, f_type, r, v)
counts = run_circuit(circuit, s)
end = time.time()
if v: print(f'\nCounts: {counts}\n')
ret = check_valid(counts, s, f_type)
print(f"Deutsch-Josza {'completed successfully!' if ret else 'failed...'}\n", flush=True)
print(f'(Took {end - start:.2f} s to complete.)', flush=True)

# Store times
TIMES_FILE = 'times/dj.csv'

with open(TIMES_FILE, 'r') as file:
    times = file.readlines()

lineno = (2*n + (0 if b else 1)) - 1
line=times[lineno].split(',')
line[2] = f'{end - start:.4f}\n'
times[lineno] = ','.join(line)

with open(TIMES_FILE, 'w') as file:
    file.writelines(times)
