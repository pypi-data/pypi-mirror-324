""" Test for the carry gates.
"""
from qiskit.circuit import QuantumCircuit, QuantumRegister

import crsq_arithmetic as ari
import crsq_arithmetic.bit_ops as bb
import crsq_arithmetic.test_tools as test_tools

def do_carry(in_bits: list[int], out_bits: list[int], use_gate):
    """ test carry for one set of inputs and compare with expected output.
        in_bits: [ cin, a, b, cout ]
    """
    qr = QuantumRegister(4)
    qc = QuantumCircuit(qr)
    ari.set_bits(qc, qr, in_bits)
    if use_gate:
        qc.append(bb.carry_gate(), qr[:])
    else:
        bb.carry(qc, qr[0], qr[1], qr[2], qr[3])
    qc.save_statevector()
    expected = "".join(map(lambda x: bin(x)[-1:], reversed(out_bits)))
    exp_dict = {
        expected: 1
    }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_carry():
    """ test carry gate for all possible inputs
    """
    # [cin a b cout]
    print("test_carry")
    for ug in [False, True]:
        do_carry([0, 0, 0, 0], [0, 0, 0, 0], ug)
        do_carry([0, 1, 0, 0], [0, 1, 1, 0], ug)
        do_carry([0, 0, 1, 0], [0, 0, 1, 0], ug)
        do_carry([0, 1, 1, 0], [0, 1, 0, 1], ug)
        do_carry([1, 0, 0, 0], [1, 0, 0, 0], ug)
        do_carry([1, 1, 0, 0], [1, 1, 1, 1], ug)
        do_carry([1, 0, 1, 0], [1, 0, 1, 1], ug)
        do_carry([1, 1, 1, 0], [1, 1, 0, 1], ug)


def do_icarry(in_bits: list[int], out_bits: list[int], use_gate):
    """ test icarry for one set of inputs and compare with expected output.
        in_bits: [ cin, a, b, cout ]
        Note that the arg order is reversed.
    """
    qr = QuantumRegister(4)
    qc = QuantumCircuit(qr)
    ari.set_bits(qc, qr, in_bits)
    if use_gate:
        qc.append(bb.icarry_gate(), qr[:])
    else:
        bb.icarry(qc, qr[0], qr[1], qr[2], qr[3])
    qc.save_statevector()
    expected = "".join(map(lambda x: bin(x)[-1:], reversed(out_bits)))
    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_icarry():
    """ test carry gate for all possible inputs
    """
    # [cin a b cout]
    print("test_icarry")
    # out_bits, in_bits
    for ug in [False, True]:
        do_icarry([0, 0, 0, 0], [0, 0, 0, 0], ug)
        do_icarry([0, 1, 1, 0], [0, 1, 0, 0], ug)
        do_icarry([0, 0, 1, 0], [0, 0, 1, 0], ug)
        do_icarry([0, 1, 0, 1], [0, 1, 1, 0], ug)
        do_icarry([1, 0, 0, 0], [1, 0, 0, 0], ug)
        do_icarry([1, 1, 1, 1], [1, 1, 0, 0], ug)
        do_icarry([1, 0, 1, 1], [1, 0, 1, 0], ug)
        do_icarry([1, 1, 0, 1], [1, 1, 1, 0], ug)


def do_ccarry(in_bits: list[int], out_bits: list[int], use_gate):
    """ test controlled carry for one set of inputs and compare with expected output.
        in_bits: [ cin, a, b, cout ]
    """
    qr = QuantumRegister(5)
    qc = QuantumCircuit(qr)
    ari.set_bits(qc, qr, in_bits)
    if use_gate:
        qc.append(bb.ccarry_gate(), qr[:])
    else:
        bb.ccarry(qc, qr[0], qr[1], qr[2], qr[3], qr[4])
    qc.save_statevector()
    expected = "".join(map(lambda x: bin(x)[-1:], reversed(out_bits)))
    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_ccarry():
    """ test controlled carry gate for all possible inputs
    """
    # [cbit cin a b cout]
    print("test_ccarry")
    for ug in [False, True]:
        do_ccarry([0, 0, 0, 0, 0], [0, 0, 0, 0, 0], ug)
        do_ccarry([0, 0, 1, 0, 0], [0, 0, 1, 0, 0], ug)
        do_ccarry([0, 0, 0, 1, 0], [0, 0, 0, 1, 0], ug)
        do_ccarry([0, 0, 1, 1, 0], [0, 0, 1, 1, 0], ug)
        do_ccarry([0, 1, 0, 0, 0], [0, 1, 0, 0, 0], ug)
        do_ccarry([0, 1, 1, 0, 0], [0, 1, 1, 0, 0], ug)
        do_ccarry([0, 1, 0, 1, 0], [0, 1, 0, 1, 0], ug)
        do_ccarry([0, 1, 1, 1, 0], [0, 1, 1, 1, 0], ug)

        do_ccarry([1, 0, 0, 0, 0], [1, 0, 0, 0, 0], ug)
        do_ccarry([1, 0, 1, 0, 0], [1, 0, 1, 1, 0], ug)
        do_ccarry([1, 0, 0, 1, 0], [1, 0, 0, 1, 0], ug)
        do_ccarry([1, 0, 1, 1, 0], [1, 0, 1, 0, 1], ug)
        do_ccarry([1, 1, 0, 0, 0], [1, 1, 0, 0, 0], ug)
        do_ccarry([1, 1, 1, 0, 0], [1, 1, 1, 1, 1], ug)
        do_ccarry([1, 1, 0, 1, 0], [1, 1, 0, 1, 1], ug)
        do_ccarry([1, 1, 1, 1, 0], [1, 1, 1, 0, 1], ug)


