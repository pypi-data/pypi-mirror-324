""" Bitwise operations for arithmetic

    Carry gates:
    carry, carry_gate, icarry, icarry_gate, ccarry, ccarry_gate, cicarry, cicarry_gate,
    hcarry, hcarry_gate, ihcarry, ihcarry_gate, chcarry, chcarry_gate, cihcarry, cihcarry_gate
     
    cocarry, cocarry_gate, icocarry, icocarry_gate
    cohcarry, cohcarry_gate, ihcarry, ihcarry_gate

    Sum gates
    qsum, qsum_gate, iqsum, iqsum_gate, cqsum, cqsum_gate
    qhsum, qhsum_gate, iqhsum, iqhsum_gate, cqhsum, cqhsum_gate

    cosum, cosum_gate, icosum, icosum_gate
    cohsum, cohsum_gate, icohsum, icohsum_gate
"""

from qiskit.circuit import QuantumCircuit, Gate
from qiskit.circuit.library.standard_gates.x import C3XGate
from qiskit.circuit.quantumcircuit import QubitSpecifier


def carry(qc: QuantumCircuit, cin: QubitSpecifier,
           a: QubitSpecifier, b: QubitSpecifier, cout: QubitSpecifier):
    """ Emit a 1 qubit carry.
    """
    qc.ccx(a, b, cout)
    qc.cx(a, b)
    qc.ccx(cin, b, cout)


def carry_gate(label: str="carry") -> Gate:
    """ Emit a 1 qubit carry.

        - [0] : cin
        - [1] : a
        - [2] : b
        - [3] : cout
    """
    qc = QuantumCircuit(4)
    qc.ccx(1, 2, 3)
    qc.cx(1, 2)
    qc.ccx(0, 2, 3)
    return qc.to_gate(label=label)


def icarry(qc: QuantumCircuit, cin: QubitSpecifier,
            a: QubitSpecifier, b: QubitSpecifier, cout: QubitSpecifier):
    """ Emit 1 reversed qubit carry
    """
    qc.ccx(cin, b, cout)
    qc.cx(a, b)
    qc.ccx(a, b, cout)


def icarry_gate(label: str="icarry") -> Gate:
    """ Emit 1 reversed qubit carry

        - [0] cin
        - [1] a
        - [2] b
        - [3] cout
    """
    qc = QuantumCircuit(4)
    qc.ccx(0, 2, 3)
    qc.cx(1, 2)
    qc.ccx(1, 2, 3)
    return qc.to_gate(label=label)


def ccarry(qc: QuantumCircuit, cbit: QubitSpecifier,
            cin: QubitSpecifier,
            a: QubitSpecifier, b: QubitSpecifier, cout: QubitSpecifier):
    """ Emit 1 controlled qubit carry
    """
    qc.append(C3XGate(), [cbit, a, b, cout], [])
    qc.ccx(cbit, a, b)
    qc.append(C3XGate(), [cbit, cin, b, cout], [])


def ccarry_gate():
    """ Controlled carry gate """
    return carry_gate().control(1)


def cicarry(qc: QuantumCircuit,
             cbit: QubitSpecifier, cin: QubitSpecifier,
             a: QubitSpecifier, b: QubitSpecifier, cout: QubitSpecifier):
    """ Emit a controlled reversed qubit carry
    """
    qc.append(C3XGate(), [cbit, cin, b, cout], [])
    qc.ccx(cbit, a, b)
    qc.append(C3XGate(), [cbit, a, b, cout], [])


def cicarry_gate() -> Gate:
    """ Emit a controlled reversed qubit carry gate"""
    return icarry_gate().control(1)


def hcarry(qc: QuantumCircuit,
           a: QubitSpecifier, b: QubitSpecifier, cout: QubitSpecifier):
    """ Emit a 1 qubit half carry.
    """
    qc.ccx(a, b, cout)
    qc.cx(a, b)


def hcarry_gate(label: str="hcarry") -> Gate:
    """ Emit a 1 qubit hafl carry gate.

        - [0] : a
        - [1] : b
        - [2] : cout
    """
    qc = QuantumCircuit(3)
    qc.ccx(0, 1, 2)
    qc.cx(0, 1)
    return qc.to_gate(label=label)


def ihcarry(qc: QuantumCircuit,
           a: QubitSpecifier, b: QubitSpecifier, cout: QubitSpecifier):
    """ Emit a 1 qubit reversed half carry.
    """
    qc.cx(a, b)
    qc.ccx(a, b, cout)


def ihcarry_gate(label: str="ihcarry") -> Gate:
    """ Emit a 1 qubit reversed half carry gate.

        - [0] : a
        - [1] : b
        - [2] : cout
    """
    qc = QuantumCircuit(3)
    qc.cx(0, 1)
    qc.ccx(0, 1, 2)
    return qc.to_gate(label=label)


