""" arithmetic operator test (signed int adder)
"""
from qiskit import QuantumCircuit, QuantumRegister
import crsq_arithmetic as ari
import crsq_arithmetic.test_tools as test_tools

def build_signed_adder_with_values(aval, bval, n, use_bit_gates: bool, use_gate_version: bool):
    """ build an n bit signed adder circuit
    """
    ar = QuantumRegister(n, name='a')
    br = QuantumRegister(n, name='b')
    cr = QuantumRegister(n - 1, name='c')
    qc = QuantumCircuit(ar, br, cr)

    ari.set_value(qc, ar, aval)
    ari.set_value(qc, br, bval)

    if use_gate_version:
        qc.append(ari.signed_adder_gate(n, use_gates=use_bit_gates), ar[:] + br[:] + cr[:])
    else:
        ari.signed_adder(qc, ar, br, cr, use_gates=use_bit_gates)
    qc.save_statevector()
    return qc


def do_sadd(aval, bval, n, use_bit_gates: bool, use_gate_version: bool):
    """ Test adding two n-bit signed integers
    """
    qc = build_signed_adder_with_values(aval, bval, n, use_bit_gates, use_gate_version)
    astr = bin((1 << n) + aval)[-n:]
    bstr = bin((1 << n+1)+aval+bval)[-n:]
    cstr = "0"*(n-1)
    expected = cstr + bstr + astr
    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_signed_adder():
    """ test adder for all possible n-bit inputs.
    """
    print("Signed int adder test")
    for use_gate_version in [False, True]:
        for use_bit_gates in [False, True]:
            print(f" gate version: {use_gate_version}  bit gates: {use_bit_gates}")
            for n in range(2, 4):
                s = 1 << n
                hs = s >> 1
                for a in range(s):
                    for b in range(s):
                        # print("a = ", a, "b=", b)
                        do_sadd(a-hs, b-hs, n, use_bit_gates, use_gate_version)


## signed adderv >>>>
def build_signed_adderv_with_values(aval, bval, m, n, use_bit_gates: bool, use_gate_version: bool):
    """ build an n bit signed adder circuit
    """
    ar = QuantumRegister(m, name='a')
    br = QuantumRegister(n, name='b')
    cr = QuantumRegister(n-1, name='c')
    qc = QuantumCircuit(ar, br, cr)

    ari.set_value(qc, ar, aval)
    ari.set_value(qc, br, bval)

    if use_gate_version:
        qc.append(ari.signed_adderv_gate(m, n, use_gates=use_bit_gates), ar[:] + br[:] + cr[:])
    else:
        ari.signed_adderv(qc, ar, br, cr, use_gates=use_bit_gates)
    qc.save_statevector()
    return qc


def do_saddv(aval, bval, m, n, use_bit_gates: bool, use_gate_version: bool):
    """ Test adding two n-bit signed integers
    """
    qc = build_signed_adderv_with_values(aval, bval, m, n, use_bit_gates, use_gate_version)
    astr = bin((1 << m+1) + aval)[-m:]
    bstr = bin((1 << n+1) + aval + bval)[-n:]
    cstr = "0"*(n-1)
    expected = cstr + bstr + astr
    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_signed_adderv():
    """ test adder for all possible n-bit inputs.
    """
    print("Signed int adderv test")
    for use_gate_version in [False, True]:
        for use_bit_gates in [False, True]:
            print(f" gate version: {use_gate_version}  bit gates: {use_bit_gates}")
            for n in range(2, 4):
                t = 1 << n
                ht = t >> 1
                for m in range(1, n+1):
                    s = 1 << m
                    hs = s >> 1
                    for a in range(s):
                        for b in range(t):
                            # print("a = ", a, "b=", b)
                            do_saddv(a-hs, b-ht, m, n, use_bit_gates, use_gate_version)


## signed adderv <<<<

