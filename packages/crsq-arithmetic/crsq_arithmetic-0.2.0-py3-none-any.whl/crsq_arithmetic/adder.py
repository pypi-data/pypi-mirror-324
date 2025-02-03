""" Adder gates
"""
from qiskit.circuit import QuantumCircuit, QuantumRegister, Gate
from qiskit.circuit.library import C3XGate
from qiskit.circuit.quantumcircuit import QubitSpecifier

import crsq_arithmetic.bit_ops as bb
import crsq_arithmetic.utils as ut

def unsigned_coadder(qc: QuantumCircuit, y: int,
                   br: QuantumRegister, cr: QuantumRegister, use_gates: bool=False):
    """ Emit an n bit constant adder circuit

        Effect:
          [y, br, cr=0] -> [y, br+y, cr = 0]

        :param qc: target circuit
        :param y: left (circuit build time constant)
        :param br: right (n+1 bits)
        :param cr: carry (n-1 bits)
    """
    n = ut.bitsize(br) - 1
    if not (ut.bitsize(br) == n+1 and ut.bitsize(cr) == n-1):
        raise ValueError(
            f"size mismatch: ar[{n}], cr[{ut.bitsize(cr)}]")
    if use_gates:
        k = 0
        ybit = y & 1
        qc.append(bb.cohcarry_gate(ybit), [br[k], cr[k]])
        for k in range(1, n-1):
            ybit = (y >> k) & 1
            qc.append(bb.cocarry_gate(ybit), [cr[k-1], br[k], cr[k]])
        k = n - 1
        ybit = (y >> k) & 1
        qc.append(bb.cocarry_gate(ybit), [cr[k-1], br[k], br[k+1]])
        if ybit:
            qc.x(br[k])
        qc.append(bb.coqsum_gate(y), [cr[k-1], br[k]])

        for k in range(n-2, 0, -1):
            ybit = (y >> k) & 1
            qc.append(bb.icocarry_gate(ybit), [cr[k-1], y, br[k], cr[k]])
            qc.append(bb.cosum_gate(ybit), [cr[k-1], br[k]])

        k = 0
        ybit = y & 1
        qc.append(bb.icohcarry_gate(ybit), [br[k], cr[k]])
        qc.append(bb.cosum_gate(ybit), [cr[k], br[k]])
    else:
        k = 0
        ybit = y & 1
        bb.cohcarry(qc, ybit, br[k], cr[k])
        for k in range(1, n-1):
            ybit = (y >> k) & 1
            bb.cocarry(qc, cr[k-1], y, br[k], cr[k])

        k = n - 1
        ybit = (y >> k) & 1
        bb.cocarry(qc, cr[k-1], ybit, br[k], br[k+1])
        if ybit:
            qc.x(br[k])
        bb.cosum(qc, cr[k-1], ybit, br[k])

        for k in range(n-2, 0, -1):
            ybit = (y >> k) & 1
            bb.icocarry(qc, cr[k-1], ybit, br[k], cr[k])
            bb.cosum(qc, cr[k-1], ybit, br[k])

        k = 0
        ybit = y & 1
        bb.icohcarry(qc, ybit, br[k], cr[k])
        bb.cohsum(qc, ybit, br[k])

def unsigned_coadder_gate(n: int, y: int, label: str="ucoadd", use_gates: bool=False) -> Gate:
    """ Create an unsigned constant adder gate.

        Usage:
          qc.append(unsigned_coadder_gate(n, y), [b1,...,bn, c1,...,cn-1])

        Effect:
          [y, b, c=0] -> [y, b+y, c=0]

        :param n: bit size of b - 1
        :param y: constant value to add
        :param label: label to put on the gate
    """
    br = QuantumRegister(n+1, "b")
    cr = QuantumRegister(n-1, "c")
    qc = QuantumCircuit(br, cr)
    unsigned_coadder(qc, y, br, cr, use_gates=use_gates)
    return qc.to_gate(label=f"{label}({n},{y})")

