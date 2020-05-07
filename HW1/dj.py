import numpy as np
import itertools
import oracle

# Unit Test Functions

def is_bal_or_const(m, balanced):
    if not balanced:
        x = next(iter(m.values()))
        return all(val == x for val in m.values())
    else:
        val0 = sum(value == '0' for value in m.values())
        val1 = sum(value == '1' for value in m.values())
        return val0 == val1 and val0+val1 == len(m.values())

def is_unitary(m):
    return np.allclose(np.eye(len(m)), m.dot(m.T.conj()))

def unit_tests(n):
    const_mapping = oracle.init_bit_mapping(n, dj=True, balanced=False)
    assert is_bal_or_const(const_mapping, False)

    balanced_mapping = oracle.init_bit_mapping(n, dj=True, balanced=True)
    assert is_bal_or_const(balanced_mapping, True)

    U_const_f = oracle.gen_matrix(const_mapping, n, 1)
    assert is_unitary(U_const_f)

    U_bal_f = oracle.gen_matrix(balanced_mapping, n, 1)
    assert is_unitary(U_bal_f)

for n in range(5):
    unit_tests(n+1)