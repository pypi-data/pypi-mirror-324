""" Multiplier Gates
"""

from qiskit.circuit import QuantumCircuit, QuantumRegister, Gate
from crsq_arithmetic.adder import unsigned_adder, unsigned_adder_gate

import crsq_arithmetic.utils as ut


def unsigned_multiplier(qc: QuantumCircuit, ar: QuantumRegister,
                        br: QuantumRegister, dr: QuantumRegister,
                        cr1: QuantumRegister, cr2: QuantumRegister):
    """ Emit an unsigned multiplier circuit.

        Effect:
            [ar, br, dr=0, cr1=0, cr2=0] -> [ar, br, dr=ar*br, cr1=0, cr2=0]

        :param qc: target circuit
        :param ar: left (n bits)
        :param br: right (n bits)
        :param dr: product (2*n bits)
        :param cr1: carry for the multiplier (n bits)
        :param cr2: carry for the internal adder (n-1 bits)
    """
    n = ut.bitsize(ar)
    if not (ut.bitsize(br) == n and ut.bitsize(cr1) == n and
            ut.bitsize(cr2) == n - 1  and ut.bitsize(dr) == n * 2):
        raise ValueError(
            f"size mismatch: ar[{ut.bitsize(ar)}], br[{ut.bitsize(br)}]," +
            f" cr1[{ut.bitsize(cr1)}], cr2[{ut.bitsize(cr2)}], dr[{ut.bitsize(dr)}]")
    for k in range(n):
        qc.ccx(ar[k], br[0], dr[k])
    for j in range(1, n):
        for k in range(n):
            qc.ccx(ar[k], br[j], cr1[k])
#        unsigned_adder(qc, cr1, register_range(dr, j, n + 1), cr2)
        qc.append(unsigned_adder_gate(n), cr1[:] + ut.register_range(dr, j, n + 1)[:] + cr2[:])
        for k in range(n-1, -1, -1):
            qc.ccx(ar[k], br[j], cr1[k])


def unsigned_multiplier_gate(n: int, label: str="umult") -> Gate:
    """ Create an unsigned multiplier gate.

        Usage:
            qc.append(unsigned_multiplier_gate(n),
              [a1...an, b1...bn, d1...d2n, c11...c1n, c21...c2n])

        Effect:
            [a, b, d=0, c1=0, c2=0] -> [a, b, a*b, c1=0, c2=0]

        :param n: bit size of a
        :param label: label to put on the gate
    """
    ar = QuantumRegister(n, name="a")
    br = QuantumRegister(n, name="b")
    dr = QuantumRegister(2*n, "d")
    c1 = QuantumRegister(n, "c1")
    c2 = QuantumRegister(n - 1, "c2")
    qc = QuantumCircuit(ar, br, dr, c1, c2)
    unsigned_multiplier(qc, ar, br, dr, c1, c2)
    return qc.to_gate(label=f"{label}({n})")


def signed_multiplier(qc: QuantumCircuit, ar: QuantumRegister,
                      br: QuantumRegister, dr: QuantumRegister,
                      cr1: QuantumRegister, cr2: QuantumRegister,
                      use_gates: bool = False):
    """ Emit a signed multiplier circuit.

        Effect:
            [ar, br, dr=0, cr1=0, cr2=0] -> [ar, br, ar*br, cr1=0, cr2=0]
        
        :param qc: target circuit
        :param ar: left (n bits)
        :param br: right (n bits)
        :param dr: product (2*n bits)
        :param cr1: carry for the multiplier (n bits)
        :param cr2: carry for the internal adder (n - 1 bits)
    """
    n = ut.bitsize(ar)
    if not (ut.bitsize(br) == n and ut.bitsize(cr1) == n and
            ut.bitsize(cr2) == n - 1 and ut.bitsize(dr) == n * 2):
        raise ValueError(
            f"size mismatch: ar[{ut.bitsize(ar)}], br[{ut.bitsize(br)}]," +
            f" cr1[{ut.bitsize(cr1)}], cr2[{ut.bitsize(cr2)}], dr[{ut.bitsize(dr)}]")
    if use_gates:
        qc.x(dr[n])
        qc.x(dr[2*n-1])
        # j = 0 case is special
        j = 0
        for k in range(n):
            qc.ccx(ar[k], br[j], dr[k])
        qc.x(dr[n-1])
        # j = [1, n-1) follows a pattern
        for j in range(1, n-1):
            for k in range(n):
                qc.ccx(ar[k], br[j], cr1[k])
            qc.x(cr1[n-1])
            qc.append(unsigned_adder_gate(n), cr1[:] + ut.register_range(dr, j, n + 1)[:] + cr2[:])
            qc.x(cr1[n-1])
            for k in range(n - 1, -1, -1):
                qc.ccx(ar[k], br[j], cr1[k])
        # j = n -1 is special
        j = n - 1
        for k in range(n):
            qc.ccx(ar[k], br[j], cr1[k])
        for k in range(n - 1):
            qc.x(cr1[k])
        qc.append(unsigned_adder_gate(n), cr1[:] + ut.register_range(dr, j, n + 1)[:] + cr2[:])
        for k in range(n - 1 - 1, -1, -1):
            qc.x(cr1[k])
        for k in range(n - 1, -1, -1):
            qc.ccx(ar[k], br[j], cr1[k])
    else:
        qc.x(dr[n])
        qc.x(dr[2*n-1])
        # j = 0 case is special
        j = 0
        for k in range(n):
            qc.ccx(ar[k], br[j], dr[k])
        qc.x(dr[n-1])
        # j = [1, n-1) follows a pattern
        for j in range(1, n-1):
            for k in range(n):
                qc.ccx(ar[k], br[j], cr1[k])
            qc.x(cr1[n-1])
            unsigned_adder(qc, cr1, ut.register_range(dr, j, n + 1), cr2)
            qc.x(cr1[n-1])
            for k in range(n - 1, -1, -1):
                qc.ccx(ar[k], br[j], cr1[k])
        # j = n -1 is special
        j = n - 1
        for k in range(n):
            qc.ccx(ar[k], br[j], cr1[k])
        for k in range(n - 1):
            qc.x(cr1[k])
        unsigned_adder(qc, cr1, ut.register_range(dr, j, n + 1), cr2)
        for k in range(n - 1 - 1, -1, -1):
            qc.x(cr1[k])
        for k in range(n - 1, -1, -1):
            qc.ccx(ar[k], br[j], cr1[k])


def signed_multiplier_gate(n: int, label: str="smult") -> Gate:
    """ Create a signed multiplier gate.
        
        Usage:
            qc.append(signed_multiplier_gate(n), [a1...an, b1...bn, d1...d2n, c11...c1n, c21...c2n])
        
        Effect:
            [a, b, d, c1=0, c2=0] -> [a, b, a*b, c1=0, c2=0]
        
        :param n: bit size of a
        :param label: label to put on the gate
    """
    ar = QuantumRegister(n, name="a")
    br = QuantumRegister(n, name="b")
    dr = QuantumRegister(2*n, "d")
    c1 = QuantumRegister(n, "c1")
    c2 = QuantumRegister(n - 1, "c2")
    qc = QuantumCircuit(ar, br, dr, c1, c2)
    signed_multiplier(qc, ar, br, dr, c1, c2)
    return qc.to_gate(label=f"{label}({n})")
