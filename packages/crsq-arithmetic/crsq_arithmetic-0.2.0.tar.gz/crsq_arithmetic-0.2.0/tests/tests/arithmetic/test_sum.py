""" Test for the sum gates.
"""
from qiskit.circuit import QuantumCircuit, QuantumRegister
import crsq_arithmetic as ari
import crsq_arithmetic.bit_ops as bb
import crsq_arithmetic.test_tools as test_tools

def do_qsum(in_bits: list[int], out_bits: list[int], use_gate):
    """ test carry for one set of inputs and compare with expected output.
        in_bits: [ cin, a, b ]
    """
    qr = QuantumRegister(3)
    qc = QuantumCircuit(qr)
    ari.set_bits(qc, qr, in_bits)
    if use_gate:
        qc.append(bb.qsum_gate(), qr[:])
    else:
        bb.qsum(qc, qr[0], qr[1], qr[2])
    qc.save_statevector()
    expected = "".join(map(lambda x: bin(x)[-1:], reversed(out_bits)))
    exp_dict = {
        expected: 1
    }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_qsum():
    """ test qsum gate for all possible inputs
    """
    print("test_qsum")
    # [cin a b]
    for ug in [False,True]:
        do_qsum([0, 0, 0], [0, 0, 0], ug)
        do_qsum([0, 1, 0], [0, 1, 1], ug)
        do_qsum([0, 0, 1], [0, 0, 1], ug)
        do_qsum([0, 1, 1], [0, 1, 0], ug)
        do_qsum([1, 0, 0], [1, 0, 1], ug)
        do_qsum([1, 1, 0], [1, 1, 0], ug)
        do_qsum([1, 0, 1], [1, 0, 0], ug)
        do_qsum([1, 1, 1], [1, 1, 1], ug)


def do_iqsum(in_bits: list[int], out_bits: list[int], use_gate):
    """ test carry for one set of inputs and compare with expected output.
        in_bits: [ cin, a, b ]
    """
    qr = QuantumRegister(3)
    qc = QuantumCircuit(qr)
    ari.set_bits(qc, qr, in_bits)
    if use_gate:
        qc.append(bb.iqsum_gate(), qr[:])
    else:
        bb.iqsum(qc, qr[0], qr[1], qr[2])
    qc.save_statevector()
    expected = "".join(map(lambda x: bin(x)[-1:], reversed(out_bits)))
    exp_dict = {
        expected: 1
    }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_iqsum():
    """ test iqsum gate for all possible inputs
    """
    print("test_iqsum")
    # [cin a b]
    for ug in [False, True]:
        do_iqsum([0, 0, 0], [0, 0, 0], ug)
        do_iqsum([0, 1, 1], [0, 1, 0], ug)
        do_iqsum([0, 0, 1], [0, 0, 1], ug)
        do_iqsum([0, 1, 0], [0, 1, 1], ug)
        do_iqsum([1, 0, 1], [1, 0, 0], ug)
        do_iqsum([1, 1, 0], [1, 1, 0], ug)
        do_iqsum([1, 0, 0], [1, 0, 1], ug)
        do_iqsum([1, 1, 1], [1, 1, 1], ug)


def do_cqsum(in_bits: list[int], out_bits: list[int], use_gate):
    """ test carry for one set of inputs and compare with expected output.
        in_bits: [ cin, a, b ]
    """
    qr = QuantumRegister(4)
    qc = QuantumCircuit(qr)
    ari.set_bits(qc, qr, in_bits)
    if use_gate:
        qc.append(bb.cqsum_gate(), qr[:])
    else:
        bb.cqsum(qc, qr[0], qr[1], qr[2], qr[3])
    qc.save_statevector()
    expected = "".join(map(lambda x: bin(x)[-1:], reversed(out_bits)))
    exp_dict = {
        expected: 1
    }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_cqsum():
    """ test qsum gate for all possible inputs
    """
    print("test_cqsum")
    # [cin a b]
    for ug in [False, True]:
        do_cqsum([0, 0, 0, 0], [0, 0, 0, 0], ug)
        do_cqsum([0, 0, 1, 0], [0, 0, 1, 0], ug)
        do_cqsum([0, 0, 0, 1], [0, 0, 0, 1], ug)
        do_cqsum([0, 0, 1, 1], [0, 0, 1, 1], ug)
        do_cqsum([0, 1, 0, 0], [0, 1, 0, 0], ug)
        do_cqsum([0, 1, 1, 0], [0, 1, 1, 0], ug)
        do_cqsum([0, 1, 0, 1], [0, 1, 0, 1], ug)
        do_cqsum([0, 1, 1, 1], [0, 1, 1, 1], ug)

        do_cqsum([1, 0, 0, 0], [1, 0, 0, 0], ug)
        do_cqsum([1, 0, 1, 0], [1, 0, 1, 1], ug)
        do_cqsum([1, 0, 0, 1], [1, 0, 0, 1], ug)
        do_cqsum([1, 0, 1, 1], [1, 0, 1, 0], ug)
        do_cqsum([1, 1, 0, 0], [1, 1, 0, 1], ug)
        do_cqsum([1, 1, 1, 0], [1, 1, 1, 0], ug)
        do_cqsum([1, 1, 0, 1], [1, 1, 0, 0], ug)
        do_cqsum([1, 1, 1, 1], [1, 1, 1, 1], ug)


