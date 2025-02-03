""" arithmetic operator test (signed int adder)
"""
from qiskit import QuantumCircuit, QuantumRegister
import crsq_arithmetic as ari
import crsq_arithmetic.test_tools as test_tools

def build_signed_cdk_adder_with_values(aval, bval, n, use_gate_version: bool):
    """ build an n bit signed adder circuit
    """
    ar = QuantumRegister(n, name='a')
    br = QuantumRegister(n, name='b')
    cr = QuantumRegister(1, name='c')
    qc = QuantumCircuit(ar, br, cr)

    ari.set_value(qc, ar, aval)
    ari.set_value(qc, br, bval)

    if use_gate_version:
        qc.append(ari.cdk_adder_gate(n, is_unsigned=False), ar[:] + br[:] + cr[:])
    else:
        ari.cdk_adder(qc, ar, br, cr, is_unsigned=False)
    qc.save_statevector()
    return qc


def do_cdk_sadd(aval, bval, n, use_gate_version: bool):
    """ Test adding two n-bit signed integers
    """
    qc = build_signed_cdk_adder_with_values(aval, bval, n, use_gate_version)
    astr = bin((1 << n) + aval)[-n:]
    bstr = bin((1 << n+1)+aval+bval)[-n:]
    cstr = "0"*(1)
    expected = cstr + bstr + astr
    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_signed_cdk_adder():
    """ test adder for all possible n-bit inputs.
    """
    print("Signed int adder test")
    for use_gate_version in [False, True]:
        print(f" gate version: {use_gate_version}")
        for n in range(2, 5):
            print(f"n={n}")
            s = 1 << n
            hs = s >> 1
            for a in range(s):
                for b in range(s):
                    # print("a = ", a, "b=", b)
                    do_cdk_sadd(a-hs, b-hs, n, use_gate_version)


def build_controlled_signed_cdk_adder_with_values(aval, bval, cbit_val, n, use_gate_version: bool):
    """ build an n bit controlled signed adder circuit
    """
    ar = QuantumRegister(n, name='a')
    br = QuantumRegister(n, name='b')
    cr = QuantumRegister(1, name='c')
    cbit = QuantumRegister(1, name='cbit')
    qc = QuantumCircuit(cbit, ar, br, cr)

    ari.set_value(qc, ar, aval)
    ari.set_value(qc, br, bval)
    ari.set_value(qc, cbit, cbit_val)

    # no use_gates option
    if use_gate_version:
        qc.append(ari.cdk_adder_gate(n, is_unsigned=False, opt_ctrl_state="1"),
                  cbit[:] + ar[:] + br[:] + cr[:])
    else:
        ari.cdk_adder(qc, ar, br, cr, is_unsigned=False, opt_ctrl_bit=cbit[0])

    qc.save_statevector()
    return qc


def do_cdk_csadd(aval, bval, cbit_val, n, use_gate_version: bool):
    """ Test adding two n-bit singed integers
    """
    qc = build_controlled_signed_cdk_adder_with_values(
        aval, bval, cbit_val, n, use_gate_version)

    astr = bin((1 << n) + aval)[-n:]
    bstr = bin((1 << n+1)+ (cbit_val*aval) +bval)[-n:]
    cstr = "0"*(1)
    cbstr = bin(cbit_val)[-1:]
    expected = cstr + bstr + astr + cbstr

    exp_dict = { expected: 1 }
    print(f"expected: {expected}")
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_controlled_signed_cdk_adder():
    """ test adder for all possible n bit inputs.
    """
    print("Controlled Signed int adder test")
    for use_gate_version in [False, True]:
        print(f" gate version: {use_gate_version}")
        for n in range(2, 4):
            print(f"n={n}")
            s = 1 << n
            hs = s >> 1
            for a in range(s):
                for b in range(s):
                    for cbit in range(2):
                        # print(f"   a: {a}, b: {b}, cbit: {cbit}")
                        do_cdk_csadd(a-hs, b-hs, cbit, n, use_gate_version)



if __name__ == '__main__':
    test_signed_cdk_adder()
    test_controlled_signed_cdk_adder()