def unsigned_adder(qc: QuantumCircuit, ar: QuantumRegister,
                   br: QuantumRegister, cr: QuantumRegister, use_gates: bool=False):
    """ Emit an n bit adder circuit

        Effect:
          [ar, br, cr=0] -> [ar, br+ar, cr = 0]

        :param qc: target circuit
        :param ar: left (n bits)
        :param br: right (n+1 bits)
        :param cr: carry (n-1 bits)
    """
    n = ut.bitsize(ar)
    if not (ut.bitsize(br) == n+1 and ut.bitsize(cr) == n-1):
        raise ValueError(
            f"size mismatch: ar[{n}], br[{ut.bitsize(br)}], cr[{ut.bitsize(cr)}]")
    if use_gates:
        k = 0
        qc.append(bb.hcarry_gate(), [ar[k], br[k], cr[k]])
        for k in range(1, n-1):
            qc.append(bb.carry_gate(), [cr[k-1], ar[k], br[k], cr[k]])

        k = n - 1
        qc.append(bb.carry_gate(), [cr[k-1], ar[k], br[k], br[k+1]])
        qc.cx(ar[k], br[k])
        qc.append(bb.qsum_gate(), [cr[k-1], ar[k], br[k]])

        for k in range(n-2, 0, -1):
            qc.append(bb.icarry_gate(), [cr[k-1], ar[k], br[k], cr[k]])
            qc.append(bb.qsum_gate(), [cr[k-1], ar[k], br[k]])

        k = 0
        qc.append(bb.ihcarry_gate(), [ar[k], br[k], cr[k]])
        qc.append(bb.qsum_gate(), [cr[k], ar[k], br[k]])
    else:
        k = 0
        bb.hcarry(qc, ar[k], br[k], cr[k])
        for k in range(1, n-1):
            bb.carry(qc, cr[k-1], ar[k], br[k], cr[k])

        k = n - 1
        bb.carry(qc, cr[k-1], ar[k], br[k], br[k+1])
        qc.cx(ar[k], br[k])
        bb.qsum(qc, cr[k-1], ar[k], br[k])

        for k in range(n-2, 0, -1):
            bb.icarry(qc, cr[k-1], ar[k], br[k], cr[k])
            bb.qsum(qc, cr[k-1], ar[k], br[k])

        k = 0
        bb.ihcarry(qc, ar[k], br[k], cr[k])
        bb.qhsum(qc, ar[k], br[k])


def unsigned_adder_gate(n: int, label: str="uadd", use_gates: bool=False) -> Gate:
    """ Crete an unsigned adder gate.
     
        Usage:
          qc.append(unsigned_adder_gate(n), [a1,...,an, b1,...,bn+1, c1,...,cn])

        Effect:
          [a, b, c=0] -> [a, b+a, c=0]
        
        :param n: bit size of a
        :param label: label for the gate.
    """
    ar = QuantumRegister(n, name="a")
    br = QuantumRegister(n+1, name="b")
    cr = QuantumRegister(n-1, "c")
    qc = QuantumCircuit(ar, br, cr)
    unsigned_adder(qc, ar, br, cr, use_gates=use_gates)
    return qc.to_gate(label=f"{label}({n})")


