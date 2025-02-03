""" arithmetic operator test for pytest
"""
from qiskit import QuantumCircuit, QuantumRegister

import crsq_arithmetic as ari
import crsq_arithmetic.test_tools as test_tools

def do_cdk_subtract(aval, bval, n, use_gate_version):
    """ Test adding two 3bit unsinged integers
       aval, bval : result = bval - aval
       n : bit size of the registers
    """
    ar = QuantumRegister(n, name='a')
    br = QuantumRegister(n+1, name='b')
    cr = QuantumRegister(1, name='c')
    qc = QuantumCircuit(ar, br, cr)

    ari.set_value(qc, ar, aval)
    ari.set_value(qc, br, bval)

    if use_gate_version:
        qc.append(ari.cdk_subtractor_gate(n, is_unsigned=True), ar[:]+br[:]+cr[:])
    else:
        ari.cdk_subtractor(qc, ar, br, cr, is_unsigned=True)

    qc.save_statevector()

    astr = bin((1 << n) + aval)[-n:]
    bstr = bin((1 << n+1)+ bval - aval)[-(n+1):]
    cstr = "0"*(1)
    expected = cstr + bstr + astr

    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_unsigned_cdk_subtractor():
    """ run unsigned_cdk_subtractor for positive numbers
    """
    print("Unsigned int cdk_subtractor test")
    for use_gate_version in [False, True]:
        print(f" gate version: {use_gate_version}")
        for n in range(2, 5):
            print(f" bit size: {n}")
            s = 1 << n
            for aa in range(s):
                for bb in range(s):
                    cc = aa + bb
                    do_cdk_subtract(aa, cc, n, use_gate_version)


if __name__ == '__main__':
    test_unsigned_cdk_subtractor()
