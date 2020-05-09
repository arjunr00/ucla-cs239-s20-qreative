import numpy as np
import os
import oracle

# Unit Test Functions

def is_unitary(m):
    # https://stackoverflow.com/a/34997613
    return np.allclose(np.eye(len(m)), m.dot(m.T.conj()))

def unit_tests(n):
    print(f'Testing n = {str(n)}')

    if not os.path.exists('uf'):
        os.mkdir('uf')
    if not os.path.exists('uf/grover'):
        os.mkdir('uf/grover')
    SAVEPATH = 'uf/grover/'
    FILEPATH = f'{SAVEPATH}grover{str(n)}.npy'

    if not os.path.exists(FILEPATH):
        mapping = oracle.init_bit_mapping(n, algo=oracle.Algos.GROVER)
        print(mapping)
        U_f  = oracle.gen_matrix(mapping, n, 1)
    else:
        U_f = np.load(FILEPATH)

    assert is_unitary(U_f)
    if not os.path.exists(FILEPATH):
        np.save(FILEPATH, U_f)

    print(f'Finished n = {str(n)}')

for n in range (1, 10):
    unit_tests(n)