def do_cicarry(in_bits: list[int], out_bits: list[int], use_gate):
    """ test ccarry for one set of inputs and compare with expected output.
        in_bits: [ cin, a, b, cout ]
        Note that args is in the order of (out,in)
    """
    qr = QuantumRegister(5)
    qc = QuantumCircuit(qr)
    ari.set_bits(qc, qr, in_bits)
    if use_gate:
        qc.append(bb.cicarry_gate(), qr[:])
    else:
        bb.cicarry(qc, qr[0], qr[1], qr[2], qr[3], qr[4])
    qc.save_statevector()
    expected = "".join(map(lambda x: bin(x)[-1:], reversed(out_bits)))
    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_cicarry():
    """ test cicarry gate for all possible inputs
    """
    #          out              in
    #          [cbit cin a b cout]
    print("test_cicarry")
    for ug in [False, True]:
        do_cicarry([0, 0, 0, 0, 0], [0, 0, 0, 0, 0], ug)
        do_cicarry([0, 0, 1, 0, 0], [0, 0, 1, 0, 0], ug)
        do_cicarry([0, 0, 0, 1, 0], [0, 0, 0, 1, 0], ug)
        do_cicarry([0, 0, 1, 1, 0], [0, 0, 1, 1, 0], ug)
        do_cicarry([0, 1, 0, 0, 0], [0, 1, 0, 0, 0], ug)
        do_cicarry([0, 1, 1, 0, 0], [0, 1, 1, 0, 0], ug)
        do_cicarry([0, 1, 0, 1, 0], [0, 1, 0, 1, 0], ug)
        do_cicarry([0, 1, 1, 1, 0], [0, 1, 1, 1, 0], ug)

        do_cicarry([1, 0, 0, 0, 0], [1, 0, 0, 0, 0], ug)
        do_cicarry([1, 0, 1, 1, 0], [1, 0, 1, 0, 0], ug)
        do_cicarry([1, 0, 0, 1, 0], [1, 0, 0, 1, 0], ug)
        do_cicarry([1, 0, 1, 0, 1], [1, 0, 1, 1, 0], ug)
        do_cicarry([1, 1, 0, 0, 0], [1, 1, 0, 0, 0], ug)
        do_cicarry([1, 1, 1, 1, 1], [1, 1, 1, 0, 0], ug)
        do_cicarry([1, 1, 0, 1, 1], [1, 1, 0, 1, 0], ug)
        do_cicarry([1, 1, 1, 0, 1], [1, 1, 1, 1, 0], ug)


def do_hcarry(in_bits: list[int], out_bits: list[int], use_gate):
    """ test carry for one set of inputs and compare with expected output.
        in_bits: [ cin, a, b, cout ]
    """
    qr = QuantumRegister(3)
    qc = QuantumCircuit(qr)
    ari.set_bits(qc, qr, in_bits)
    if use_gate:
        qc.append(bb.hcarry_gate(), qr[:])
    else:
        bb.hcarry(qc, qr[0], qr[1], qr[2])
    qc.save_statevector()
    expected = "".join(map(lambda x: bin(x)[-1:], reversed(out_bits)))
    exp_dict = {
        expected: 1
    }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_hcarry():
    """ test carry gate for all possible inputs
    """
    # [a b cout]
    print("test_hcarry")
    for ug in [False, True]:
        do_hcarry([0, 0, 0], [0, 0, 0], ug)
        do_hcarry([1, 0, 0], [1, 1, 0], ug)
        do_hcarry([0, 1, 0], [0, 1, 0], ug)
        do_hcarry([1, 1, 0], [1, 0, 1], ug)


