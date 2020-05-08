import numpy as np
import os
import itertools
import oracle

# Unit Test Functions

def is_correct(m):
    print(m)
    correct = False

    s = get_s(m)
    print(f's: {s}')

    for x in m:
        count = sum(val == m[x] for val in m.values())
        if (s == '0' * len(s) and count != 1) or \
           (s != '0' * len(s) and count != 2):
            return False

    return True

def get_s(m):
    xa = list(m)[0]
    xb = xa
    fa = m[xa]
    for x, fx in m.items():
        if fx == fa and x != xa:
            xb = x
            break
    return f'{int(xa, 2) ^ int(xb, 2):0{len(fa)}b}'

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
    SPATH = 's_dict'
    
    if not os.path.exists(SAVEDIR + FILEPATH+'.npy'):
        mapping = oracle.init_bit_mapping(n, algo=oracle.Algos.SIMON)
        assert is_correct(mapping)
        U_f = oracle.gen_matrix(mapping, n, n)

        s = get_s(mapping)
        if os.path.exists(SAVEDIR + SPATH+'.npy'):
            s_list = np.load(SAVEDIR + SPATH+'.npy', allow_pickle=True).item()
        else:
            s_list = {}

        s_list[n] = s
        np.save(SAVEDIR + SPATH, s_list, allow_pickle=True)
    else:
        U_f = np.load(SAVEDIR + FILEPATH +'.npy')

    assert is_unitary(U_f)
    if not os.path.exists(SAVEDIR + FILEPATH+'.npy'):
        np.save(SAVEDIR + FILEPATH, U_f)

for n in range(1,7):
    unit_tests(n)