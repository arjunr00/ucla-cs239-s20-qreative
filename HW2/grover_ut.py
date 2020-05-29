import numpy as np
import os
import oracle
from qiskit.quantum_info.operators import Operator

##################################
###      GROVER UNIT TEST      ###
##################################

SAVEDIR = 'uf/grover/'
FLIST   = 'f_list'

def unit_test(n):
    if not os.path.exists('uf/grover'):
        os.makedirs('uf/grover')

    if not os.path.exists(f'{SAVEDIR}grover{str(n)}.npy'):
        print(f'Generating bit mapping for {n}-qubit Grover .. ', end='', flush=True)
        mapping = oracle.init_bit_mapping(n, algo=oracle.Algos.GROVER)
        print('done')

        if os.path.exists(f'{SAVEDIR}{FLIST}.npy'):
            print(f'Loading f_list for Grover from {SAVEDIR}{FLIST}.npy .. ', end='', flush=True)
            f_list = np.load(f'{SAVEDIR}{FLIST}.npy', allow_pickle=True).item()
            print('done')
        else:
            f_list={}

        f_list[n] = mapping

        print(f'Saving f_list for Grover to {SAVEDIR}{FLIST}.npy .. ', end='', flush=True)
        np.save(f'{SAVEDIR}{FLIST}.npy', f_list, allow_pickle=True)
        print('done')

        print(f'Generating oracle matrix for {n}-qubit Grover .. ', end='', flush=True)
        U_f = oracle.gen_matrix(mapping, n, 1)
        print('done')
    else:
        print(f'Loading U_f for {n}-qubit Grover from {SAVEDIR}grover{str(n)}.npy .. ', end='', flush=True)
        U_f = Operator(np.load(f'{SAVEDIR}grover{str(n)}.npy'))   
        print("done")

    print(f'Check if U_f is unitary .. ', end='', flush=True)
    assert U_f.is_unitary()
    print('done')

    if not os.path.exists(f'{SAVEDIR}grover{str(n)}.npy'):
        print(f'Saving U_f for {n}-qubit Grover from {SAVEDIR}grover{str(n)}.npy .. ', end='', flush=True)
        np.save(f'{SAVEDIR}grover{str(n)}.npy', U_f.data)
        print("done")

for n in range(1, 10):
    unit_test(n)