def build_controlled_signed_adder_with_values(aval, bval, cbit_val, n, use_bit_gates: bool, use_gate_version: bool):
    """ build an n bit controlled signed adder circuit
    """
    ar = QuantumRegister(n, name='a')
    br = QuantumRegister(n, name='b')
    cr = QuantumRegister(n-1, name='c')
    cbit = QuantumRegister(1, name='cbit')
    qc = QuantumCircuit(ar, br, cr, cbit)

    ari.set_value(qc, ar, aval)
    ari.set_value(qc, br, bval)
    ari.set_value(qc, cbit, cbit_val)

    # no use_gates option
    if use_gate_version:
        qc.append(ari.controlled_signed_adder_gate(n, use_gates=use_bit_gates),
                  [cbit] + ar[:] + br[:] + cr[:])
    else:
        ari.controlled_signed_adder(qc, cbit, ar, br, cr, use_bit_gates)

    qc.save_statevector()
    return qc


def do_csadd(aval, bval, cbit_val, n, use_bit_gates: bool, use_gate_version: bool):
    """ Test adding two n-bit singed integers
    """
    qc = build_controlled_signed_adder_with_values(
        aval, bval, cbit_val, n, use_bit_gates, use_gate_version)

    astr = bin((1 << n) + aval)[-n:]
    bstr = bin((1 << n+1)+ (cbit_val*aval) +bval)[-n:]
    cstr = "0"*(n-1)
    cbstr = bin(cbit_val)[-1:]
    expected = cbstr + cstr + bstr + astr

    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_controlled_signed_adder():
    """ test adder for all possible n bit inputs.
    """
    print("Controlled Signed int adder test")
    for use_gate_version in [False, True]:
        for use_bit_gates in [False, True]:
            print(f" gate version: {use_gate_version}  bit gates: {use_bit_gates}")
            for n in range(2, 4):
                s = 1 << n
                hs = s >> 1
                for a in range(s):
                    print("   a:", a)
                    for b in range(s):
                        for cbit in range(2):
                            do_csadd(a-hs, b-hs, cbit, n, use_bit_gates, use_gate_version)


def build_controlled_signed_adderv_with_values(
        aval, bval, cbit_val, m,  n, use_bit_gates: bool, use_gate_version: bool):
    """ build an n bit signed adder circuit
    """
    ar = QuantumRegister(m, name='a')
    br = QuantumRegister(n, name='b')
    cr = QuantumRegister(n-1, name='c')
    cbit = QuantumRegister(1, name='cbit')
    qc = QuantumCircuit(ar, br, cr, cbit)

    ari.set_value(qc, ar, aval)
    ari.set_value(qc, br, bval)
    ari.set_value(qc, cbit, cbit_val)

    if use_gate_version:
        qc.append(ari.controlled_signed_adderv_gate(m, n, use_gates=use_bit_gates),
                  [cbit] + ar[:] + br[:] + cr[:])
    else:
        ari.controlled_signed_adderv(qc, cbit, ar, br, cr, use_gates=use_bit_gates)

    qc.save_statevector()
    return qc


def do_csaddv(aval, bval, cbit_val, m, n, use_bit_gates: bool, use_gate_version: bool):
    """ Test adding m-bit and n-bit (m <= n) singed integers
    """
    qc = build_controlled_signed_adderv_with_values(
        aval, bval, cbit_val, m, n, use_bit_gates, use_gate_version)

    astr = bin((1 << m) + aval)[-m:]
    bstr = bin((1 << n+1)+ (cbit_val*aval) +bval)[-n:]
    cstr = "0"*(n-1)
    cbstr = bin(cbit_val)[-1:]
    expected = cbstr + cstr + bstr + astr

    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_controlled_signed_adderv():
    """ test adder for all possible m-bit x n-bit inputs.
        a : unsigned input
        b : signed input
    """
    print("Controlled Signed int adder for mixed bit length test")
    for use_gate_version in [False, True]:
        for use_bit_gates in [False, True]:
            print(f" gate version: {use_gate_version}  bit gates: {use_bit_gates}")
            for n in range(2, 4):
                t = 1 << n
                ht = t >> 1
                for m in range(1, n+1):
                    s = 1 << m
                    hs = s >> 1
                    for a in range(s):
                        print(f"   m: {m}  a:{a}")
                        for b in range(t):
                            for cbit in range(2):
                                # no use_gates option
                                do_csaddv(a-hs, b-ht, cbit, m, n, use_bit_gates, use_gate_version)


if __name__ == '__main__':
    test_signed_adder()
    test_signed_adderv()
    test_controlled_signed_adder()
    test_controlled_signed_adderv()