def unsigned_adderv(qc: QuantumCircuit, ar: QuantumRegister,
                    br: QuantumRegister, cr: QuantumRegister,
                    use_gates = True):
    """ Emit an n bit adder circuit.

        This version supports unmatched register sizes.

        Effect:
            [ar, br, cr=0] -> [ar, br+ar, cr=0]
        
        :param qc: target circuit
        :param ar: left (m bits)
        :param br: right (n+1 bits (n >= m))
        :param cr: carry (n-1 bits)
    """
    m = ut.bitsize(ar)
    n = ut.bitsize(br)-1
    if not (n >= m and ut.bitsize(cr) == n - 1):
        raise ValueError(
            f"size mismatch: ar[{m}], br[{n}], cr[{ut.bitsize(cr)}]")
    if use_gates:
        k = 0
        if k < n - 1:
            qc.append(bb.hcarry_gate(), [ar[k], br[k], cr[k]])
        for k in range(1, n-1):
            if k < m:
                qc.append(bb.carry_gate(), [cr[k-1], ar[k], br[k], cr[k]])
            else:
                qc.ccx(cr[k-1], br[k], cr[k])

        k = n-1
        if k < m:
            if k == 0:
                # special case
                qc.append(bb.hcarry_gate(), [ar[k], br[k], br[k+1]])
                qc.cx(ar[k], br[k])
                qc.append(bb.qhsum_gate(), [ar[k], br[k]])
            else:
                qc.append(bb.carry_gate(), [cr[k-1], ar[k], br[k], br[k+1]])
                qc.cx(ar[k], br[k])
                qc.append(bb.qsum_gate(), [cr[k-1], ar[k], br[k]])
        else:
            qc.ccx(cr[k-1], br[k], br[k+1])
            qc.cx(cr[k-1], br[k])

        for k in range(n-2, 0, -1):
            if k < m:
                qc.append(bb.icarry_gate(), [cr[k-1], ar[k], br[k], cr[k]])
                qc.append(bb.qsum_gate(), [cr[k-1], ar[k], br[k]])
            else:
                qc.ccx(cr[k-1], br[k], cr[k])
                qc.cx(cr[k-1], br[k])
        k = 0
        if k < n - 1:
            qc.append(bb.ihcarry_gate(), [ar[k], br[k], cr[k]])
            qc.append(bb.qhsum_gate(), [ar[k], br[k]])

    else:
        k = 0
        if k < n - 1:
            bb.hcarry(qc, ar[k], br[k], cr[k])
        for k in range(1, n-1):
            if k < m:
                bb.carry(qc, cr[k-1], ar[k], br[k], cr[k])
            else:
                qc.ccx(cr[k-1], br[k], cr[k])

        k = n-1
        if k < m:
            if k == 0:
                # special case
                bb.hcarry(qc, ar[k], br[k], br[k+1])
                qc.cx(ar[k], br[k])
                bb.qhsum(qc, ar[k], br[k])
            else:
                bb.carry(qc, cr[k-1], ar[k], br[k], br[k+1])
                qc.cx(ar[k], br[k])
                bb.qsum(qc, cr[k-1], ar[k], br[k])
        else:
            qc.ccx(cr[k-1], br[k], br[k+1])
            qc.cx(cr[k-1], br[k])

        for k in range(n-2, 0, -1):
            if k < m:
                bb.icarry(qc, cr[k-1], ar[k], br[k], cr[k])
                bb.qsum(qc, cr[k-1], ar[k], br[k])
            else:
                qc.ccx(cr[k-1], br[k], cr[k])
                qc.cx(cr[k-1], br[k])
        k = 0
        if k < n - 1:
            bb.ihcarry(qc, ar[k], br[k], cr[k])
            bb.qhsum(qc, ar[k], br[k])


def unsigned_adderv_gate(m: int, n: int, label="uaddv", use_gates: bool = False) -> Gate:
    """ Create an unsigned adder gate.

        This version supports unmatched register sizes.

        Usage:
            qc.append(unsigned_adderv_gate(n), [a1,...,am, b1,...,bn+1, c1,...,cn])
        
        Effect:
            [a, b, c=0] -> [a, b+a, c=0]

        :param m: bit size of a
        :param n: bit size of b - 1
        :param label: label to put on the gate

    """
    ar = QuantumRegister(m, name="a")
    br = QuantumRegister(n+1, name="b")
    cr = QuantumRegister(n-1, "c")
    qc = QuantumCircuit(ar, br, cr)
    unsigned_adderv(qc, ar, br, cr, use_gates=use_gates)
    return qc.to_gate(label=f"{label}({m},{n})")


