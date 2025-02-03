""" arithmetic operator test (unsigned square square)
"""
from qiskit import QuantumCircuit, QuantumRegister

import crsq_arithmetic as ari
import crsq_arithmetic.test_tools as test_tools

def build_multiplier_with_values(aval, bval, n: int):
    """ build an n bit square circuit
        aval, bval : operands
        n : bit size of the register to use
    """
    ar = QuantumRegister(n, name='a')
    br = QuantumRegister(n, name='b')
    dr = QuantumRegister(n*2, name='d')
    cr1 = QuantumRegister(n, name='cr1')
    cr2 = QuantumRegister(n-1, name='cr2')
    qc = QuantumCircuit(ar, br, dr, cr1, cr2)

    ari.set_value(qc, ar, aval)
    ari.set_value(qc, br, bval)

    # no use_gates option
    ari.unsigned_multiplier(qc, ar, br, dr, cr1, cr2)

    qc.save_statevector()
    return qc


def do_umult(aval, bval, n):
    """ Test squaring two n bit unsinged integers
    """
    qc = build_multiplier_with_values(aval, bval, n)

    m = n * 2  # bits for result
    astr = bin((1 << n) + aval)[-n:]
    bstr = bin((1 << n) + bval)[-n:]
    dstr = bin((1 << m) + aval*bval)[-m:]
    cstr = "0"*(n+n-1)
    expected = cstr + dstr + bstr + astr

    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_unsigned_multiplier():
    """ test square for all possible 3bit inputs.
    """
    n = 3
    s = 1 << n
    print("Unsigned int multiplier test")
    for a in range(s):
        for b in range(s):
            do_umult(a, b, n)


def build_multiplier_gate_with_values(aval, bval, n: int):
    """ build an n bit square circuit
        aval, bval : operands
        n : bit size of the register to use
    """
    ar = QuantumRegister(n, name='a')
    br = QuantumRegister(n, name='b')
    dr = QuantumRegister(n*2, name='d')
    cr1 = QuantumRegister(n, name='cr1')
    cr2 = QuantumRegister(n-1, name='cr2')
    qc = QuantumCircuit(ar, br, cr1, cr2, dr)

    ari.set_value(qc, ar, aval)
    ari.set_value(qc, br, bval)

    qc.append(ari.unsigned_multiplier_gate(n), ar[:] + br[:] + dr[:] + cr1[:] + cr2[:])

    qc.save_statevector()
    return qc


def do_umult_gate(aval, bval, n):
    """ Test squaring two n bit unsinged integers
    """
    qc = build_multiplier_gate_with_values(aval, bval, n)

    m = n * 2  # bits for result
    astr = bin((1 << n) + aval)[-n:]
    bstr = bin((1 << n) + bval)[-n:]
    dstr = bin((1 << m) + aval*bval)[-m:]
    cstr = "0"*(n+n-1)
    expected = dstr + cstr + bstr + astr

    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_unsigned_multiplier_gate():
    """ test square for all possible 3bit inputs.
    """
    n = 3
    s = 1 << n
    print("Unsigned int multiplier gate test")
    for a in range(s):
        for b in range(s):
            do_umult_gate(a, b, n)


if __name__ == '__main__':
    test_unsigned_multiplier()
    test_unsigned_multiplier_gate()
