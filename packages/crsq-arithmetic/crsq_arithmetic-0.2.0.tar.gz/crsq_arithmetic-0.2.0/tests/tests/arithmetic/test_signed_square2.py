""" arithmetic operator test (signed square square)
"""
from qiskit import QuantumCircuit, QuantumRegister

import crsq_arithmetic as ari
import crsq_arithmetic.square2 as square2
import crsq_arithmetic.test_tools as test_tools

def build_square2_with_values(aval, n: int, use_gate_version):
    """ build an n bit square gate circuit
        aval, bval : operands
        n : bit size of the register to use
    """
    ar = QuantumRegister(n, name='a')
    dr = QuantumRegister(n*2, name='d')
    cr1 = QuantumRegister(n+1, name='cr1')
    cr2 = QuantumRegister(1, name='cr2')
    qc = QuantumCircuit(ar, dr, cr1, cr2)

    ari.set_value(qc, ar, aval)

    if use_gate_version:
        qc.append(square2.signed_square2_gate(n), ar[:] + dr[:] + cr1[:] + cr2[:])
    else:
        square2.signed_square2(qc, ar, dr, cr1, cr2)

    qc.save_statevector()
    return qc


def do_square2(aval, n, use_gate_version):
    """ Test squaring two n bit signed integers
    """
    qc = build_square2_with_values(aval, n, use_gate_version)

    m = n * 2  # bits for result
    astr = bin((1 << n) + aval)[-n:]
    dstr = bin((1 << m) + aval*aval)[-m:]
    cstr = "0"*(n + 2)
    expected = cstr + dstr + astr

    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_signed_square2():
    """ test square_gate for all possible 3bit inputs.
    """
    print("Signed int square gate test")
    for use_gate_version in [False, True]:
        print(f" gate version: {use_gate_version}")
        for n in [4,5,6]:
            s = 1 << n
            hs = 1 << n-1
            for a in [0, 1, 2, 3, hs-1, hs, hs+1, s-4, s-3, s-2, s-1]:
                print(f"n={n} a={a-hs}")
                do_square2(a-hs, n, use_gate_version)


if __name__ == '__main__':
    test_signed_square2()
