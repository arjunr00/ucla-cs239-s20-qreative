print('Loading dependencies .. ', end='', flush=True)
from qiskit import IBMQ, QuantumCircuit, execute, assemble, transpile
from dotenv import load_dotenv
import matplotlib
import os
print('done')

SAVEDIR = 'plots/'
CIRCUIT_FILENAME = 'circuit.png'

def load_api_token():
  load_dotenv()
  API_TOKEN = os.getenv('API_TOKEN')
  IBMQ.save_account(API_TOKEN)

def run_on_ibmq(draw=False, waitForResult=False, backend='ibmq_burlington'):
    print('Loading account .. ', end='', flush=True)
    provider = IBMQ.load_account()
    print('done')
    backend = getattr(provider.backends, backend)
    circuit = define_circuit(draw)

    print('Transpiling .. ', end='')
    transpiled = transpile(circuit, backend)
    print('done')
    print('Assembling .. ', end='')
    qobj = assemble(transpiled, backend, shots=1000)
    print('done')
    exit()
    print(f'Sending to {backend} .. ', end='')
    job = backend.run(qobj)
    print('done')
    if waitForResult:
        print(f'Waiting for result .. ', end='', flush=True)
        delayed_result = backend.retrieve_job(job.job_id()).result()
        delayed_counts = delayed_result.get_counts()
        print('done')
        print(f'\nTotal counts: {delayed_counts}')
    else:
        print(f'\nJob ID: {job.job_id()}')

def define_circuit(draw):
    print('Creating circuit .. ', end='')
    circuit = QuantumCircuit(2, 2)
    # Add a H gate on qubit 0
    circuit.h(0)
    # Add a CX (CNOT) gate on control qubit 0 and target qubit 1
    circuit.cx(0, 1)
    # Map the quantum measurement to the classical bits
    circuit.measure([0,1], [0,1])
    print('done\n')

    if draw:
        print('Circuit:')
        print(circuit.draw('text'))
        circuit.draw('mpl')
        print(f'Saving circuit to {CIRCUIT_FILENAME} .. ', end='')
        if not os.path.exists(SAVEDIR):
            os.mkdir(SAVEDIR)

        matplotlib.pyplot.savefig('plots/circuit.png')
        print('done\n')
    return circuit

if __name__ == '__main__':
  # load_api_token()
  run_on_ibmq(draw=True, waitForResult=True, backend='ibmq_london')
