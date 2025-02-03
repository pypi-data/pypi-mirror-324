""" arithmetic operator test (signed int adder)
"""
import math

from qiskit import QuantumCircuit, QuantumRegister

import crsq_arithmetic as ari
import crsq_arithmetic.test_tools as test_tools

def build_square_root_with_values(zval: int, n: int, use_bit_gates: bool, use_gate_version: bool):
    """ build an n bit square root circuit
        zval : value to take square root
        n : bit size of the register to use
    """
    wr = QuantumRegister(n+1, name='w')
    zr = QuantumRegister(n*2, name='z')
    rr = QuantumRegister(n, name='r')
    cr = QuantumRegister(n*2-1, name='cr')
    qc = QuantumCircuit(wr, zr, rr, cr)

    ari.set_value(qc, zr, zval)

    if use_gate_version:
        qc.append(ari.square_root_gate(n, use_gates=use_bit_gates), zr[:]+rr[:]+wr[:]+cr[:])
    else:
        ari.square_root(qc, zr, rr, wr, cr, use_gates=use_bit_gates)

    qc.save_statevector()
    return qc


def do_sqrt(zval, n, use_bit_gates: bool, use_gate_version: bool):
    """ Test square root of a 4bit unsinged integer
    """
    qc = build_square_root_with_values(zval, n, use_bit_gates, use_gate_version)

    r = int(math.sqrt(zval))
    z_out = zval - r*r
    w = r * 2

    zstr = bin((1 << (n*2)) + z_out)[-(n*2):]
    rstr = bin((1 << n) + r)[-n:]
    wstr = bin((1 << n+1) + w)[-(n+1):]
    cstr = "0"*(2*n-1)
    expected = cstr + rstr + zstr + wstr

    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)

def test_sqrt():
    """ test square root for all possible 6bit inputs.
    """

    print("int sqrt test. compute r,w such that z_in = r*r + z_out")
    for use_gate_version in [False, True]:
        for use_bit_gates in [False, True]:
            print(f" gate version: {use_gate_version}  bit gates: {use_bit_gates}")
            for n in [2,3]:
                s = (2**n-1)**2
                for z in range(s):
                    print(f" z: {z}")
                    do_sqrt(z, n, use_bit_gates, use_gate_version)


if __name__ == '__main__':
    test_sqrt()
