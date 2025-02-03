""" arithmetic operator test for pytest
"""
from qiskit import QuantumCircuit, QuantumRegister

import crsq_arithmetic as ari
import crsq_arithmetic.test_tools as test_tools

def do_cmp(aval, bval, n):
    """ Test adding two 3bit unsinged integers
       aval, bval : values to add
       n : bit size of the registers
    """
    ar = QuantumRegister(n, name='a')
    br = QuantumRegister(n+1, name='b')
    cr = QuantumRegister(1, name='c')
    qc = QuantumCircuit(ar, br, cr)

    ari.set_value(qc, ar, aval)
    ari.set_value(qc, br, bval)

    ari.cdk_comparator(qc, ar, br, cr)

    qc.save_statevector()

    astr = bin((1 << n) + aval)[-n:]
    bstr = bin((1 << n) + bval)[-n:]
    zstr = "1" if aval > bval else "0"
    cstr = "0"*(1)
    expected = cstr + zstr + bstr + astr

    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_unsigned_cdk_comparator():
    """ run unsigned_comparator for positive numbers
    """
    print("Unsigned int comparator test")
    for n in range(2, 6):
        print(f"n={n}")
        s = 1 << n
        for aa in range(s):
            # print(f"n={n}, aa={aa}")
            for bb in range(s):
                do_cmp(aa, bb, n)


if __name__ == '__main__':
    test_unsigned_cdk_comparator()
