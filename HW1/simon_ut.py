import numpy as np
import os
import itertools
import oracle

# Unit Test Functions

def is_correct(m):
    print(m)
    correct = False

    xa = list(m)[0]
    xb = ""
    fa = m[xa]
    for x, fx in m.items():
        if fx == fa and x != xa:
            xb = x
            break
    s = f'{int(xa, 2) ^ int(xb, 2):0{len(fa)}b}'
    print(s)

    for x in m:
        count = sum(val == m[x] for val in m.values())
        if (s == '0' * len(s) and count != 1) or count != 2:
            return False

    return True

def is_unitary(m):
    # https://stackoverflow.com/a/34997613
    return np.allclose(np.eye(len(m)), m.dot(m.T.conj()))

def unit_tests(n):
    if not os.path.exists('uf'):
        os.mkdir('uf') 
    if not os.path.exists('uf/simon'):
        os.mkdir('uf/simon')
    SAVEDIR = 'uf/simon/'
    FILEPATH = 'simon'+str(n)
    
    if not os.path.exists(SAVEDIR + FILEPATH+'.npy'):
        mapping = oracle.init_bit_mapping(n, algo=oracle.Algos.SIMON, func=oracle.Simon.TWO_TO_ONE)
        assert is_correct(mapping)
        U_f = oracle.gen_matrix(mapping, n, n)
    else:
        U_f = np.load(SAVEDIR + FILEPATH +'.npy')

    assert is_unitary(U_f)
    if not os.path.exists(SAVEDIR + FILEPATH+'.npy'):
        np.save(SAVEDIR + FILEPATH, U_f)

# for n in range(1,10):
#     unit_tests(n)
unit_tests(3)