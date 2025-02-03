""" test arithmetic on superposed input
"""
from qiskit_aer import Aer
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import transpile

import crsq_arithmetic as ari

def run_and_get_histogram(qc: QuantumCircuit) -> dict:
    """ run a simulation and return counts
    """
    sim = Aer.get_backend('aer_simulator')
    result = sim.run(transpile(qc, sim)).result()
    counts = result.get_counts()
    return counts


def adder_test(n: int):
    """ build a circuit and run a simulation
    """
    ar = QuantumRegister(n, name='a')
    br = QuantumRegister(n, name='b')
    bcr = QuantumRegister(n, name='bc')  # copy of input br.
    cr = QuantumRegister(n, name='c')
    car = ClassicalRegister(n, name="ca")
    cbr = ClassicalRegister(n, name="cb")
    cbcr = ClassicalRegister(n, name="cbc")
    qc = QuantumCircuit(ar, br, bcr, cr, cbr, car, cbcr)

    for k in range(n):
        qc.h(ar[k])
        qc.h(br[k])
        qc.cx(br[k], bcr[k])
    ari.signed_adder(qc, ar, br, cr)
    qc.measure(ar, car)
    qc.measure(bcr, cbcr)
    qc.measure(br, cbr)

    counts = run_and_get_histogram(qc)
    for s in sorted(counts):
        [a, b, c] = map(lambda t: int(t, 2), s.split(' '))
        if ((a + b - c) % (1 << n) == 0):
            print(s, "OK")
        else:
            print(s, "FAIL")

#    print(counts)


if __name__ == '__main__':
    adder_test(4)