def do_ihcarry(in_bits: list[int], out_bits: list[int], use_gate):
    """ test carry for one set of inputs and compare with expected output.
        in_bits: [ cin, a, b, cout ]
    """
    qr = QuantumRegister(3)
    qc = QuantumCircuit(qr)
    ari.set_bits(qc, qr, in_bits)
    if use_gate:
        qc.append(bb.ihcarry_gate(), qr[:])
    else:
        bb.ihcarry(qc, qr[0], qr[1], qr[2])
    qc.save_statevector()
    expected = "".join(map(lambda x: bin(x)[-1:], reversed(out_bits)))
    exp_dict = {
        expected: 1
    }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_ihcarry():
    """ test carry gate for all possible inputs
    """
    # [a b cout]
    print("test_ihcarry")
    for ug in [False, True]:
        do_ihcarry([0, 0, 0], [0, 0, 0], ug)
        do_ihcarry([1, 1, 0], [1, 0, 0], ug)
        do_ihcarry([0, 1, 0], [0, 1, 0], ug)
        do_ihcarry([1, 0, 1], [1, 1, 0], ug)



def do_chcarry(in_bits: list[int], out_bits: list[int], use_gate):
    """ test controlled carry for one set of inputs and compare with expected output.
        in_bits: [ ctrl, a, b, cout ]
    """
    qr = QuantumRegister(4)
    qc = QuantumCircuit(qr)
    ari.set_bits(qc, qr, in_bits)
    if use_gate:
        qc.append(bb.chcarry_gate(), qr[:])
    else:
        bb.chcarry(qc, qr[0], qr[1], qr[2], qr[3])
    qc.save_statevector()
    expected = "".join(map(lambda x: bin(x)[-1:], reversed(out_bits)))
    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_chcarry():
    """ test controlled carry gate for all possible inputs
    """
    # [cbit cin a b cout]
    print("test_chcarry")
    for ug in [False, True]:
        do_chcarry([0, 0, 0, 0], [0, 0, 0, 0], ug)
        do_chcarry([0, 1, 0, 0], [0, 1, 0, 0], ug)
        do_chcarry([0, 0, 1, 0], [0, 0, 1, 0], ug)
        do_chcarry([0, 1, 1, 0], [0, 1, 1, 0], ug)

        do_chcarry([1, 0, 0, 0], [1, 0, 0, 0], ug)
        do_chcarry([1, 1, 0, 0], [1, 1, 1, 0], ug)
        do_chcarry([1, 0, 1, 0], [1, 0, 1, 0], ug)
        do_chcarry([1, 1, 1, 0], [1, 1, 0, 1], ug)


def do_cihcarry(in_bits: list[int], out_bits: list[int], use_gate):
    """ test ccarry for one set of inputs and compare with expected output.
        in_bits: [ ctrl, a, b, cout ]
        Note that args is in the order of (out,in)
    """
    qr = QuantumRegister(4)
    qc = QuantumCircuit(qr)
    ari.set_bits(qc, qr, in_bits)
    if use_gate:
        qc.append(bb.cihcarry_gate(), qr[:])
    else:
        bb.cihcarry(qc, qr[0], qr[1], qr[2], qr[3])
    qc.save_statevector()
    expected = "".join(map(lambda x: bin(x)[-1:], reversed(out_bits)))
    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_cihcarry():
    """ test cicarry gate for all possible inputs
    """
    #          out              in
    #          [cbit cin a b cout]
    print("test_cihcarry")
    for ug in [False, True]:
        do_cihcarry([0, 0, 0, 0], [0, 0, 0, 0], ug)
        do_cihcarry([0, 1, 0, 0], [0, 1, 0, 0], ug)
        do_cihcarry([0, 0, 1, 0], [0, 0, 1, 0], ug)
        do_cihcarry([0, 1, 1, 0], [0, 1, 1, 0], ug)

        do_cihcarry([1, 0, 0, 0], [1, 0, 0, 0], ug)
        do_cihcarry([1, 1, 1, 0], [1, 1, 0, 0], ug)
        do_cihcarry([1, 0, 1, 0], [1, 0, 1, 0], ug)
        do_cihcarry([1, 1, 0, 1], [1, 1, 1, 0], ug)


def do_cocarry(in_bits: list[int], out_bits: list[int], use_gate):
    """ test constant input carry for one set of inputs and compare with expected output.
        in_bits: [ cin, y, b, cout ]
    """
    qr = QuantumRegister(3)
    qc = QuantumCircuit(qr)
    ari.set_bits(qc, qr, in_bits[0:1] + in_bits[2:4])
    if use_gate:
        qc.append(bb.cocarry_gate(in_bits[1]), qr[:])
    else:
        bb.cocarry(qc, qr[0], in_bits[1], qr[1], qr[2])
    qc.save_statevector()
    expected = "".join(map(lambda x: bin(x)[-1:], reversed(out_bits)))
    exp_dict = {
        expected: 1
    }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_cocarry():
    """ test carry gate for all possible inputs
    """
    # [cin a b cout]
    print("test_cocarry")
    for ug in [False, True]:
        do_cocarry([0, 0, 0, 0], [0, 0, 0], ug)
        do_cocarry([0, 1, 0, 0], [0, 1, 0], ug)
        do_cocarry([0, 0, 1, 0], [0, 1, 0], ug)
        do_cocarry([0, 1, 1, 0], [0, 0, 1], ug)
        do_cocarry([1, 0, 0, 0], [1, 0, 0], ug)
        do_cocarry([1, 1, 0, 0], [1, 1, 1], ug)
        do_cocarry([1, 0, 1, 0], [1, 1, 1], ug)
        do_cocarry([1, 1, 1, 0], [1, 0, 1], ug)


