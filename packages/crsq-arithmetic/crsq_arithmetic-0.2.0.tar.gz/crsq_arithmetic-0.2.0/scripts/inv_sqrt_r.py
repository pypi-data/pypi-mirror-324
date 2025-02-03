import os, sys
import crsq_arithmetic as ari
import qiskit_aer
import qiskit

from qiskit.circuit import QuantumCircuit, QuantumRegister

n = 8
qr2 = QuantumRegister(n*2, 'r^2')
qsqr = QuantumRegister(n, 'sqrt')
qtmp = QuantumRegister(3*n+1, 'tmp')
qone = QuantumRegister(n, 'one')
qc = QuantumCircuit(qr2, qsqr, qtmp, qone)

qc.x(qone[n-1])
ari.square_root(qc, qr2, qsqr, qtmp[:n+1], qtmp[n+1:3*n])
ari.unsigned_divider(qc, qsqr, qtmp[0:n], qone, qtmp[n:2*n-1])

dirname="output/circuits"
os.makedirs(dirname, exist_ok=True)
# qc.draw(output='mpl', filename= dirname + "/inv_sqrt_by_gates", scale=0.6)

# transpile the circuit to count gates
print(qiskit_aer.AerSimulator().available_methods())
backend = qiskit_aer.AerSimulator(method='matrix_product_state')

transpiled = qiskit.transpile(qc, backend)

print(transpiled.count_ops())
