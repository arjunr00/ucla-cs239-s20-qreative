print('Loading dependencies .. ', end='', flush=True)
import numpy as np
import sympy as sp
import time
import argparse
import os
import oracle

from qiskit import QuantumCircuit, execute, Aer, IBMQ, assemble, transpile
from qiskit.visualization import plot_histogram
from qiskit.quantum_info.operators import Operator
from qiskit.tools.monitor import job_monitor
from qiskit.providers.ibmq import least_busy
from qiskit.providers.ibmq.job.exceptions import IBMQJobFailureError
print('done\n', flush=True)

def get_s(mapping):
    print(mapping)
    y1 = y0 = list(mapping)[0]
    f_0 = mapping[y0]
    for y, f_x in mapping.items():
        if f_x == f_0 and y != y0:
            y1 = y
            break
    return y1

def is_valid(s, mapping):
    single_s = all(v == '0' for v in s)
    print(f's: {s}')
    for i in mapping:
        count = sum(f_x == mapping[i] for f_x in mapping.values())
        if (single_s and count != 1) or (not single_s and count != 2):
            return False
    return True

def getUf(n, reload):
    path = f'uf/simon/simon{n}.npy'
    SAVEDIR = 'uf/simon/'
    SLIST = 's_list.npy'

    if not reload and os.path.exists(path):
        U_f = np.load(path)
        s_list = np.load(SAVEDIR+SLIST, allow_pickle=True).item()
        s = s_list[n]
    else:
        SAVEDIR = 'uf/simon/'
        SLIST = 's_list.npy'

        mapping = oracle.init_bit_mapping(n, algo=oracle.Algos.SIMON)
        s = get_s(mapping)

        assert is_valid(s, mapping)

        if os.path.exists(SAVEDIR + SLIST):
            s_list = np.load(SAVEDIR + SLIST, allow_pickle=True).item()
        else:
            s_list = {}

        s_list[n] = s
        np.save(SAVEDIR + SLIST, s_list, allow_pickle=True)
        U_f = oracle.gen_matrix(mapping, n, n)

    return U_f, s

def is_lin_indep(potential_ys, n):
    if '0'*n in potential_ys:
        potential_ys.remove('0'*n)
    return len(potential_ys) == (n-1) and len(potential_ys) == len(set(potential_ys))

def check_validity(potential_ys, s):
    ys = [list(i) for i in potential_ys]
    zero = [0] * len(ys[0])
    ys.append(zero)
    Mys = sp.Matrix(ys)
    Z = sp.Matrix(zero)

    s_elems = sp.symbols([f's{i}' for i in range(len(zero))])
    soln = sp.linsolve((Mys, Z), s_elems).subs([(si, 1) for si in s_elems])

    solved_s_arr = [si % 2 for si in list(list(soln)[0])][::-1]
    solved_s = ''.join(str(si) for si in solved_s_arr)

    print(f'Simon says s = {solved_s}')

    if s is not None or s != '0' * len(s):
        return solved_s == s
    else:
        return True

def generate_circuit(n, t, reload, verbose):
    trials = (n-1) * (4*t)

    u_f, s = getUf(n,reload)
    U_f = Operator(u_f)

    circuit = QuantumCircuit(2*n, n)

    circuit.h(range(n))
    # circuit.append(U_f, range(2*n)[::-1])
    circuit.barrier()
    for i in range(n):
        circuit.cx(i, n+i)
        if s[i] == '1':
            circuit.x(n+i)
    circuit.barrier()
    for i in range(n):
        k = n+i
        while k == n+i:
            k = np.random.randint(low=n, high=2*n)
        circuit.swap(n+i, k)
    circuit.h(range(n))
    circuit.barrier()

    circuit.measure(range(0, n), range(n))
    circuit.measure(range(n, 2*n), range(n))

    return circuit, s

##################################
###          LOCAL             ###
##################################
def qc_program(n, t, reload, verbose):
    print('Generating circuit .. ', end='', flush=True)
    circuit = generate_circuit(n, t, reload, verbose)
    print('done')
    print(circuit[0])
    print(f's = {circuit[1]}', flush=True)
    simulator = Aer.get_backend('qasm_simulator')

    s = circuit[1]
    for i in range(4*t):
        job = execute(circuit[0], simulator, shots=(n-1))
        results = job.result().get_counts(circuit[0])
        if len(results.keys()) != n-1:
            continue
        if verbose:
            print(f'    Trial {i+1}:')

        potential_ys = []
        for index, y in enumerate(results.keys()):
            potential_ys.append(y)
            if verbose:
                print(f'        y_{index} = {y}')
        if is_lin_indep(potential_ys, n):
            if verbose:
                print(f'Checking if they solve to s correctly...')
                print('====================================\n')
            return check_validity(potential_ys, s)
    if verbose:
        print('====================================\n')
    return None

