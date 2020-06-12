from qiskit.quantum_info.operators import Operator

import numpy as np
import os
import itertools

import oracle

# Unit Test Functions

def is_bal_or_const(m, f):
    if f is oracle.DJ.CONSTANT:
        x = next(iter(m.values()))
        return all(val == x for val in m.values())
    elif f is oracle.DJ.BALANCED:
        val0 = sum(value == '0' for value in m.values())
        val1 = sum(value == '1' for value in m.values())
        return val0 == val1 and val0+val1 == len(m.values())

def unit_tests(n):
    if not os.path.exists('uf'):
        os.mkdir('uf')
    if not os.path.exists('uf/dj'):
        os.mkdir('uf/dj')
    SAVEPATH = 'uf/dj/'
    CONSTPATH = f'const{n}'
    BALPATH = f'bal{n}'

    if not os.path.exists(f'{SAVEPATH}{CONSTPATH}.npy'):
        print(f'Generating bit mapping for {n}-qubit constant DJ .. ', end='', flush=True)
        const_mapping = oracle.init_bit_mapping(n, algo=oracle.Algos.DJ, func=oracle.DJ.CONSTANT)
        print('done')
        assert is_bal_or_const(const_mapping, oracle.DJ.CONSTANT)
        print(f'Generating U_f from bit mapping .. ', end='', flush=True)
        U_const_f = oracle.gen_matrix(const_mapping, n, 1)
        print('done')
    else:
        print(f'Loading U_f for {n}-qubit constant DJ from {SAVEPATH}{CONSTPATH}.npy .. ', end='', flush=True)
        U_const_f = Operator(np.load(f'{SAVEPATH}{CONSTPATH}.npy'))
        print('done')

    if not os.path.exists(f'{SAVEPATH}{BALPATH}.npy'):
        print(f'Generating bit mapping for {n}-qubit balanced DJ .. ', end='', flush=True)
        balanced_mapping = oracle.init_bit_mapping(n, algo=oracle.Algos.DJ, func=oracle.DJ.BALANCED)
        print('done')
        assert is_bal_or_const(balanced_mapping, oracle.DJ.BALANCED)
        print(f'Generating U_f from bit mapping .. ', end='', flush=True)
        U_bal_f = oracle.gen_matrix(balanced_mapping, n, 1)
        print('done')
    else:
        print(f'Loading U_f for {n}-qubit balanced DJ from {SAVEPATH}{BALPATH}.npy .. ', end='', flush=True)
        U_bal_f = Operator(np.load(f'{SAVEPATH}{BALPATH}.npy'))
        print('done')

    assert U_const_f.is_unitary()
    if not os.path.exists(f'{SAVEPATH}{CONSTPATH}.npy'):
        print(f'Saving U_f for {n}-qubit constant DJ to {SAVEPATH}{CONSTPATH}.npy .. ', end='', flush=True)
        np.save(SAVEPATH + CONSTPATH, U_const_f.data)
        print('done')

    assert U_bal_f.is_unitary()
    if not os.path.exists(f'{SAVEPATH}{BALPATH}.npy'):
        print(f'Saving U_f for {n}-qubit balanced DJ to {SAVEPATH}{BALPATH}.npy .. ', end='', flush=True)
        np.save(SAVEPATH + BALPATH, U_bal_f.data)
        print('done')

    print('')

for n in range(1,10):
    unit_tests(n)