def do_qhsum(in_bits: list[int], out_bits: list[int], use_gate):
    """ test carry for one set of inputs and compare with expected output.
        in_bits: [ a, b ]
    """
    qr = QuantumRegister(2)
    qc = QuantumCircuit(qr)
    ari.set_bits(qc, qr, in_bits)
    if use_gate:
        qc.append(bb.qhsum_gate(), qr[:])
    else:
        bb.qhsum(qc, qr[0], qr[1])
    qc.save_statevector()
    expected = "".join(map(lambda x: bin(x)[-1:], reversed(out_bits)))
    exp_dict = {
        expected: 1
    }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_qhsum():
    """ test qsum gate for all possible inputs
    """
    print("test_qhsum")
    # [cin a b]
    for ug in [False, True]:
        do_qhsum([0, 0], [0, 0], ug)
        do_qhsum([1, 0], [1, 1], ug)
        do_qhsum([0, 1], [0, 1], ug)
        do_qhsum([1, 1], [1, 0], ug)


def do_iqhsum(out_bits: list[int], in_bits: list[int], use_gate):
    """ test carry for one set of inputs and compare with expected output.
        in_bits: [ a, b ]
    """
    qr = QuantumRegister(2)
    qc = QuantumCircuit(qr)
    ari.set_bits(qc, qr, in_bits)
    if use_gate:
        qc.append(bb.iqhsum_gate(), qr[:])
    else:
        bb.iqhsum(qc, qr[0], qr[1])
    qc.save_statevector()
    expected = "".join(map(lambda x: bin(x)[-1:], reversed(out_bits)))
    exp_dict = {
        expected: 1
    }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_iqhsum():
    """ test iqsum gate for all possible inputs
    """
    print("test_iqhsum")
    # [a b]
    for ug in [False, True]:
        do_iqhsum([0, 0], [0, 0], ug)
        do_iqhsum([1, 0], [1, 1], ug)
        do_iqhsum([0, 1], [0, 1], ug)
        do_iqhsum([1, 1], [1, 0], ug)


def do_cqhsum(in_bits: list[int], out_bits: list[int], use_gate):
    """ test carry for one set of inputs and compare with expected output.
        in_bits: [ ctrl, a, b ]
    """
    qr = QuantumRegister(3)
    qc = QuantumCircuit(qr)
    ari.set_bits(qc, qr, in_bits)
    if use_gate:
        qc.append(bb.cqhsum_gate(), qr[:])
    else:
        bb.cqhsum(qc, qr[0], qr[1], qr[2])
    qc.save_statevector()
    expected = "".join(map(lambda x: bin(x)[-1:], reversed(out_bits)))
    exp_dict = {
        expected: 1
    }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_cqhsum():
    """ test qsum gate for all possible inputs
    """
    print("test_cqhsum")
    # [cin a b]
    for ug in [False, True]:
        do_cqhsum([0, 0, 0], [0, 0, 0], ug)
        do_cqhsum([0, 1, 0], [0, 1, 0], ug)
        do_cqhsum([0, 0, 1], [0, 0, 1], ug)
        do_cqhsum([0, 1, 1], [0, 1, 1], ug)

        do_cqhsum([1, 0, 0], [1, 0, 0], ug)
        do_cqhsum([1, 1, 0], [1, 1, 1], ug)
        do_cqhsum([1, 0, 1], [1, 0, 1], ug)
        do_cqhsum([1, 1, 1], [1, 1, 0], ug)


