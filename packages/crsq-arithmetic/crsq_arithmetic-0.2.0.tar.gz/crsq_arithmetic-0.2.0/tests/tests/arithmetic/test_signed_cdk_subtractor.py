""" arithmetic operator test (signed int subtracter)
"""
from qiskit import QuantumCircuit, QuantumRegister

import crsq_arithmetic as ari
import crsq_arithmetic.test_tools as test_tools

def build_cdk_subtractor_with_values(aval, bval, n, use_gate_version: bool):
    """ build an n bit subtracter circuit
    """
    ar = QuantumRegister(n, name='a')
    br = QuantumRegister(n, name='b')
    cr = QuantumRegister(1, name='c')
    qc = QuantumCircuit(ar, br, cr)

    ari.set_value(qc, ar, aval)
    ari.set_value(qc, br, bval)

    if use_gate_version:
        qc.append(ari.cdk_subtractor_gate(n, is_unsigned=False), ar[:]+br[:]+cr[:])
    else:
        ari.cdk_subtractor(qc, ar, br, cr, is_unsigned=False)

    qc.save_statevector()
    return qc


def do_cdk_sub(aval, bval, n, use_gate_version):
    """ Test adding two n bit unsinged integers
    """
    qc = build_cdk_subtractor_with_values(aval, bval, n, use_gate_version)

    astr = bin((1 << n) + aval)[-n:]
    bstr = bin((1 << (n+1)) + bval - aval)[-n:]
    cstr = "0"*(1)
    expected = cstr + bstr + astr

    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_cdk_signed_subtractor():
    """ test subtracter for all possible 3bit inputs.
    """
    print("Signed int subtractor test")
    for use_gate_version in [False, True]:
        print(f" gate version: {use_gate_version}")
        for n in (3, 5):
            s = 1 << n
            hs = 1 << n - 1
            for b in range(s):
                for a in range(s):
                    do_cdk_sub(a-hs, b-hs, n, use_gate_version)



if __name__ == '__main__':
    test_cdk_signed_subtractor()
    