def do_icocarry(in_bits: list[int], out_bits: list[int], use_gate):
    """ test constant input carry for one set of inputs and compare with expected output.
        in_bits: [ cin, y, b, cout ]
    """
    qr = QuantumRegister(3)
    qc = QuantumCircuit(qr)
    ari.set_bits(qc, qr, in_bits[0:1] + in_bits[2:4])
    if use_gate:
        qc.append(bb.icocarry_gate(in_bits[1]), qr[:])
    else:
        bb.icocarry(qc, qr[0], in_bits[1], qr[1], qr[2])
    qc.save_statevector()
    out_reg_bits = out_bits[0:1] + out_bits[2:4]
    expected = "".join(map(lambda x: bin(x)[-1:], reversed(out_reg_bits)))
    exp_dict = {
        expected: 1
    }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_icocarry():
    """ test carry gate for all possible inputs
    """
    # [cin a b cout]
    print("test_icocarry")

    for ug in [False, True]:
        do_icocarry([0, 0, 0, 0], [0, 0, 0, 0], ug)
        do_icocarry([0, 1, 1, 0], [0, 1, 0, 0], ug)
        do_icocarry([0, 0, 1, 0], [0, 0, 1, 0], ug)
        do_icocarry([0, 1, 0, 1], [0, 1, 1, 0], ug)
        do_icocarry([1, 0, 0, 0], [1, 0, 0, 0], ug)
        do_icocarry([1, 1, 1, 1], [1, 1, 0, 0], ug)
        do_icocarry([1, 0, 1, 1], [1, 0, 1, 0], ug)
        do_icocarry([1, 1, 0, 1], [1, 1, 1, 0], ug)


def do_cohcarry(in_bits: list[int], out_bits: list[int], use_gate):
    """ test carry for one set of inputs and compare with expected output.
        in_bits: [ cin, a, b, cout ]
    """
    qr = QuantumRegister(2)
    qc = QuantumCircuit(qr)
    ari.set_bits(qc, qr, in_bits[1:3])
    if use_gate:
        qc.append(bb.cohcarry_gate(in_bits[0]), qr[:])
    else:
        bb.cohcarry(qc, in_bits[0], qr[0], qr[1])
    qc.save_statevector()
    expected = "".join(map(lambda x: bin(x)[-1:], reversed(out_bits)))
    exp_dict = {
        expected: 1
    }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_cohcarry():
    """ test carry gate for all possible inputs
    """
    # [y b cout]
    print("test_cohcarry")
    for ug in [False, True]:
        do_cohcarry([0, 0, 0], [0, 0], ug)
        do_cohcarry([1, 0, 0], [1, 0], ug)
        do_cohcarry([0, 1, 0], [1, 0], ug)
        do_cohcarry([1, 1, 0], [0, 1], ug)


def do_icohcarry(in_bits: list[int], out_bits: list[int], use_gate):
    """ test carry for one set of inputs and compare with expected output.
        in_bits: [ cin, a, b, cout ]
    """
    qr = QuantumRegister(2)
    qc = QuantumCircuit(qr)
    ari.set_bits(qc, qr, in_bits[1:3])
    if use_gate:
        qc.append(bb.icohcarry_gate(in_bits[0]), qr[:])
    else:
        bb.icohcarry(qc, in_bits[0], qr[0], qr[1])
    qc.save_statevector()
    expected = "".join(map(lambda x: bin(x)[-1:], reversed(out_bits)))
    exp_dict = {
        expected: 1
    }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_icohcarry():
    """ test carry gate for all possible inputs
    """
    # [y b cout]
    print("test_icohcarry")
    for ug in [False, True]:
        do_icohcarry([0, 0, 0], [0, 0], ug)
        do_icohcarry([1, 1, 0], [0, 0], ug)
        do_icohcarry([0, 1, 0], [1, 0], ug)
        do_icohcarry([1, 0, 1], [1, 0], ug)


if __name__ == '__main__':
    test_carry()
    test_ccarry()
    test_icarry()
    test_cicarry()
    test_hcarry()
    test_ihcarry()
    test_chcarry()
    test_cihcarry()
    test_cocarry()
    test_icocarry()
    test_cohcarry()
    test_icohcarry()
