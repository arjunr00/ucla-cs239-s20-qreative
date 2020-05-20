from qiskit import IBMQ, QuantumCircuit, execute, assemble, transpile
from dotenv import load_dotenv
import os

def load_api_token():
  load_dotenv()
  API_TOKEN = os.getenv('API_TOKEN')
  IBMQ.save_account(API_TOKEN)

def run_on_ibmq(ifDraw=False):
  provider = IBMQ.load_account()
  backend = provider.backends.ibmq_burlington
  circuit = define_circuit(ifDraw)

  transpiled = transpile(circuit, backend)
  qobj = assemble(transpiled, backend, shots=1000)
  job = backend.run(qobj)
  print(job.job_id())

def define_circuit(ifDraw):
  circuit = QuantumCircuit(2, 2)
  # Add a H gate on qubit 0
  circuit.h(0)
  # Add a CX (CNOT) gate on control qubit 0 and target qubit 1
  circuit.cx(0, 1)
  # Map the quantum measurement to the classical bits
  circuit.measure([0,1], [0,1])

  if ifDraw:
    print(circuit.draw('text'))
  return circuit

  
if __name__ == "__main__":
  # load_api_token()
  run_on_ibmq(ifDraw=True)