def chcarry(qc: QuantumCircuit, cbit: QubitSpecifier,
            a: QubitSpecifier, b: QubitSpecifier, cout: QubitSpecifier):
    """ Emit 1 controlled qubit half carry
    """
    qc.append(C3XGate(), [cbit, a, b, cout], [])
    qc.ccx(cbit, a, b)


def chcarry_gate():
    """ Controlled carry gate """
    return hcarry_gate().control(1)


def cihcarry(qc: QuantumCircuit,
             cbit: QubitSpecifier,
             a: QubitSpecifier, b: QubitSpecifier, cout: QubitSpecifier):
    """ Emit a controlled reversed qubit carry
    """
    qc.ccx(cbit, a, b)
    qc.append(C3XGate(), [cbit, a, b, cout])


def cihcarry_gate() -> Gate:
    """ Emit a controlled reversed qubit carry gate"""
    return ihcarry_gate().control(1)


def cocarry(qc: QuantumCircuit, cin: QubitSpecifier,
              ybit: int, b: QubitSpecifier, cout: QubitSpecifier):
    """ Emit carry for constant ybit and qubit b to cout.
        Takes cin.
    """
    if ybit == 0:
        qc.ccx(cin, b, cout)
    else:
        qc.cx(b, cout)
        qc.x(b)
        qc.ccx(cin, b, cout)


def cocarry_gate(ybit: int, label: str = "cocarry") -> Gate:
    """ Emit carry for constant ybit and qubit b to cout.
        Takes cin.

        - [0] cin
        - [1] b
        - [2] cout
    """
    qc = QuantumCircuit(3)
    if ybit == 0:
        qc.ccx(0, 1, 2)
    else:
        qc.cx(1, 2)
        qc.x(1)
        qc.ccx(0, 1, 2)
    return qc.to_gate(label=f"{label}({ybit})")


def icocarry(qc: QuantumCircuit, cin: QubitSpecifier,
               ybit: int, b: QubitSpecifier, cout: QubitSpecifier):
    """ Emit inverse carry for constant ybit and qubit b to cout.
        Takes cin.
    """
    if ybit == 0:
        qc.ccx(cin, b, cout)
    else:
        qc.ccx(cin, b, cout)
        qc.x(b)
        qc.cx(b, cout)


def icocarry_gate(ybit: int, label: str = "icocarry") -> Gate:
    """ Emit inverse carry for constant ybit and qubit b to cout.
        Takes cin.

        - [0] cin
        - [1] b
        - [2] cout
    """
    qc = QuantumCircuit(3)
    if ybit == 0:
        qc.ccx(0, 1, 2)
    else:
        qc.ccx(0, 1, 2)
        qc.x(1)
        qc.cx(1, 2)
    return qc.to_gate(label=f"{label}({ybit})")


def cohcarry(qc: QuantumCircuit, ybit: int,
             b: QubitSpecifier, cout: QubitSpecifier):
    """ Constant input half carry.
    
        Emit a carry for constant ybit and qubit b to cout.
        Does not take cin.
    """
    if ybit == 0:
        pass
    else:
        qc.cx(b, cout)
        qc.x(b)


def cohcarry_gate(ybit: int, label: str = "cohcarry") -> Gate:
    """ Constant input half carry gate.
        Emit a carry for constant ybit and qubit b to cout.
        Does not take cin.

        - [0] b
        - [1] cout
    """
    qc = QuantumCircuit(2)
    if ybit == 0:
        pass
    else:
        qc.cx(0, 1)
        qc.x(0)
    return qc.to_gate(label=f"{label}({ybit})")


def icohcarry(qc: QuantumCircuit, ybit: int,
              b: QubitSpecifier, cout: QubitSpecifier):
    """ Emit an inverse carry for constant ybit and qubit b to cout.
        Does not take cin.
        - [0] b
        - [1] cout
    """
    if ybit == 0:
        pass
    else:
        qc.x(b)
        qc.cx(b, cout)


def icohcarry_gate(ybit: int, label: str = "icohcarry"):
    """ Emit an inverse carry for constant ybit and qubit b to cout.
        Does not take cin.
        - [0] b
        - [1] cout
    """
    qc = QuantumCircuit(2)
    if ybit == 0:
        pass
    else:
        qc.x(0)
        qc.cx(0, 1)
    return qc.to_gate(label=f"{label}({ybit})")


def qsum(qc: QuantumCircuit, cin: QubitSpecifier,
          a: QubitSpecifier, b: QubitSpecifier):
    """ Emit a 1 qubit sum
    """
    qc.cx(a, b)
    qc.cx(cin, b)


def qsum_gate(label: str="qsum") -> Gate:
    """ Emit a 1 qubit sum

        - [0] cin
        - [1] a
        - [2] b
    """
    qc = QuantumCircuit(3)
    qc.cx(1, 2)
    qc.cx(0, 2)
    return qc.to_gate(label=label)