def do_cosum(in_bits: list[int], out_bits: list[int], use_gate):
    """ test carry for one set of inputs and compare with expected output.
        in_bits: [ cin, y, b ]
    """
    qr = QuantumRegister(2)
    qc = QuantumCircuit(qr)
    ari.set_bits(qc, qr, in_bits[0:1] + in_bits[2:3])
    if use_gate:
        qc.append(bb.cosum_gate(in_bits[1]), qr[:])
    else:
        bb.cosum(qc, qr[0], in_bits[1], qr[1])
    qc.save_statevector()
    expected = "".join(map(lambda x: bin(x)[-1:], reversed(out_bits)))
    exp_dict = {
        expected: 1
    }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_cosum():
    """ test qsum gate for all possible inputs
    """
    print("test_cosum")
    # [cin a b]
    for ug in [False,True]:
        do_cosum([0, 0, 0], [0, 0], ug)
        do_cosum([0, 1, 0], [0, 1], ug)
        do_cosum([0, 0, 1], [0, 1], ug)
        do_cosum([0, 1, 1], [0, 0], ug)
        do_cosum([1, 0, 0], [1, 1], ug)
        do_cosum([1, 1, 0], [1, 0], ug)
        do_cosum([1, 0, 1], [1, 0], ug)
        do_cosum([1, 1, 1], [1, 1], ug)


def do_icosum(in_bits: list[int], out_bits: list[int], use_gate):
    """ test carry for one set of inputs and compare with expected output.
        in_bits: [ cin, y, b ]
    """
    qr = QuantumRegister(2)
    qc = QuantumCircuit(qr)
    ari.set_bits(qc, qr, in_bits[0:1] + in_bits[2:3])
    if use_gate:
        qc.append(bb.icosum_gate(in_bits[1]), qr[:])
    else:
        bb.icosum(qc, qr[0], in_bits[1], qr[1])
    qc.save_statevector()
    expected = "".join(map(lambda x: bin(x)[-1:], reversed(out_bits)))
    exp_dict = {
        expected: 1
    }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_icosum():
    """ test iqsum gate for all possible inputs
    """
    print("test_icosum")
    # [cin a b]
    for ug in [False, True]:
        do_icosum([0, 0, 0], [0, 0], ug)
        do_icosum([0, 1, 1], [0, 0], ug)
        do_icosum([0, 0, 1], [0, 1], ug)
        do_icosum([0, 1, 0], [0, 1], ug)
        do_icosum([1, 0, 1], [1, 0], ug)
        do_icosum([1, 1, 0], [1, 0], ug)
        do_icosum([1, 0, 0], [1, 1], ug)
        do_icosum([1, 1, 1], [1, 1], ug)


def do_cohsum(in_bits: list[int], out_bits: list[int], use_gate):
    """ test carry for one set of inputs and compare with expected output.
        in_bits: [ y, b ]
    """
    qr = QuantumRegister(1)
    qc = QuantumCircuit(qr)
    ari.set_bits(qc, qr, in_bits[1:2])
    if use_gate:
        qc.append(bb.cohsum_gate(in_bits[0]), qr[:])
    else:
        bb.cohsum(qc, in_bits[0], qr[0])
    qc.save_statevector()
    expected = "".join(map(lambda x: bin(x)[-1:], reversed(out_bits)))
    exp_dict = {
        expected: 1
    }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_cohsum():
    """ test qsum gate for all possible inputs
    """
    print("test_cohsum")
    # [cin a b]
    for ug in [False,True]:
        do_cohsum([0, 0], [0], ug)
        do_cohsum([1, 0], [1], ug)
        do_cohsum([0, 1], [1], ug)
        do_cohsum([1, 1], [0], ug)


def do_icohsum(in_bits: list[int], out_bits: list[int], use_gate):
    """ test carry for one set of inputs and compare with expected output.
        in_bits: [ y, b ]
    """
    qr = QuantumRegister(1)
    qc = QuantumCircuit(qr)
    ari.set_bits(qc, qr, in_bits[1:2])
    if use_gate:
        qc.append(bb.icohsum_gate(in_bits[0]), qr[:])
    else:
        bb.icohsum(qc, in_bits[0], qr[0])
    qc.save_statevector()
    expected = "".join(map(lambda x: bin(x)[-1:], reversed(out_bits)))
    exp_dict = {
        expected: 1
    }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_icohsum():
    """ test icohsum gate for all possible inputs
    """
    print("test_icohsum")
    # [cin a b]
    for ug in [False, True]:
        do_icohsum([0, 0], [0], ug)
        do_icohsum([1, 1], [0], ug)
        do_icohsum([0, 1], [1], ug)
        do_icohsum([1, 0], [1], ug)


if __name__ == '__main__':
    test_qsum()
    test_iqsum()
    test_cqsum()

    test_qhsum()
    test_iqhsum()
    test_cqhsum()

    test_cosum()
    test_icosum()

    test_cohsum()
    test_icohsum()
