import numpy as np
import oracle

from pyquil import Program, get_qc
from pyquil.quil import DefGate
from pyquil.gates import H
from pyquil.latex import *

def getUf(n, reload):
    if not reload:
        path = f'uf/simon/simon{n}.npy'
        U_f = np.load(path)
    else:
        U_f = oracle.gen_matrix(
            oracle.init_bit_mapping(n, algo=oracle.Algos.SIMON, func=oracle.Simon.TWO_TO_ONE),
            n, n
        )
    
    return U_f

def check_valid(m_bits, s):
    # TODO: stub
    return True

def qc_program(n, t, reload):
    U_f_def = DefGate('U_f', getUf(n, reload))
    U_f = U_f_def.get_constructor()

    qc = get_qc('10q-qvm')
    qc.compiler.client.timeout = 1000000

    p = Program()
    p += U_f_def
    p += (H(i) for i in range(n))
    p += U_f(*(tuple(range(2*n))))
    p += (H(i) for i in range(n))

    result = qc.run_and_measure(p, trials=t)
    for i in range(n):
        print(result[i])

qc_program(3, 8, False)