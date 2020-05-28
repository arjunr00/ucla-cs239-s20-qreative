import numpy as np
import os
import oracle
from qiskit.quantum_info.operators import Operator

##################################
###       SIMON UNIT TEST      ###
##################################

SAVEDIR = 'uf/simon/'
SLIST   = 's_list'

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

def unit_test(n):
    if not os.path.exists('uf/simon'):
        os.makedirs('uf/simon')

    if not os.path.exists(f'{SAVEDIR}simon{str(n)}.npy'):
        print(f'Generating bit mapping for {n}-qubit Simon .. ', end='', flush=True)
        mapping = oracle.init_bit_mapping(n, algo=oracle.Algos.SIMON)
        print('done')

        print(f'Generating s value for newly generated {n}-bit mapping Simon .. ', end='', flush=True)
        s = get_s(mapping)
        print('done')

        print(f'Checking validity of s value .. ', end='', flush=True)
        assert is_valid(s, mapping)
        print('done')

        if os.path.exists(f'{SAVEDIR}{SLIST}.npy'):
            print(f'Loading s_list for Simon from {SAVEDIR}{SLIST}.npy .. ', end='', flush=True)
            s_list = np.load(f'{SAVEDIR}{SLIST}.npy', allow_pickle=True).item()
            print('done')
        else:
            s_list={}
        s_list[n] = s

        print(f'Saving s_list for Simon to {SAVEDIR}{SLIST}.npy .. ', end='', flush=True)
        np.save(f'{SAVEDIR}{SLIST}.npy', s_list, allow_pickle=True)
        print('done')

        print(f'Generating oracle matrix for {n}-qubit Simon .. ', end='', flush=True)
        U_f = oracle.gen_matrix(mapping, n, n)
        print('done')
    else:
        print(f'Loading U_f for {n}-qubit Simon from {SAVEDIR}simon{str(n)}.npy .. ', end='', flush=True)
        U_f = Operator(np.load(f'{SAVEDIR}simon{str(n)}.npy'))   
        print("done")

    assert U_f.is_unitary()
    if not os.path.exists(f'{SAVEDIR}simon{str(n)}.npy'):
        print(f'Saving U_f for {n}-qubit Simon from {SAVEDIR}simon{str(n)}.npy .. ', end='', flush=True)
        np.save(f'{SAVEDIR}simon{str(n)}.npy', U_f.data)
        print("done")

for n in range(1, 7):
    unit_test(n)