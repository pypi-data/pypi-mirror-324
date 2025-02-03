""" arithmetic operator test for pytest
"""
from qiskit import QuantumCircuit, QuantumRegister

import crsq_arithmetic as ari
import crsq_arithmetic.test_tools as test_tools

def do_add(aval, bval, n, use_bit_gates, use_gate_version):
    """ Test adding two 3bit unsinged integers
       aval, bval : values to add
       n : bit size of the registers
    """
    ar = QuantumRegister(n, name='a')
    br = QuantumRegister(n+1, name='b')
    cr = QuantumRegister(n-1, name='c')
    qc = QuantumCircuit(ar, br, cr)

    ari.set_value(qc, ar, aval)
    ari.set_value(qc, br, bval)

    if use_gate_version:
        qc.append(ari.unsigned_adder_gate(n, use_gates=use_bit_gates),
                  ar[:]+br[:]+cr[:])
    else:
        ari.unsigned_adder(qc, ar, br, cr, use_gates=use_bit_gates)

    qc.save_statevector()

    astr = bin((1 << n) + aval)[-n:]
    bstr = bin((1 << n+1)+aval+bval)[-(n+1):]
    cstr = "0"*(n-1)
    expected = cstr + bstr + astr

    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_unsigned_adder():
    """ run unsigned_adder for positive numbers
    """
    print("Unsigned int adder test")
    for use_gate_version in [False, True]:
        for use_bit_gates in [False, True]:
            print(f" gate version: {use_gate_version}  bit gates: {use_bit_gates}")
            for n in range(2, 4):
                s = 1 << n
                for aa in range(s):
                    for bb in range(s):
                        do_add(aa, bb, n, use_bit_gates, use_gate_version)


def do_addv(aval, bval, m, n, use_bit_gates, use_gate_version):
    """ Test adding two 3bit unsinged integers
       aval, bval : values to add
       n : bit size of the registers
    """
    ar = QuantumRegister(m, name='a')
    br = QuantumRegister(n+1, name='b')
    cr = QuantumRegister(n-1, name='c')
    qc = QuantumCircuit(ar, br, cr)

    ari.set_value(qc, ar, aval)
    ari.set_value(qc, br, bval)

    if use_gate_version:
        qc.append(ari.unsigned_adderv_gate(m, n, use_gates=use_bit_gates),
                  ar[:] + br[:] + cr[:])
    else:
        ari.unsigned_adderv(qc, ar, br, cr, use_gates=use_bit_gates)

    qc.save_statevector()

    astr = bin((1 << m) + aval)[-m:]
    bstr = bin((1 << n+1) + aval + bval)[-(n+1):]
    cstr = "0"*(n-1)
    expected = cstr + bstr + astr

    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_unsigned_adderv():
    """ run unsigned_adder for positive numbers
    """
    print("Unsigned int with unmatched bit length adder test")
    for use_gate_version in [False, True]:
        for use_bit_gates in [False, True]:
            print(f" gate version: {use_gate_version}  bit gates: {use_bit_gates}")
            for n in range(1, 4):
                t = 1 << n
                for m in range(1, n+1):
                    s = 1 << m
                    for aa in range(s):
                        for bb in range(t):
                            do_addv(aa, bb, m, n, use_bit_gates, use_gate_version)



def build_controlled_unsigned_adderv_with_values(
        aval, bval, cbit_val, m,  n, use_bit_gates: bool, use_gate_version: bool):
    """ build an n bit signed adder circuit
    """
    ar = QuantumRegister(m, name='a')
    br = QuantumRegister(n+1, name='b')
    cr = QuantumRegister(n-1, name='c')
    cbit = QuantumRegister(1, name='cbit')
    qc = QuantumCircuit(ar, br, cr, cbit)

    ari.set_value(qc, ar, aval)
    ari.set_value(qc, br, bval)
    ari.set_value(qc, cbit, cbit_val)

    if use_gate_version:
        qc.append(ari.controlled_unsigned_adderv_gate(m, n, use_gates=use_bit_gates),
                  [cbit] + ar[:] + br[:] + cr[:])
    else:
        ari.controlled_unsigned_adderv(qc, cbit, ar, br, cr, use_gates=use_bit_gates)

    qc.save_statevector()
    return qc


def do_cuaddv(aval, bval, cbit_val, m, n, use_bit_gates: bool, use_gate_version: bool):
    """ Test adding m-bit and n-bit (m <= n) singed integers
    """
    qc = build_controlled_unsigned_adderv_with_values(
        aval, bval, cbit_val, m, n, use_bit_gates, use_gate_version)

    astr = bin((1 << m) + aval)[-m:]
    bstr = bin((1 << (n+1))+ (cbit_val*aval) + bval)[-(n+1):]
    cstr = "0"*(n-1)
    cbstr = bin(cbit_val)[-1:]
    expected = cbstr + cstr + bstr + astr

    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_controlled_unsigned_adderv():
    """ test adder for all possible m-bit x n-bit inputs.
        a : unsigned input
        b : signed input
    """
    print("Controlled Unigned int adder for mixed bit length test")
    for use_gate_version in [False, True]:
        for use_bit_gates in [False, True]:
            print(f" gate version: {use_gate_version}  bit gates: {use_bit_gates}")
            for n in range(1, 4):
                t = 1 << n
                for m in range(1, n+1):
                    s = 1 << m
                    for a in range(s):
                        print(f"   m: {m}  a:{a}")
                        for b in range(t):
                            for cbit in range(2):
                                # no use_gates option
                                do_cuaddv(a, b, cbit, m, n, use_bit_gates, use_gate_version)


if __name__ == '__main__':
    test_unsigned_adder()
    test_unsigned_adderv()
    test_controlled_unsigned_adderv()
