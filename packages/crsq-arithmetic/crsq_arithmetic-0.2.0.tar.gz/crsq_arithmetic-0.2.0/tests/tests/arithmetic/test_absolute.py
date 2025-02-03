""" Test const adder
"""

from qiskit.circuit import QuantumCircuit, QuantumRegister

import crsq_arithmetic as ari
import crsq_arithmetic.test_tools as test_tools

def build_absolute_circ_for(n: int, a: int):
    """ build test circuit for scoadder"""
    ar = QuantumRegister(n, "a")
    cr = QuantumRegister(n-1, "cy")
    sr = QuantumRegister(1, "s")
    sb = sr[0]
    qc: QuantumCircuit = QuantumCircuit(ar, sr, cr)
    ari.set_value(qc, ar, a)
    ari.absolute(qc, ar, sb, cr)
    return qc

def do_absolute_for(n: int, a: int, verbose: bool = False):
    """ test for one combination of y and b
    """
    qc = build_absolute_circ_for(n, a)
    qc.save_statevector()
    ##
    cbits = "0" * (n-1)
    if a < 0:
        sbit = "1"
    else:
        sbit = "0"
    abits = (bin((1<<n) + abs(a)))[-n:]
    exp = {
        cbits + sbit + abits : 1
    }
    if verbose:
        print(f" testing a = {a}")
    test_tools.run_circuit_and_check(qc, exp)


def test_absolute(verbose: bool = False):
    """ test scoadder
    """
    n = 4  # bits
    N = 2**n
    H = N // 2
    print(f"test_aboslute({n})")
    for a in range(N):
        do_absolute_for(n, a - H, verbose)


def build_absolute_gate_for(n: int, b: int):
    """ build test gate for scoadder"""
    ar = QuantumRegister(n, "a")
    cr = QuantumRegister(n-1, "cy")
    sr = QuantumRegister(1, "s")
    qc: QuantumCircuit = QuantumCircuit(ar, sr, cr)
    ari.set_value(qc, ar, b)
    qc.append(ari.absolute_gate(n), ar[:] + sr[:] + cr[:])
    return qc

def do_absolute_gate_for(n: int, a: int, verbose: bool = False):
    """ test for one combination of y and b
    """
    qc = build_absolute_gate_for(n, a)
    qc.save_statevector()
    ##
    cbits = "0" * (n-1)
    if a < 0:
        sbit = "1"
    else:
        sbit = "0"
    abits = (bin((1<<n) + abs(a)))[-n:]
    exp = {
        cbits + sbit + abits : 1
    }
    if verbose:
        print(f" testing a = {a}")
    test_tools.run_circuit_and_check(qc, exp)


def test_absolute_gate(verbose: bool = False):
    """ test scoadder
    """
    n = 4  # bits
    N = 2**n
    H = N // 2
    print(f"test_aboslute_gate({n})")
    for a in range(N):
        do_absolute_gate_for(n, a - H, verbose)


if __name__ == '__main__':
    v = True
    test_absolute(v)
    test_absolute_gate(v)
