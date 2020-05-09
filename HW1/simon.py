import numpy as np
import sympy as sp
import time
import argparse
import oracle

from pyquil import Program, get_qc
from pyquil.quil import DefGate
from pyquil.gates import H
from pyquil.latex import *

def getUf(n, reload):
    if not reload:
        path = f'uf/simon/simon{n}.npy'
        U_f = np.load(path)
    else:
        U_f = oracle.gen_matrix(
            oracle.init_bit_mapping(n, algo=oracle.Algos.SIMON),
            n, n
        )
    
    return U_f

def check_lin_indep(ys):
    ys_strs = ["".join(str(b) for b in y_arr) for y_arr in ys]
    n = len(ys_strs[0])
    return ('0' * n) not in ys_strs and len(ys_strs) == len(set(ys_strs))

def check_valid(ys, s):
    zero = [0] * len(ys[0])
    ys.append(zero)
    Mys = sp.Matrix(ys)
    Z = sp.Matrix(zero)

    s_elems = sp.symbols([f's{i}' for i in range(len(zero))])
    soln = sp.linsolve((Mys, Z), s_elems).subs([(si, 1) for si in s_elems])

    solved_s_arr = [si % 2 for si in list(list(soln)[0])]
    solved_s = ''.join(str(si) for si in solved_s_arr)
    
    return solved_s == s

def qc_program(n, m, reload, verbose):
    # Simon's algorithm uses (n - 1) * 4m iterations
    t = (n-1) * (4*m)
    SAVEDIR = 'uf/simon/'
    SPATH = 's_dict.npy'
    s = np.load(SAVEDIR + SPATH, allow_pickle=True).item()[n]

    U_f_def = DefGate('U_f', getUf(n, reload))
    U_f = U_f_def.get_constructor()

    qc = get_qc(f'{str(2*n)}q-qvm')
    qc.compiler.client.timeout = 1000000

    p = Program()
    p += U_f_def
    p += (H(i) for i in range(n))
    p += U_f(*(tuple(range(2*n))))
    p += (H(i) for i in range(n))

    result = qc.run_and_measure(p, trials=t)
    if verbose:
        print('====================================')
        print('Measured Qubit State Across Trials:')
        for i in range(n):
            print(f'    {result[i]}')
        print('====================================\n')

    if verbose:
        print('====================================')
        print('Measured y values:')

    for i in range(4*m):
        if verbose:
            print(f'    Trial {i+1}:')

        ys=[]
        for j in range((n-1)*i, (n-1)*(i+1)):
            measured = [result[q][j] for q in range(n)]
            y = "".join(str(b) for b in measured)
            ys.append(measured)
            if verbose:
                print(f'        y_{j - (n-1)*i} = {y}')
        if check_lin_indep(ys):
            if verbose:
                print(f'Found linearly independent ys!\nChecking if they solve to s correctly...')
                print('====================================\n')
            return check_valid(ys, s)

    if verbose:
        print('====================================\n')

    return None

parser = argparse.ArgumentParser(description='CS239 - Spring 20 - Simon', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.set_defaults(reload=False, verbose=False)
parser.add_argument("--num", "-n", type=int, default=3, help="Set length of input bitstring")
parser.add_argument("--trials", "-t", type=int, default=1, help="Set number of times to run the entire algorithm (each time calls U_f (n-1) times)")
parser.add_argument("--reload", "-r", action="store_true", help='Reload new U_f matrix')
parser.add_argument("--verbose", "-v", action="store_true", help='Print out measured bits and steps')
args = parser.parse_args()

if __name__ == '__main__':
    n = args.num
    m = args.trials
    r = args.reload
    v = args.verbose

    print('=======================================================')
    print('Testing Simon\'s Algorithm')
    if v:
        print(f'\n   Running with bit string of size n = {n},')
        print(f'                  number of trials m = {m},')
        print(f'                   reload U_f matrix = {r}')
    print('=======================================================\n')

    start = time.time()
    ret = qc_program(n, m, r, v)
    end = time.time()
    if ret is None:
        ret_str = "Indeterminate... (Try a larger m with the --trials option?)"
    elif ret is True:
        ret_str = "Success!"
    else:
        ret_str = "Fail :("
    print(f'Simon\'s Algorithm: {ret_str}')
    print(f'(Took {end - start:.2f} s to complete.)')