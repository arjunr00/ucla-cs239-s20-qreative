import numpy as np
import argparse
import matplotlib
import math
import os
import oracle
import time

from qiskit import QuantumCircuit, execute, Aer, IBMQ, assemble, transpile
from qiskit.visualization import plot_histogram
from qiskit.quantum_info.operators import Operator

from dotenv import load_dotenv

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
    success = 0
    total = 0
    for qubits, frequency in qubits.items():
        if verbose:
            print(f'    => f({qubits}) = {f[qubits]}\n')
        if f[qubits[::-1]] == '1':
            success += int(frequency)
        total += frequency
    if verbose:
        print(f'Number of Success: {success}')
        print(f'Number Total: {total}')
    return (success / total) > 0.5

def generate_circuit(n, reload, v):
    SAVEDIR = 'plots/'
    CIRCUIT_FILENAME = f'grover_{n}.pdf'
    N = 2**n
    sqrtN = math.sqrt(N)

    # For "very large" N, this is a good approximation
    k = math.floor((math.pi * sqrtN)/4)
    if v:
        print('====================================')
        # U+2248 is the Unicode encoding for approximately equal to
        # U+230A is the Unicode encoding for left floor
        # U+230B is the Unicode encoding for right floor
        # U+03C0 is the Unicode encoding for lowercase pi
        # U+221A is the Unicode encoding for sqrt
        # U+207f is the Unicode encoding for ^n
        print(f'[k \u2248 \u230a(\u03c0\u221aN)/4\u230b = {k}\t(N = 2\u207f = 2^{n})]\n')

    if (v): print('Getting Z_0 .. ', end='', flush=True)
    z0 = Operator(get_z0(n))
    if (v): print('done', flush=True)
    if (v): print('Getting Z_f .. ', end='', flush=True)
    zf = Operator(get_zf(n, reload, v))
    if (v): print('done', flush=True)

    if (v): print('Creating circuit .. ', end='', flush=True)
    # Intialize
    circuit = QuantumCircuit(n+1, n)
    circuit.x(n)
    circuit.h(range(n+1))
    
    # Loop
    for i in range(k):
        circuit.append(zf, range(n+1)[::-1])
        circuit.h(range(n))
        circuit.append(z0, range(n)[::-1])
        circuit.h(range(n))

    circuit.measure(range(n), range(n))

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

##################################
###          LOCAL             ###
##################################
def qc_program(n, reload, verbose):
    circuit = generate_circuit(n, reload, verbose)
    simulator = Aer.get_backend('qasm_simulator')

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

##################################
###           IMBQ             ###
##################################
def load_api_token():
  load_dotenv()
  API_TOKEN = os.getenv('API_TOKEN')
  IBMQ.save_account(API_TOKEN)

def run_on_ibmq(n, reload, verbose, draw=False, waitForResult=False, backend='ibmq_burlington'):
    print('Loading account .. ', end='', flush=True)
    provider = IBMQ.load_account()
    print('done')
    backend = getattr(provider.backends, backend)
    circuit = generate_circuit(n, reload, verbose)

    print('Transpiling .. ', end='')
    transpiled = transpile(circuit, backend)
    print('done')
    print('Assembling .. ', end='')
    qobj = assemble(transpiled, backend, shots=500)
    print('done')
    print(f'Sending to {backend} .. ', end='')
    job = backend.run(qobj)
    print('done')
    if waitForResult:
        print(f'Waiting for result .. ', end='', flush=True)
        delayed_result = backend.retrieve_job(job.job_id()).result()
        delayed_counts = delayed_result.get_counts()
        print('done')
        print(f'\nTotal counts: {delayed_counts}')
        return check_validity(n, delayed_counts, verbose)
    else:
        print(f'\nJob ID: {job.job_id()}')
        return False


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
    # ret = qc_program(n, r, v)
    ret = run_on_ibmq(n, r, v, waitForResult=True, backend="ibmq_qasm_simulator")
    end = time.time()

    if ret is True:
        ret_str = "Success!"
    else:
        ret_str = "Fail :("

    print(f'Grover\'s Algorithm: {ret_str}')
    print(f'(Took {end - start:.2f} s to complete.)')