def iqsum(qc: QuantumCircuit, cin: QubitSpecifier,
           a: QubitSpecifier, b: QubitSpecifier):
    """ emit 1 reversed qubit sum
    """
    qc.cx(cin, b)
    qc.cx(a, b)


def iqsum_gate(label: str = "iqsum"):
    """ emit 1 reversed qubit sum
        - [0] cin
        - [1] a
        - [2] b
    """
    qc = QuantumCircuit(3)
    qc.cx(0, 2)
    qc.cx(1, 2)
    return qc.to_gate(label=label)


def cqsum(qc: QuantumCircuit,
           cbit: QubitSpecifier, cin: QubitSpecifier,
           a: QubitSpecifier, b: QubitSpecifier):
    """ emit 1 controlled qubit sum
    """
    qc.ccx(cbit, a, b)
    qc.ccx(cbit, cin, b)


def cqsum_gate():
    """ emit 1 controlled qubit sum gate """
    return qsum_gate().control(1)


def qhsum(qc: QuantumCircuit,
          a: QubitSpecifier, b: QubitSpecifier):
    """ Emit a 1 qubit sum
    """
    qc.cx(a, b)


def qhsum_gate(label: str="qhsum") -> Gate:
    """ Emit a 1 qubit sum

        - [0] a
        - [1] b
    """
    qc = QuantumCircuit(2)
    qc.cx(0, 1)
    return qc.to_gate(label=label)


def iqhsum(qc: QuantumCircuit,
          a: QubitSpecifier, b: QubitSpecifier):
    """ Emit a 1 qubit sum
    """
    qc.cx(a, b)


def iqhsum_gate(label: str="iqhsum") -> Gate:
    """ Emit a 1 qubit sum

        - [0] a
        - [1] b
    """
    qc = QuantumCircuit(2)
    qc.cx(0, 1)
    return qc.to_gate(label=label)


def cqhsum(qc: QuantumCircuit,
           cbit: QubitSpecifier,
           a: QubitSpecifier, b: QubitSpecifier):
    """ emit 1 controlled qubit sum
    """
    qc.ccx(cbit, a, b)


def cqhsum_gate():
    """ emit 1 controlled qubit sum gate """
    return qhsum_gate().control(1)


def cosum(qc: QuantumCircuit, cin: QubitSpecifier,
          ybit: int, b: QubitSpecifier):
    """ constant operand sum.
    
        Emit sum of constant ybit and qubit b to b.
        Takes cin.
    """
    if ybit == 0:
        qc.cx(cin, b)
    else:
        qc.x(b)
        qc.cx(cin, b)


def cosum_gate(ybit: int, label: str="cosum") -> Gate:
    """ Emit sum of constant ybit and qubit b to b.
        Takes cin.

        - [0] cin
        - [1] b
    """
    qc = QuantumCircuit(2)
    if ybit == 0:
        qc.cx(0, 1)
    else:
        qc.x(1)
        qc.cx(0, 1)
    return qc.to_gate(label=f"{label}({ybit})")


def icosum(qc: QuantumCircuit, cin: QubitSpecifier,
           ybit: int, b: QubitSpecifier):
    """ Emit inverse of cosumc.
        Takes cin.
    """
    if ybit == 0:
        qc.cx(cin, b)
    else:
        qc.cx(cin, b)
        qc.x(b)


def icosum_gate(ybit: int, label: str="icosum") -> Gate:
    """ Emit inverse of cosumc
        Takes cin.

        - [0] cin
        - [1] b
    """
    qc = QuantumCircuit(2)
    if ybit == 0:
        qc.cx(0, 1)
    else:
        qc.cx(0, 1)
        qc.x(1)
    return qc.to_gate(label=f"{label}({ybit})")


def cohsum(qc: QuantumCircuit, ybit: int, b: QubitSpecifier):
    """ Emit sum of constant ybit and qubit b to b.
        does not take cin.
    """
    if ybit == 0:
        pass
    else:
        qc.x(b)


def cohsum_gate(ybit: int, label="cohsum"):
    """ Emit sum of constant ybit and qubit b to b.
        does not take cin.
        This can also be used as icosum_gate

        - [0] : b
    """
    qc = QuantumCircuit(1)
    if ybit == 0:
        pass
    else:
        qc.x(0)
    return qc.to_gate(label=f"{label}({ybit})")


def icohsum(qc: QuantumCircuit, ybit: int, b:QubitSpecifier):
    """ Emit inverse of cosum, which is the same as cosum."""
    cohsum(qc, ybit, b)


def icohsum_gate(ybit: int, label="icohsum"):
    """ Create an icosum gate, which is identical to cosum_gate
        (except for the label)
    """
    return cohsum_gate(ybit, label)
