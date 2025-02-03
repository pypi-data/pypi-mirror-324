""" Arithmetic utilities
"""
from qiskit.circuit import QuantumCircuit, QuantumRegister
from qiskit.circuit.quantumcircuit import QubitSpecifier

def bitsize(reg_or_list) -> int:
    """ Get the number of quantum bits from a var which is
        either a QuantumRegister or a list.
    """
    if type(reg_or_list) is QuantumRegister:
        return reg_or_list.size
    if type(reg_or_list) is list:
        return len(reg_or_list)
    raise TypeError(f"Unexpected type: {type(reg_or_list)}")


def register_range(qr: QuantumRegister, start: int, length: int) -> list:
    """ extract a list of bits from a register
    """
    if length == 0:
        return []
    res = [qr[i] for i in range(start, start+length)]
    return res


def set_value(circ: QuantumCircuit, qr: QuantumRegister, val: int):
    """ Decompose an integer value into bits and set them
        to a quantum register.

        :param circ: The circuit for the register.
        :param qr: The target register.
        :param val: Value to set to the register.
    """
    n = qr.size
    for k in range(n):
        mask = 1 << k
        if val & mask:
            circ.x(qr[k])


def set_bit(circ: QuantumCircuit, qb: QubitSpecifier, flag: bool):
    """ Set a value, which is a compile-time constant bool to a bit.
        An X gate on the specified bit will be emitted if the value is true.

        :param circ: target circuit
        :param qb: the bit to set
        :param flag: the value to set to the bit
    """
    if flag:
        circ.x(qb)


def set_bits(circ: QuantumCircuit, qr: QuantumRegister, bits: list[int]):
    """ Insert an X gate on bits of qr when the corresponding
        bit in bits is true.
    """
    for k, bit in enumerate(bits):
        if bit:
            circ.x(qr[k])