def controlled_unsigned_adderv(qc: QuantumCircuit, cbit: QubitSpecifier,
                               ar: QuantumRegister, br: QuantumRegister,
                               cr: QuantumRegister, use_gates = True):
    """ Emit an n bit adder circuit.

        This version supports unmatched register sizes.

        Effect:
            [ar, br, cr=0] -> [ar, br+ar, cr=0]
        
        :param qc: target circuit
        :param ar: left (m bits)
        :param br: right (n+1 bits (n >= m))
        :param cr: carry (n bits)
    """
    m = ut.bitsize(ar)
    n = ut.bitsize(br)-1
    if not (n >= m and ut.bitsize(cr) == n - 1):
        raise ValueError(
            f"size mismatch: ar[{m}], br[{n}], cr[{ut.bitsize(cr)}]")
    if use_gates:
        k = 0
        if k < n - 1:
            qc.append(bb.chcarry_gate(), [cbit, ar[k], br[k], cr[k]])
        for k in range(1, n-1):
            if k < m:
                qc.append(bb.ccarry_gate(), [cbit, cr[k-1], ar[k], br[k], cr[k]])
            else:
                qc.append(C3XGate(), [cbit, cr[k-1], br[k], cr[k]])

        k = n-1
        if k < m:
            if k == 0:
                # special case
                qc.append(bb.chcarry_gate(), [cbit, ar[k], br[k], br[k+1]])
                qc.ccx(cbit, ar[k], br[k])
                qc.append(bb.cqhsum_gate(), [cbit, ar[k], br[k]])
            else:
                qc.append(bb.ccarry_gate(), [cbit, cr[k-1], ar[k], br[k], br[k+1]])
                qc.ccx(cbit, ar[k], br[k])
                qc.append(bb.cqsum_gate(), [cbit, cr[k-1], ar[k], br[k]])
        else:
            qc.append(C3XGate(), [cbit, cr[k-1], br[k], br[k+1]])
            qc.ccx(cbit, cr[k-1], br[k])

        for k in range(n-2, 0, -1):
            if k < m:
                qc.append(bb.cicarry_gate(), [cbit, cr[k-1], ar[k], br[k], cr[k]])
                qc.append(bb.cqsum_gate(), [cbit, cr[k-1], ar[k], br[k]])
            else:
                qc.append(C3XGate(), [cbit, cr[k-1], br[k], cr[k]])
                qc.ccx(cbit, cr[k-1], br[k])
        k = 0
        if k < n - 1:
            qc.append(bb.cihcarry_gate(), [cbit, ar[k], br[k], cr[k]])
            qc.append(bb.cqhsum_gate(), [cbit, ar[k], br[k]])
    else:
        k =  0
        if k < n - 1:
            bb.chcarry(qc, cbit, ar[k], br[k], cr[k])
        for k in range(1, n-1):
            if k < m:
                bb.ccarry(qc, cbit, cr[k-1], ar[k], br[k], cr[k])
            else:
                qc.append(C3XGate(), [cbit, cr[k-1], br[k], cr[k]])

        k = n-1
        if k < m:
            if k == 0:
                # special case
                bb.chcarry(qc, cbit, ar[k], br[k], br[k+1])
                qc.ccx(cbit, ar[k], br[k])
                bb.cqhsum(qc, cbit, ar[k], br[k])
            else:
                bb.ccarry(qc, cbit, cr[k-1], ar[k], br[k], br[k+1])
                qc.ccx(cbit, ar[k], br[k])
                bb.cqsum(qc, cbit, cr[k-1], ar[k], br[k])
        else:
            qc.append(C3XGate(), [cbit, cr[k-1], br[k], br[k+1]])
            qc.ccx(cbit, cr[k-1], br[k])

        for k in range(n-2, 0, -1):
            if k < m:
                bb.cicarry(qc, cbit, cr[k-1], ar[k], br[k], cr[k])
                bb.cqsum(qc, cbit, cr[k-1], ar[k], br[k])
            else:
                qc.append(C3XGate(), [cbit, cr[k-1], br[k], cr[k]])
                qc.ccx(cbit, cr[k-1], br[k])
        k = 0
        if k < n -1:
            bb.cihcarry(qc, cbit, ar[k], br[k], cr[k])
            bb.cqhsum(qc, cbit, ar[k], br[k])



def controlled_unsigned_adderv_gate(m: int, n: int, label: str="uaddv", use_gates=False):
    """ Create a controlled version of unsigned_adderv_gate"""
    base_gate = unsigned_adderv_gate(m, n, label=label, use_gates=use_gates)
    controlled_gate = base_gate.control(1)
    return controlled_gate


