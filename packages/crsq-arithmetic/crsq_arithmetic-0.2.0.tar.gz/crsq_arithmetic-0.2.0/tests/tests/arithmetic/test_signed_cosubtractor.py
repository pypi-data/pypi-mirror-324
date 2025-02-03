""" Test const subtractor
"""
from qiskit.circuit import QuantumCircuit, QuantumRegister

import crsq_arithmetic as ari
import crsq_arithmetic.test_tools as test_tools

def build_signed_cosubtractor_circ_for(n: int, y: int, b: int, use_bit_gates: bool, use_gate_version: bool):
    """ build test circuit for signed_cosubtractor"""
    br = QuantumRegister(n, "b")
    cr = QuantumRegister(n-1, "cy")
    qc: QuantumCircuit = QuantumCircuit(br, cr)
    ari.set_value(qc, br, b)
    if use_gate_version:
        qc.append(ari.signed_cosubtractor_gate(n, y, use_gates=use_bit_gates), br[:] + cr[:])
    else:
        ari.signed_cosubtractor(qc, y, br, cr, use_gates=use_bit_gates)
    return qc

def do_signed_cosubtractor_for(n: int, y: int, b: int, verbose: bool, use_bit_gates: bool, use_gate_version: bool):
    """ test for one combination of y and b
    """
    qc = build_signed_cosubtractor_circ_for(n, y, b, use_bit_gates, use_gate_version)
    qc.save_statevector()
    ##
    cbits = "0" * (n-1)
    mask = (1<<n) - 1
    bbits = (bin((1<<n) + ((b-y) & mask)))[-n:]
    exp = {
        cbits+bbits : 1
    }
    if verbose:
        print(f" testing use_gate = {ug} y = {y}, b = {b}, b-y = {b-y}")
    test_tools.run_circuit_and_check(qc, exp)


def test_signed_cosubtractor(verbose: bool = False):
    """ test signed_cosubtractor
    """
    n = 4  # bits
    N = 2**n
    H = N // 2
    for use_gate_version in [False, True]:
        for use_bit_gates in [False, True]:
            for y in range(N):
                for b in range(N):
                    do_signed_cosubtractor_for(n, y - H, b - H, verbose, use_bit_gates, use_gate_version)

if __name__ == '__main__':
    test_signed_cosubtractor(True)
