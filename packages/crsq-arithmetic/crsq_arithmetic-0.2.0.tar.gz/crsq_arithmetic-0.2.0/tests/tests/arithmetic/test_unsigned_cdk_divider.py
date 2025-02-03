""" arithmetic operator test (signed int adder)
"""
from qiskit import QuantumCircuit, QuantumRegister

import crsq_arithmetic as ari
import crsq_arithmetic.test_tools as test_tools

def build_cdk_divider_with_values(aval: int, bval: int,
                              m: int, n: int, ug: bool):
    """ build an n bit cdk_divider circuit
        aval, bval : operands
        n : bit size of the register to use
    """
    zr = QuantumRegister(m, name='z')
    zzr = QuantumRegister(n, name='zz')
    dr = QuantumRegister(n, name='d')
    cr = QuantumRegister(1, name='cr')
    qc = QuantumCircuit(dr, zr, zzr, cr)

    ari.set_value(qc, zr, aval)
    ari.set_value(qc, dr, bval)

    ari.unsigned_cdk_divider(qc, zr, zzr, dr, cr, use_gates=ug)

    qc.save_statevector()
    return qc


def do_divide(aval, bval, m, n, ug):
    """ Test dividing two integers
    """
    qc = build_cdk_divider_with_values(aval, bval, m, n, ug)

    qq = aval // bval  # higher m bits
    rr = aval % bval   # lower n bits
    qqrr = (qq << n) + rr

    expected = [
        {
            'regs': {
                'zz': (qqrr >> m) & ((1<<n)-1),
                'z': qqrr & ((1<<m)-1),
                'd': bval & ((1<<n)-1),
                'cr': 0
            },
            'amp': 1
        }
    ]
    test_tools.run_circuit_and_check(qc, expected)


def test_cdk_divider():
    """ test cdk_divider for all possible m-bit / n-bit inputs.
    """
    m = 4
    s = 1 << m
    n = 3
    t = 1 << n
    print("int unsigned cdk_divider test")
    for a in range(s):
        for b in range(1, t, 1):
            for ug in [False, True]:
                do_divide(a, b, m, n, ug)


def build_cdk_divider_gate_with_values(aval: int, bval: int,
                                   m: int, n: int):
    """ build an n bit cdk_divider_gate circuit
        aval, bval : operands
        n : bit size of the register to use
    """
    dr = QuantumRegister(n, name='d')
    zr = QuantumRegister(m, name='z')
    zzr = QuantumRegister(n, name='zz')
    cr = QuantumRegister(1, name='cr')
    qc = QuantumCircuit(dr, zr, zzr, cr)

    ari.set_value(qc, zr, aval)
    ari.set_value(qc, dr, bval)

    qc.append(ari.unsigned_cdk_divider_gate(m, n), zr[:] + zzr[:] + dr[:] + cr[:])

    qc.save_statevector()
    return qc


def do_divide_gate(aval, bval, m, n):
    """ Test dividing two integers
    """
    qc = build_cdk_divider_gate_with_values(aval, bval, m, n)

    qq = aval // bval
    rr = aval % bval
    qqrr = (qq << n) + rr

    expected = [
        {
            'regs': {
                'zz': (qqrr >> m) & ((1<<n)-1),
                'z': qqrr & ((1<<m)-1),
                'd': bval & ((1<<n)-1),
                'cr': 0
            },
            'amp': 1
        }
    ]
    test_tools.run_circuit_and_check(qc, expected)


def test_cdk_divider_gate():
    """ test cdk_divider_gate for all possible m-bit / n-bit inputs.
    """
    m = 4
    s = 1 << m
    n = 3
    t = 1 << n
    print("int unsigned cdk_divider gate test")
    for a in range(s):
        for b in range(1, t, 1):
            do_divide_gate(a, b, m, n)


if __name__ == '__main__':
    test_cdk_divider()
    test_cdk_divider_gate()