def scoadder(qc: QuantumCircuit, y: int,
             br: QuantumRegister, cr: QuantumRegister,
             use_gates: bool = False):
    """ Emit a signed constant adder circuit.

        Effect:
            [y, br, cr=0] = [y, br+y, cr=0]
        
        :param qc: target circuit
        :param y: left (circuit build time constant)
        :param br: right (n bits)
        :param cr: carry (n - 1 bits)
    """
    n = ut.bitsize(br)
    nc = ut.bitsize(cr)
    if not nc == n - 1:
        raise ValueError(
            f"size mismatch: br[{n}], cr[{nc}]")
    if use_gates:
        ybit = y & 1
        qc.append(bb.cohcarry_gate(ybit), [br[0], cr[0]])
        for i in range(1, n-1):
            ybit = (y >> i) & 1
            qc.append(bb.cocarry_gate(ybit), [cr[i-1], br[i], cr[i]])
        ybit = (y >> (n-1)) & 1
        qc.append(bb.cosum_gate(ybit), [cr[n-2], br[n-1]])
        for i in range(n-2, 0, -1):
            ybit = (y >> i) & 1
            qc.append(bb.icocarry_gate(ybit), [cr[i-1], br[i], cr[i]])
            qc.append(bb.cosum_gate(ybit), [cr[i-1], br[i]])
        ybit = y & 1
        qc.append(bb.icohcarry_gate(ybit), [br[0], cr[0]])
        qc.append(bb.cohsum_gate(ybit), [br[0]])
    else:
        ybit = y & 1
        bb.cohcarry(qc, ybit, br[0], cr[0])
        for i in range(1, n-1):
            ybit = (y >> i) & 1
            bb.cocarry(qc, cr[i-1], ybit, br[i], cr[i])
        ybit = (y >> (n-1)) & 1
        bb.cosum(qc, cr[n-2], ybit, br[n-1])
        for i in range(n-2, 0, -1):
            ybit = (y >> i) & 1
            bb.icocarry(qc, cr[i-1], ybit, br[i], cr[i])
            bb.cosum(qc, cr[i-1], ybit, br[i])
        ybit = y & 1
        bb.icohcarry(qc, ybit, br[0], cr[0])
        bb.cohsum(qc, ybit, br[0])


def scoadder_gate(n: int, y: int, label="scoadd", use_gates: bool=False) -> Gate:
    """ Create a signed constant adder gate.

        Usage:
            qc.append(scoadder_gate(n, y), [b1,...,bn, c1,...,cn-1])
        
        Effect:
            [y, b, c=0] -> [y, b+y, c=0]

        :param n: bit size of b - 1
        :param y: constant value to add
        :param label: label to put on the gate

    """
    br = QuantumRegister(n, "b")
    cr = QuantumRegister(n-1, "cr")
    qc = QuantumCircuit(br, cr)
    scoadder(qc, y, br, cr, use_gates=use_gates)
    return qc.to_gate(label=f"{label}({n},{y})")

