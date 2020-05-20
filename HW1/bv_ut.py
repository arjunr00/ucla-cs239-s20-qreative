import numpy as np
import os
import itertools
import oracle

# Unit Test Functions

def is_correct(m, a):
    return True

def is_unitary(m):
    # https://stackoverflow.com/a/34997613
    return np.allclose(np.eye(len(m)), m.dot(m.T.conj()))

def unit_tests(n):
    if not os.path.exists('uf/bv'):
        os.makedirs('uf/bv')

    SAVEPATH = 'uf/bv/'
    FILEPATH = 'bv'+str(n)
    SPATH = 'a_dict'

    if not os.path.exists(SAVEPATH + FILEPATH+'.npy'):
        if os.path.exists(SAVEPATH + SPATH+'.npy'):
            a_list = np.load(SAVEPATH+ SPATH+'.npy', allow_pickle=True).item()
        else:
            a_list = {}
        a = a_list[n] if  n in a_list.keys() else np.random.randint(low=0, high=2, size=n)
        a_list[n] = a
        np.save(SAVEPATH + SPATH, a_list, allow_pickle=True)

        f_mapping = oracle.init_bit_mapping(n, algo=oracle.Algos.BV, func=(a,0))
        assert is_correct(f_mapping, a)

        U_f = oracle.gen_matrix(f_mapping, n, 1)
    else:
        U_f = np.load(SAVEPATH + FILEPATH +'.npy')

    assert is_unitary(U_f)

    if not os.path.exists(SAVEPATH + FILEPATH+'.npy'):
        np.save(SAVEPATH + FILEPATH, U_f)

for n in range(1,10):
    unit_tests(n)
