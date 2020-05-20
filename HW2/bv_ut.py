from qiskit.quantum_info.operators import Operator

import numpy as np
import os
import itertools

import oracle

# Unit Test Functions

def unit_tests(n):
    if not os.path.exists('uf/bv'):
        os.makedirs('uf/bv')

    SAVEPATH = 'uf/bv/'
    FILEPATH = f'bv{n}'
    APATH = 'a_dict'
    BPATH = 'b_dict'

    if not os.path.exists(f'{SAVEPATH}{FILEPATH}.npy'):
        if os.path.exists(f'{SAVEPATH}{APATH}.npy'):
            a_list = np.load(f'{SAVEPATH}{APATH}.npy', allow_pickle=True).item()
        else:
            a_list = {}

        if os.path.exists(f'{SAVEPATH}{BPATH}.npy'):
            b_list = np.load(f'{SAVEPATH}{BPATH}.npy', allow_pickle=True).item()
        else:
            b_list = {}

        a = a_list[n] if n in a_list.keys() else np.random.randint(low=0, high=2, size=n)
        b = b_list[n] if n in b_list.keys() else np.random.randint(low=0, high=2)
        a_list[n] = a
        b_list[n] = b
        np.save(f'{SAVEPATH}{APATH}.npy', a_list, allow_pickle=True)
        np.save(f'{SAVEPATH}{BPATH}.npy', b_list, allow_pickle=True)

        print(f'Generating bit mapping for {n}-qubit BV with a={"".join(str(i) for i in a)} and b={b} .. ', end='', flush=True)
        mapping = oracle.init_bit_mapping(n, algo=oracle.Algos.BV, func=(a,b))
        print('done')

        print(f'Generating U_f from bit mapping .. ', end='', flush=True)
        U_f = oracle.gen_matrix(mapping, n, 1)
        print('done')
    else:
        print(f'Loading U_f for {n}-qubit BV from {SAVEPATH}{FILEPATH}.npy .. ', end='', flush=True)
        U_f = Operator(np.load(f'{SAVEPATH}{FILEPATH}.npy'))
        print('done')

    assert U_f.is_unitary()
    if not os.path.exists(f'{SAVEPATH}{FILEPATH}.npy'):
        print(f'Saving U_f for {n}-qubit BV to {SAVEPATH}{FILEPATH}.npy .. ', end='', flush=True)
        np.save(f'{SAVEPATH}{FILEPATH}', U_f.data)
        print('done')

    print('')

for n in range(1,10):
    unit_tests(n)