def signed_adder(qc: QuantumCircuit, ar: QuantumRegister, br: QuantumRegister,
                 cr: QuantumRegister, use_gates: bool=False):
    """ Emit an n bit signed adder circuit.

        Effect:
            [ar, br, cr=0] -> [ar, br+ar, c=0]
        
        :param qc: target circuit
        :param ar: left (n bits)
        :param br: right (n bits)
        :param cr: carry (n-1 bits)
    """
    n = ut.bitsize(ar)
    if not (ut.bitsize(br) == n and ut.bitsize(cr) == n-1):
        raise ValueError(
            f"size mismatch: ar[{n}], br[{ut.bitsize(br)}], cr[{ut.bitsize(cr)}]")
    if use_gates:
        k = 0
        qc.append(bb.hcarry_gate(), [ar[k], br[k], cr[k]])

        for k in range(1, n-1):
            qc.append(bb.carry_gate(), [cr[k-1], ar[k], br[k], cr[k]])

        k = n - 1
        qc.append(bb.qsum_gate(), [cr[k-1], ar[k], br[k]])

        for k in range(n-2, 0, -1):
            qc.append(bb.icarry_gate(), [cr[k-1], ar[k], br[k], cr[k]])
            qc.append(bb.qsum_gate(), [cr[k-1], ar[k], br[k]])

        k = 0
        qc.append(bb.ihcarry_gate(), [ar[k], br[k], cr[k]])
        qc.append(bb.qhsum_gate(), [ar[k], br[k]])
    else:
        k = 0
        bb.hcarry(qc, ar[k], br[k], cr[k])

        for k in range(1, n-1):
            bb.carry(qc, cr[k-1], ar[k], br[k], cr[k])

        k = n - 1
        bb.qsum(qc, cr[k-1], ar[k], br[k])

        for k in range(n-2, 0, -1):
            bb.icarry(qc, cr[k-1], ar[k], br[k], cr[k])
            bb.qsum(qc, cr[k-1], ar[k], br[k])
        
        k = 0
        bb.ihcarry(qc, ar[k], br[k], cr[k])
        bb.qhsum(qc, ar[k], br[k])


def signed_adder_gate(n, label="sadd", use_gates=False) -> Gate:
    """ Create a signed adder gate.

        Usage:
            qc.append(signed_adder_gate(n), [a1,...,an, b1,...,bn, c1,...,cn])

        Effect:
            [a, b, c=0] -> [a, b+a, c=0]
        
        :param n: bit size of a
        :param label: label to put on the gate
    """
    ar = QuantumRegister(n, name="a")
    br = QuantumRegister(n, name="b")
    cr = QuantumRegister(n-1, "c")
    qc = QuantumCircuit(ar, br, cr)
    signed_adder(qc, ar, br, cr, use_gates=use_gates)
    return qc.to_gate(label=f"{label}({n})")


def signed_adderv(qc: QuantumCircuit, ar: QuantumRegister,
                  br: QuantumRegister, cr: QuantumRegister,
                  use_gates: bool=False):
    """ Emit an n bit signed adder circuit.

        This version supports unmatched register sizes.

        Effect:
            [ar, br, cr=0] -> [ar, br+ar, cr=0]
        
        :param qc: target circuit
        :param ar: left (m bits)
        :param br: right (n bits (n >= m))
        :param cr: carry (n bits)
    """
    m = ut.bitsize(ar)
    n = ut.bitsize(br)
    if not (m <= n and ut.bitsize(cr) == n-1):
        raise ValueError(
            f"size mismatch: ar[{m}], br[{n}], cr[{ut.bitsize(cr)}]")
    if use_gates:
        k = 0
        qc.append(bb.hcarry_gate(), [ar[k], br[k], cr[k]])

        for k in range(1, n-1):
            if k < m:
                qc.append(bb.carry_gate(), [cr[k-1], ar[k], br[k], cr[k]])
            else:
                # repeat using the MSB of ar for the rest of the bits.
                qc.append(bb.carry_gate(), [cr[k-1], ar[m-1], br[k], cr[k]])

        k = n-1
        if k < m:
            qc.append(bb.qsum_gate(), [cr[k-1], ar[k], br[k]])
        else:
            qc.append(bb.qsum_gate(), [cr[k-1], ar[m-1], br[k]])

        for k in range(n-2, 0, -1):
            if k < m:
                qc.append(bb.icarry_gate(), [cr[k-1], ar[k], br[k], cr[k]])
                qc.append(bb.qsum_gate(), [cr[k-1], ar[k], br[k]])
            else:
                qc.append(bb.icarry_gate(), [cr[k-1], ar[m-1], br[k], cr[k]])
                qc.append(bb.qsum_gate(), [cr[k-1], ar[m-1], br[k]])

        k = 0
        qc.append(bb.ihcarry_gate(), [ar[k], br[k], cr[k]])
        qc.append(bb.qhsum_gate(), [ar[k], br[k]])
    else:
        k = 0
        bb.hcarry(qc, ar[k], br[k], cr[k])

        for k in range(1, n-1):
            if k < m:
                bb.carry(qc, cr[k-1], ar[k], br[k], cr[k])
            else:
                # repeat using the MSB of ar for the rest of the bits.
                bb.carry(qc, cr[k-1], ar[m-1], br[k], cr[k])

        k = n-1
        if k < m:
            bb.qsum(qc, cr[k-1], ar[k], br[k])
        else:
            bb.qsum(qc, cr[k-1], ar[m-1], br[k])

        for k in range(n-2, 0, -1):
            if k < m:
                bb.icarry(qc, cr[k-1], ar[k], br[k], cr[k])
                bb.qsum(qc, cr[k-1], ar[k], br[k])
            else:
                bb.icarry(qc, cr[k-1], ar[m-1], br[k], cr[k])
                bb.qsum(qc, cr[k-1], ar[m-1], br[k])

        k = 0
        bb.ihcarry(qc, ar[k], br[k], cr[k])
        bb.qhsum(qc, ar[k], br[k])


