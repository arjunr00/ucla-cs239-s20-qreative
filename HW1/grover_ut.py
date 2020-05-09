import numpy as np
import os
import oracle

# Unit Test Functions

def is_unitary(m):
    # https://stackoverflow.com/a/34997613
    return np.allclose(np.eye(len(m)), m.dot(m.T.conj()))

def unit_tests(n):
    if not os.path.exists('uf'):
        os.mkdir('uf')
    if not os.path.exists('uf/grover'):
        os.mkdir('uf/grover')
    SAVEDIR = 'uf/grover/'
    FILEPATH = f'{SAVEDIR}grover{str(n)}.npy'
    FPATH = f'{SAVEDIR}f_dict.npy'

    if not os.path.exists(FILEPATH):
        mapping = oracle.init_bit_mapping(n, algo=oracle.Algos.GROVER)
        U_f  = oracle.gen_matrix(mapping, n, 1)

        if os.path.exists(FPATH):
            f_dict = np.load(FPATH, allow_pickle=True).item()
        else:
            f_dict = {}

        f_dict[n] = mapping
        np.save(FPATH, f_dict, allow_pickle=True)
    else:
        U_f = np.load(FILEPATH)

    assert is_unitary(U_f)
    if not os.path.exists(FILEPATH):
        np.save(FILEPATH, U_f)

for n in range (1, 10):
    unit_tests(n)
