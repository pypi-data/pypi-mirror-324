""" arithmetic operator test for pytest
"""
from qiskit import QuantumCircuit, QuantumRegister

import crsq_arithmetic as ari
import crsq_arithmetic.test_tools as test_tools

def do_subtract(aval, bval, n, use_bit_gates, use_gate_version):
    """ Test adding two 3bit unsinged integers
       aval, bval : result = bval - aval
       n : bit size of the registers
    """
    ar = QuantumRegister(n, name='a')
    br = QuantumRegister(n+1, name='b')
    cr = QuantumRegister(n-1, name='c')
    qc = QuantumCircuit(ar, br, cr)

    ari.set_value(qc, ar, aval)
    ari.set_value(qc, br, bval)

    if use_gate_version:
        qc.append(ari.unsigned_subtractor_gate(n, use_gates=use_bit_gates), ar[:]+br[:]+cr[:])
    else:
        ari.unsigned_subtractor(qc, ar, br, cr, use_gates=use_bit_gates)

    qc.save_statevector()

    astr = bin((1 << n) + aval)[-n:]
    bstr = bin((1 << n+1)+ bval - aval)[-(n+1):]
    cstr = "0"*(n-1)
    expected = cstr + bstr + astr

    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_unsigned_subtractor():
    """ run unsigned_subtractor for positive numbers
    """
    print("Unsigned int subtractor test")
    for use_gate_version in [False, True]:
        for use_bit_gates in [False, True]:
            print(f" gate version: {use_gate_version}  bit gates: {use_bit_gates}")
            for n in range(2, 4):
                s = 1 << n
                for aa in range(s):
                    for bb in range(s):
                        cc = aa + bb
                        do_subtract(aa, cc, n, use_bit_gates, use_gate_version)


def do_subtractv(aval, bval, m, n, use_bit_gates, use_gate_version):
    """ Test adding two 3bit unsinged integers
       aval, bval : result = bval - aval
       m : bit size of ar
       n : bit size of br
    """
    ar = QuantumRegister(m, name='a')
    br = QuantumRegister(n+1, name='b')
    cr = QuantumRegister(n-1, name='c')
    qc = QuantumCircuit(ar, br, cr)

    ari.set_value(qc, ar, aval)
    ari.set_value(qc, br, bval)

    # no use_gates option
    if use_gate_version:
        qc.append(ari.unsigned_subtractorv_gate(m, n, use_gates=use_bit_gates),
                  ar[:]+br[:]+cr[:])
    else:
        ari.unsigned_subtractorv(qc, ar, br, cr, use_gates=use_bit_gates)

    qc.save_statevector()

    astr = bin((1 << m) + aval)[-m:]
    bstr = bin((1 << n+1)+ bval - aval)[-(n+1):]
    cstr = "0"*(n-1)
    expected = cstr + bstr + astr

    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_unsigned_subtractorv():
    """ run unsigned_subtractor for positive numbers
    """
    print("Unsigned int subtractor for mixed bit length test")
    for use_gate_version in [False, True]:
        for use_bit_gates in [False, True]:
            print(f" gate version: {use_gate_version}  bit gates: {use_bit_gates}")
            for n in range(2, 4):
                t = 1 << n
                for m in range(1, n+1):
                    s = 1 << m
                    print(f"  m: {m}  n: {n}")
                    for aa in range(s):
                        for bb in range(t):
                            cc = aa + bb
                            do_subtractv(aa, cc, m, n, use_bit_gates, use_gate_version)



if __name__ == '__main__':
    test_unsigned_subtractor()
    test_unsigned_subtractorv()