def signed_adderv_gate(m: int, n: int, label="saddv", use_gates=False) -> Gate:
    """ Create a signed adder gate.

        This version supports unmatched register sizes.

        Usage:
            qc.append(signed_adderv_gate(n), [a1,...,am, b1,...,bn, c1,...,cn])
        
        Effect:
            [a, b, c=0] -> [a, b+a, c=0]

        :param m: bit size of a
        :param n: bit size of b
        :param label: label to put on the gate

    """
    ar = QuantumRegister(m, "a")
    br = QuantumRegister(n, "b")
    cr = QuantumRegister(n-1, "c")
    qc = QuantumCircuit(ar, br, cr)
    signed_adderv(qc, ar, br, cr, use_gates=use_gates)
    return qc.to_gate(label=f"{label}({m},{n})")


def controlled_signed_adder(qc: QuantumCircuit, cbit: QubitSpecifier,
                            ar: QuantumRegister, br: QuantumRegister,
                            cr: QuantumRegister, use_gates: bool=False):
    """ Emit an n bit controlled signed adder circuit.

        Effect:
            [ar, br, cr=0, cbit] = [ar + br+ar, cr=0] if cbit
    """
    n = ut.bitsize(ar)
    if not (ut.bitsize(br) == n and ut.bitsize(cr) == n - 1):
        raise ValueError(
            f"size mismatch: ar[{n}], br[{ut.bitsize(br)}], cr[{ut.bitsize(cr)}]")
    if use_gates:
        k = 0
        qc.append(bb.chcarry_gate(), [cbit, ar[k], br[k], cr[k]])
        for k in range(1, n-1):
            qc.append(bb.ccarry_gate(), [cbit, cr[k-1], ar[k], br[k], cr[k]])

        k = n - 1
        qc.append(bb.cqsum_gate(), [cbit, cr[k-1], ar[k], br[k]])

        for k in range(n-2, 0, -1):
            qc.append(bb.cicarry_gate(), [cbit, cr[k-1], ar[k], br[k], cr[k]])
            qc.append(bb.cqsum_gate(), [cbit, cr[k-1], ar[k], br[k]])

        k = 0
        qc.append(bb.cihcarry_gate(), [cbit, ar[k], br[k], cr[k]])
        qc.append(bb.cqhsum_gate(), [cbit, ar[k], br[k]])
    else:
        k = 0
        bb.chcarry(qc, cbit, ar[k], br[k], cr[k])

        for k in range(1, n-1):
            bb.ccarry(qc, cbit, cr[k-1], ar[k], br[k], cr[k])

        k = n - 1
        bb.cqsum(qc, cbit, cr[k-1], ar[k], br[k])

        for k in range(n-2, 0, -1):
            bb.cicarry(qc, cbit, cr[k-1], ar[k], br[k], cr[k])
            bb.cqsum(qc, cbit, cr[k-1], ar[k], br[k])

        k = 0
        bb.cihcarry(qc, cbit, ar[k], br[k], cr[k])
        bb.cqhsum(qc, cbit, ar[k], br[k])


