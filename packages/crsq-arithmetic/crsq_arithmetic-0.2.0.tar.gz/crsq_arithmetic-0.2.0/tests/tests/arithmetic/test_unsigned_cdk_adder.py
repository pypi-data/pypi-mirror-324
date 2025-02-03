""" arithmetic operator test for pytest
"""
from qiskit import QuantumCircuit, QuantumRegister

import crsq_arithmetic as ari
import crsq_arithmetic.test_tools as test_tools

def do_add(aval, bval, n):
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

    ari.cdk_adder(qc, ar, br, cr, is_unsigned=True)

    qc.save_statevector()

    astr = bin((1 << n) + aval)[-n:]
    bstr = bin((1 << n+1)+aval+bval)[-(n+1):]
    cstr = "0"*(1)
    expected = cstr + bstr + astr

    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_unsigned_cdk_adder():
    """ run unsigned_adder for positive numbers
    """
    print("Unsigned int adder test")
    for n in range(2, 6):
        print(f"n={n}")
        s = 1 << n
        for aa in range(s):
            # print(f"n={n}, aa={aa}")
            for bb in range(s):
                do_add(aa, bb, n)


def build_controlled_unsigned_cdk_adder_with_values(
        aval, bval, cbit_val, n, use_bit_gates: bool, use_gate_version: bool):
    """ build an n bit signed adder circuit
    """
    ar = QuantumRegister(n, name='a')
    br = QuantumRegister(n+1, name='b')
    cr = QuantumRegister(1, name='c')
    cbit = QuantumRegister(1, name='cbit')
    qc = QuantumCircuit(cbit, ar, br, cr)

    ari.set_value(qc, ar, aval)
    ari.set_value(qc, br, bval)
    ari.set_value(qc, cbit, cbit_val)
    # print(f"n={n}, a={aval}, b={bval}, cbit={cbit_val}")

    if use_gate_version:
        qc.append(ari.cdk_adder_gate(n, is_unsigned=True, opt_ctrl_state="1"),
                  cbit[:] + ar[:] + br[:] + cr[:])
    else:
        ari.cdk_adder(qc, ar, br, cr, is_unsigned=True, opt_ctrl_bit=cbit[0], opt_ctrl_state="1")

    qc.save_statevector()
    return qc


def do_cdk_cuadd(aval, bval, cbit_val, n, use_bit_gates: bool, use_gate_version: bool):
    """ Test adding m-bit and n-bit (m <= n) singed integers
    """
    qc = build_controlled_unsigned_cdk_adder_with_values(
        aval, bval, cbit_val, n, use_bit_gates, use_gate_version)

    astr = bin((1 << n) + aval)[-n:]
    bstr = bin((1 << (n+1))+ (cbit_val*aval) + bval)[-(n+1):]
    cstr = "0"*(1)
    cbstr = bin(cbit_val)[-1:]
    expected = cstr + bstr + astr + cbstr
    # print(f"expected: {expected}")

    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_controlled_unsigned_cdk_adder():
    """ test adder for all possible m-bit x n-bit inputs.
        a : unsigned input
        b : signed input
    """
    print("Controlled Unigned int adder test")
    for use_gate_version in [False, True]:
        for use_bit_gates in [False, True]:
            print(f" gate version: {use_gate_version}  bit gates: {use_bit_gates}")
            for n in range(2, 5):
                print(f"n={n}")
                t = 1 << n
                s = 1 << n
                for a in range(s):
                    # print(f"   n: {n}  a:{a}")
                    for b in range(t):
                        for cbit in range(2):
                            # no use_gates option
                            do_cdk_cuadd(a, b, cbit, n, use_bit_gates, use_gate_version)


if __name__ == '__main__':
    test_unsigned_cdk_adder()
    test_controlled_unsigned_cdk_adder()
