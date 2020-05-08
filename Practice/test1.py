from pyquil         import Program, get_qc
from pyquil.gates   import *
from pyquil.api     import local_forest_runtime

p = Program(H(0), CNOT(0,1))
p += X(1)

with local_forest_runtime():
    qc = get_qc('9q-square-qvm')
    result = qc.run_and_measure(p, trials=10)
    print(result[0])
    print(result[1])
    print(len(result))
