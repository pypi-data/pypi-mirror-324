""" arithmetic operator test (unsigned square square)
"""
from qiskit import QuantumCircuit, QuantumRegister

import crsq_arithmetic as ari
import crsq_arithmetic.test_tools as test_tools


def build_usquare_with_values(aval, n: int, ug: bool):
    """ build an n bit square circuit
        aval, bval : operands
        n : bit size of the register to use
    """
    ar = QuantumRegister(n, name='a')
    dr = QuantumRegister(n*2, name='d')
    cr1 = QuantumRegister(((n+1)//2)*2-1, name='cr1')
    cr2 = QuantumRegister(((n+1)//2)*2-2, name='cr2')
    qc = QuantumCircuit(ar, dr, cr1, cr2)

    ari.set_value(qc, ar, aval)

    ari.unsigned_square(qc, ar, dr, cr1, cr2, use_gates=ug)

    qc.save_statevector()
    return qc


def do_usquare(aval, n, ug):
    """ Test squaring two n bit unsinged integers
    """
    qc = build_usquare_with_values(aval, n, ug)

    m = n * 2  # bits for result
    astr = bin((1 << n) + aval)[-n:]
    dstr = bin((1 << m) + aval*aval)[-m:]
    cstr = "0"*(((n+1)//2)*4-3)
    expected = cstr + dstr + astr

    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_unsigned_square():
    """ test square for all possible 3bit inputs.
    """
    print("Unsigned int square test")
    for ug in [False, True]:
        for n in [4,5,6]:
            s = 1 << n
            for a in [0,1,2,3,s-4,s-3,s-2,s-1]:
                print(f"n={n} a={a} use_gates={ug}")
                do_usquare(a, n, ug)


def build_usquare_gate_with_values(aval, n: int):
    """ build an n bit square gate circuit
        aval, bval : operands
        n : bit size of the register to use
    """
    ar = QuantumRegister(n, name='a')
    dr = QuantumRegister(n*2, name='d')
    cr1 = QuantumRegister(((n+1)//2)*2-1, name='cr1')
    cr2 = QuantumRegister(((n+1)//2)*2-2, name='cr2')
    qc = QuantumCircuit(ar, dr, cr1, cr2)

    ari.set_value(qc, ar, aval)

    qc.append(ari.unsigned_square_gate(n), ar[:] + dr[:] + cr1[:] + cr2[:])

    qc.save_statevector()
    return qc


def do_usquare_gate(aval, n):
    """ Test squaring two n bit unsinged integers
    """
    qc = build_usquare_gate_with_values(aval, n)

    m = n * 2  # bits for result
    astr = bin((1 << n) + aval)[-n:]
    dstr = bin((1 << m) + aval*aval)[-m:]
    cstr = "0"*(((n+1)//2)*4-3)
    expected = cstr + dstr + astr

    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_unsigned_square_gate():
    """ test square_gate for all possible 3bit inputs.
    """
    print("Unsigned int square gate test")
    for n in [4,5,6]:
        s = 1 << n
        for a in [0,1,2,3,s-4,s-3,s-2,s-1]:
            print(f"n={n} a={a}")
            do_usquare_gate(a, n)


if __name__ == '__main__':
    test_unsigned_square()
    test_unsigned_square_gate()
