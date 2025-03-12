from qiskit_aer import AerSimulator
from qiskit.circuit.library import RealAmplitudes
from qiskit.circuit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import Session, SamplerV2 as Sampler, QiskitRuntimeService


# Setup 
qreg_q = QuantumRegister(3, 'q')
creg_c = ClassicalRegister(5, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

# Alice
circuit.reset(qreg_q[0])
circuit.h(qreg_q[0])
circuit.measure(qreg_q[0], creg_c[0])

circuit.reset(qreg_q[0])
circuit.h(qreg_q[0])
circuit.measure(qreg_q[0], creg_c[1])

if creg_c[0] == 1:
    circuit.x(qreg_q[0])

if creg_c[1] == 1:
    circuit.h(qreg_q[0])

# Spy
circuit.swap(qreg_q[0], qreg_q[1])
circuit.h(qreg_q[1])
circuit.measure(qreg_q[1], creg_c[2])

circuit.reset(qreg_q[1])
circuit.x(qreg_q[1])
circuit.h(qreg_q[1])

# Bob
circuit.reset(qreg_q[2])
circuit.h(qreg_q[2])
circuit.measure(qreg_q[2], creg_c[3])

circuit.swap(qreg_q[1], qreg_q[2])
if creg_c[3] == 1:
    circuit.h(qreg_q[2])

circuit.measure(qreg_q[2], creg_c[4])

### Run
aer_sim = AerSimulator()
pm = generate_preset_pass_manager(backend=aer_sim, optimization_level=1)
isa_qc = pm.run(circuit)
with Session(backend=aer_sim) as session:
    sampler = Sampler()
    result = sampler.run([isa_qc]).result()

print(result)
if creg_c[3] == creg_c[1]: 
    print("Valid" if creg_c[4] == creg_c[0] else "SPY!!!")
else:
    print("Valid")