def controlled_signed_adder_gate(n: int, use_gates: bool=False) -> Gate:
    """ Create a signed adder gate.

        Usage:
            qc.append(controlled_signed_adder_gate(n), [ctl, a1,...,an, b1,...,bn, c1,...,cn])

        Effect:
            [a, b, c=0] -> [a, b+a, c=0] when ctl == 1
        
        :param n: bit size of a
    """
    base_gate = signed_adder_gate(n, use_gates=use_gates)
    controlled_gate = base_gate.control(1)
    return controlled_gate


def controlled_signed_adderv(qc: QuantumCircuit, cbit: QubitSpecifier,
                             ar: QuantumRegister, br: QuantumRegister,
                             cr: QuantumRegister, use_gates: bool = False):
    """ Emit an n bit unmatched length signed adder circuit

        This version supports unmatched register sizes.

        Effect:
            [ar, br, cr=0] -> [ar, br+ar, cr=0]
    """
    m = ut.bitsize(ar)
    n = ut.bitsize(br)
    if not (m <= n and ut.bitsize(cr) == n - 1):
        raise ValueError(
            f"size mismatch: ar[{m}], br[{n}], cr[{ut.bitsize(cr)}]")
    if use_gates:
        k = 0
        qc.append(bb.chcarry_gate(), [cbit, ar[k], br[k], cr[k]])

        for k in range(1, n-1):
            if k < m:
                qc.append(bb.ccarry_gate(), [cbit, cr[k-1], ar[k], br[k], cr[k]])
            else:
                qc.append(bb.ccarry_gate(), [cbit, cr[k-1], ar[m-1], br[k], cr[k]])

        k = n-1
        if k < m:
            qc.append(bb.cqsum_gate(), [cbit, cr[k-1], ar[k], br[k]])
        else:
            qc.append(bb.cqsum_gate(), [cbit, cr[k-1], ar[m-1], br[k]])

        for k in range(n-2, 0, -1):
            if k < m:
                qc.append(bb.cicarry_gate(), [cbit, cr[k-1], ar[k], br[k], cr[k]])
                qc.append(bb.cqsum_gate(), [cbit, cr[k-1], ar[k], br[k]])
            else:
                qc.append(bb.cicarry_gate(), [cbit, cr[k-1], ar[m-1], br[k], cr[k]])
                qc.append(bb.cqsum_gate(), [cbit, cr[k-1], ar[m-1], br[k]])

        k = 0
        qc.append(bb.cihcarry_gate(), [cbit, ar[k], br[k], cr[k]])
        qc.append(bb.cqhsum_gate(), [cbit, ar[k], br[k]])
    else:
        k = 0
        bb.chcarry(qc, cbit, ar[k], br[k], cr[k])

        for k in range(1, n-1):
            if k < m:
                bb.ccarry(qc, cbit, cr[k-1], ar[k], br[k], cr[k])
            else:
                bb.ccarry(qc, cbit, cr[k-1], ar[m-1], br[k], cr[k])

        k = n-1
        if k < m:
            bb.cqsum(qc, cbit, cr[k-1], ar[k], br[k])
        else:
            bb.cqsum(qc, cbit, cr[k-1], ar[m-1], br[k])

        for k in range(n-2, 0, -1):
            if k < m:
                bb.cicarry(qc, cbit, cr[k-1], ar[k], br[k], cr[k])
                bb.cqsum(qc, cbit, cr[k-1], ar[k], br[k])
            else:
                bb.cicarry(qc, cbit, cr[k-1], ar[m-1], br[k], cr[k])
                bb.cqsum(qc, cbit, cr[k-1], ar[m-1], br[k])
        k = 0
        bb.cihcarry(qc, cbit, ar[k], br[k], cr[k])
        bb.cqhsum(qc, cbit, ar[k], br[k])

def controlled_signed_adderv_gate(m: int, n: int, use_gates=False) -> Gate:
    """ Create a controlled version of signed_adderv_gate"""
    base_gate = signed_adderv_gate(m, n, use_gates=use_gates)
    controlled_gate = base_gate.control(1)
    return controlled_gate
