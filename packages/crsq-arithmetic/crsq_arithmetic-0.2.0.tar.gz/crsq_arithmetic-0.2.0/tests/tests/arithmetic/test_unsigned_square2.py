""" arithmetic operator test (unsigned square square)
"""
from qiskit import QuantumCircuit, QuantumRegister

import crsq_arithmetic as ari
import crsq_arithmetic.square2 as square2
import crsq_arithmetic.test_tools as test_tools

def build_square2_with_values(aval, n: int):
    """ build an n bit square circuit
        aval, bval : operands
        n : bit size of the register to use
    """
    ar = QuantumRegister(n, name='a')
    dr = QuantumRegister(n*2, name='d')
    cr1 = QuantumRegister(n-1, name='cr1')
    help = QuantumRegister(1, name='help')
    qc = QuantumCircuit(ar, dr, cr1, help)

    ari.set_value(qc, ar, aval)

    square2.unsigned_square2(qc, ar, dr, cr1, help)

    qc.save_statevector()
    return qc


def do_square2(aval, n):
    """ Test squaring two n bit unsinged integers
    """
    qc = build_square2_with_values(aval, n)

    m = n * 2  # bits for result
    astr = bin((1 << n) + aval)[-n:]
    dstr = bin((1 << m) + aval*aval)[-m:]
    cstr = "0"*(n-1+1)
    expected = cstr + dstr + astr

    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_unsigned_square2():
    """ test square for all possible 3bit inputs.
    """
    n = 4
    s = 1 << n
    print("Unsigned int square test")
    for a in range(s):
        do_square2(a, n)


if __name__ == '__main__':
    test_unsigned_square2()
