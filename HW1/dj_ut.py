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

def is_unitary(m):
    # https://stackoverflow.com/a/34997613
    return np.allclose(np.eye(len(m)), m.dot(m.T.conj()))

def unit_tests(n):
    if not os.path.exists('uf'):
        os.mkdir('uf') 
    if not os.path.exists('uf/dj'):
        os.mkdir('uf/dj')
    SAVEPATH = 'uf/dj/'
    CONSTPATH = 'const'+str(n)
    BALPATH = 'bal'+str(n)
    
    if not os.path.exists(SAVEPATH + CONSTPATH+'.npy'):
        const_mapping = oracle.init_bit_mapping(n, algo=oracle.Algos.DJ, func=oracle.DJ.CONSTANT)
        assert is_bal_or_const(const_mapping, oracle.DJ.CONSTANT)
        U_const_f = oracle.gen_matrix(const_mapping, n, 1)
    else:
        U_const_f = np.load(SAVEPATH + CONSTPATH +'.npy')

    if not os.path.exists(SAVEPATH + BALPATH+'.npy'):
        balanced_mapping = oracle.init_bit_mapping(n, algo=oracle.Algos.DJ, func=oracle.DJ.BALANCED)
        assert is_bal_or_const(balanced_mapping, oracle.DJ.BALANCED)
        U_bal_f = oracle.gen_matrix(balanced_mapping, n, 1)
    else:
        U_bal_f = np.load(SAVEPATH + BALPATH+'.npy')

    assert is_unitary(U_const_f)
    if not os.path.exists(SAVEPATH + CONSTPATH+'.npy'):
        np.save(SAVEPATH + CONSTPATH, U_const_f)

    assert is_unitary(U_bal_f)
    if not os.path.exists(SAVEPATH + BALPATH+'.npy'):
        np.save(SAVEPATH + BALPATH, U_bal_f)

for n in range(1,10):
    unit_tests(n)