##################################
###           IMBQ             ###
##################################
def load_api_token():
    try:
        load_dotenv()
        API_TOKEN = os.getenv('API_TOKEN')
        IBMQ.save_account(API_TOKEN)
        provider = IBMQ.load_account()
        print(f'\nSuccessfully loaded API token for IBMQ\n')
        ibmq_flag = True
    except Exception as e:
        print(e)
        print(f'\nFailed to load API token for IBMQ. Running locally.')
        ibmq_flag = False

    return ibmq_flag

def run_on_ibmq(n, t, reload, verbose):
    print('Loading account .. ', end='', flush=True)
    provider = IBMQ.load_account()
    print('done')

    print('Choosing least busy device .. ', end='', flush=True)
    device = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= (2*n)+1 and not x.configuration().simulator and x.status().operational==True))
    print('done')
    print(f'Running on {device}')

    print('Generating circuit .. ', end='', flush=True)
    circuit = generate_circuit(n, t, reload, verbose)
    print('done')
    print(circuit[0])
    print(f's = {circuit[1]}', flush=True)


    print('Executing circuit .. ', end='', flush=True)
    try:
        job = execute(circuit[0], backend=device, shots=4*t*(n-1), optimization_level=3)
        job_monitor(job, interval = 1)
        results = job.result().get_counts(circuit[0])
    except IBMQJobFailureError:
        print(job.error_message())
        return None

    print(results)
    s = circuit[1]
    potential_ys = [k for k, _ in sorted(results.items(), key=lambda item: item[1])]
    print(potential_ys)
    if '0'*n in potential_ys:
        potential_ys.remove('0'*n)
    if len(potential_ys) < n-1:
        return None

    print(f'Found ys: {potential_ys}.\nChecking for linear independence .. ', end = '', flush=True)
    if not is_lin_indep(potential_ys, n):
        print('failed')
        return False
    print('done')
    if verbose:
        print(f'Checking if they solve to s correctly...')
        print('====================================\n')

    return check_validity(potential_ys, s)
    if verbose:
        print('====================================\n')

parser = argparse.ArgumentParser(description='CS239 - Spring 20 - Simon on Qiskit', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.set_defaults(reload=False, verbose=False)
parser.add_argument("--num", "-n", type=int, default=3, help="Set length of input bitstring")
parser.add_argument("--trials", "-t", type=int, default=1, help="Set number of times to run the entire algorithm (each time calls U_f (n-1) times)")
parser.add_argument("--reload", "-r", action="store_true", help='Reload new U_f matrix')
parser.add_argument("--verbose", "-v", action="store_true", help='Print out measured bits and steps')
args = parser.parse_args()

if __name__ == '__main__':
    n = args.num
    t = args.trials
    r = args.reload
    v = args.verbose

    print('=======================================================')
    print('Testing Simon\'s Algorithm')
    if v:
        print(f'\n   Running with bit string of size n = {n},')
        print(f'                  number of trials t = {t},')
        print(f'                   reload U_f matrix = {r}')
    print('=======================================================\n')

    start = time.time()
    #ret = qc_program(n, t, r, v)
    ret = run_on_ibmq(n, t, r, v)
    end = time.time()
    if ret is None:
        ret_str = "Indeterminate... (Try a larger t with the --trials option?)"
    elif ret is True:
        ret_str = "Success!"
    else:
        ret_str = "Fail :("
    print(f'Simon\'s Algorithm: {ret_str}')
    print(f'(Took {end - start:.2f} s to complete.)')

    # Store times
    TIMES_FILE = 'times/simon.csv'

    with open(TIMES_FILE, 'r') as file:
        times = file.readlines()

    lineno = n
    line=times[lineno].split(',')
    line[1] = f'{end - start:.4f}\n'
    times[lineno] = ','.join(line)

    with open(TIMES_FILE, 'w') as file:
        file.writelines(times)
