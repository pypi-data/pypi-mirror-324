""" arithmetic operator test (signed int subtracter)
"""
from qiskit import QuantumCircuit, QuantumRegister

import crsq_arithmetic as ari
import crsq_arithmetic.test_tools as test_tools

def build_subtractor_with_values(aval, bval, n, use_bit_gates: bool, use_gate_version: bool):
    """ build an n bit subtracter circuit
    """
    ar = QuantumRegister(n, name='a')
    br = QuantumRegister(n, name='b')
    cr = QuantumRegister(n-1, name='c')
    qc = QuantumCircuit(ar, br, cr)

    ari.set_value(qc, ar, aval)
    ari.set_value(qc, br, bval)

    if use_gate_version:
        qc.append(ari.signed_subtractor_gate(n, use_gates=use_bit_gates), ar[:]+br[:]+cr[:])
    else:
        ari.signed_subtractor(qc, ar, br, cr, use_gates=use_bit_gates)

    qc.save_statevector()
    return qc


def do_sub(aval, bval, n, use_bit_gates, use_gate_version):
    """ Test adding two n bit unsinged integers
    """
    qc = build_subtractor_with_values(aval, bval, n, use_bit_gates, use_gate_version)

    astr = bin((1 << n) + aval)[-n:]
    bstr = bin((1 << (n+1)) + bval - aval)[-n:]
    cstr = "0"*(n-1)
    expected = cstr + bstr + astr

    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_signed_subtractor():
    """ test subtracter for all possible 3bit inputs.
    """
    print("Signed int subtractor test")
    for use_gate_version in [False, True]:
        for use_bit_gates in [False, True]:
            print(f" gate version: {use_gate_version}  bit gates: {use_bit_gates}")
            for n in (3, 5):
                s = 1 << n
                hs = 1 << n - 1
                for b in range(s):
                    for a in range(s):
                        do_sub(a-hs, b-hs, n, use_bit_gates, use_gate_version)

def build_signed_subtractorv_with_values(aval, bval, m, n, use_bit_gates: bool, use_gate_version: bool):
    """ build an n bit signed adder circuit
    """
    ar = QuantumRegister(m, name='a')
    br = QuantumRegister(n, name='b')
    cr = QuantumRegister(n-1, name='c')
    qc = QuantumCircuit(ar, br, cr)

    ari.set_value(qc, ar, aval)
    ari.set_value(qc, br, bval)

    if use_gate_version:
        qc.append(ari.signed_subtractorv_gate(m, n, use_gates=use_bit_gates), ar[:] + br[:] + cr[:])
    else:
        ari.signed_subtractorv(qc, ar, br, cr, use_gates=use_bit_gates)
    qc.save_statevector()
    return qc


def do_ssubv(aval, bval, m, n, use_bit_gates: bool, use_gate_version: bool):
    """ Test subtracting m-bit and n-bit signed integers
    """
    qc = build_signed_subtractorv_with_values(aval, bval, m, n, use_bit_gates, use_gate_version)
    astr = bin((1 << m+1) + aval)[-m:]
    bstr = bin((1 << n+1) - aval + bval)[-n:]
    cstr = "0"*(n-1)
    expected = cstr + bstr + astr
    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_signed_subtractorv():
    """ test adder for all possible m-bit and n-bit inputs.
    """
    n = 4
    t = 1 << n
    ht = t >> 1
    print("Signed int subtractorv test")
    for use_gate_version in [False, True]:
        for use_bit_gates in [False, True]:
            print(f" gate version: {use_gate_version}  bit gates: {use_bit_gates}")
            for m in range(1, n+1):
                s = 1 << m
                hs = s >> 1
                print(f"  m: {m}  n: {n}")
                for a in range(s):
                    for b in range(t):
                        do_ssubv(a-hs, b-ht, m, n, use_bit_gates, use_gate_version)


if __name__ == '__main__':
    test_signed_subtractor()
    test_signed_subtractorv()
    
