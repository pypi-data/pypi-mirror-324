""" Subtractor gates 
"""
from qiskit.circuit import QuantumCircuit, QuantumRegister, Gate

import crsq_arithmetic.bit_ops as bb
import crsq_arithmetic.utils as ut


def unsigned_subtractor(qc: QuantumCircuit, ar: QuantumRegister,
                        br: QuantumRegister, cr: QuantumRegister,
                        use_gates: bool = False):
    """ Emit an unsigned subtractor.
        It is actually a revsersed n bit adder circuit.

        Note:
          This is the reverse operation of br = ar + br.
          The order of ar and br is not intuitive.

        Effect:
          [ar, br+ar, cr=0] -> [ar, br, cr=0]
        
        :param qc: target circuit
        :param ar: left (n bits)
        :param br: right (n+1 bits)
        :param cr: carry (n bits)
    """
    n = ut.bitsize(ar)
    m = ut.bitsize(br)
    nc = ut.bitsize(cr)
    if not (m == n+1 and nc == n - 1):
        raise ValueError(
            f"size mismatch: ar[{n}], br[{ut.bitsize(br)}], cr[{ut.bitsize(cr)}]")
    if use_gates:
        k = 0
        qc.append(bb.iqhsum_gate(), [ar[k], br[k]])
        qc.append(bb.hcarry_gate(), [ar[k], br[k], cr[k]])

        for k in range(1, n-1):
            qc.append(bb.iqsum_gate(), [cr[k-1], ar[k], br[k]])
            qc.append(bb.carry_gate(), [cr[k-1], ar[k], br[k], cr[k]])
        k = n-1
        qc.append(bb.iqsum_gate(), [cr[k-1], ar[k], br[k]])
        qc.cx(ar[k], br[k])
        qc.append(bb.icarry_gate(), [cr[k-1], ar[k], br[k], br[k+1]])
        for k in range(n-2, 0, -1):
            qc.append(bb.icarry_gate(), [cr[k-1], ar[k], br[k], cr[k]])
        k = 0
        qc.append(bb.ihcarry_gate(), [ar[k], br[k], cr[k]])
    else:
        k = 0
        bb.iqhsum(qc, ar[k], br[k])
        bb.hcarry(qc, ar[k], br[k], cr[k])
        for k in range(1, n-1):
            bb.iqsum(qc, cr[k-1], ar[k], br[k])
            bb.carry(qc, cr[k-1], ar[k], br[k], cr[k])
        k = n-1
        bb.iqsum(qc, cr[k-1], ar[k], br[k])
        qc.cx(ar[k], br[k])
        bb.icarry(qc, cr[k-1], ar[k], br[k], br[k+1])

        for k in range(n-2, 0, -1):
            bb.icarry(qc, cr[k-1], ar[k], br[k], cr[k])
        k = 0
        bb.ihcarry(qc, ar[k], br[k], cr[k])


def unsigned_subtractor_gate(n: int, label: str="usub", use_gates: bool=False) -> Gate:
    """ Create an unsigned subtractor gate.
     
        Usage:
          qc.append(unsigned_subtractor_gate(n), [a1,...,an, b1,...,bn+1, c1,...,cn])

        Effect:
          [a, b+a, c=0] -> [a, b, c=0]
        
        :param n: bit size of a
        :param label: label to put on gate
    """
    ar = QuantumRegister(n, name="a")
    br = QuantumRegister(n+1, name="b")
    cr = QuantumRegister(n-1, "c")
    qc = QuantumCircuit(ar, br, cr)
    unsigned_subtractor(qc, ar, br, cr, use_gates=use_gates)
    return qc.to_gate(label=f"{label}({n})")


def unsigned_cosubtractor(qc: QuantumCircuit, y: int,
                          br: QuantumRegister, cr: QuantumRegister,
                          use_gates: bool = False):
    """ Emit an unsigned subtractor.
        It is actually a revsersed n bit adder circuit.

        Note:
          This is the reverse operation of br = ar + br.
          The order of ar and br is not intuitive.

        Effect:
          [ar, br+ar, cr=0] -> [ar, br, cr=0]
        
        :param qc: target circuit
        :param ar: left (n bits)
        :param br: right (n+1 bits)
        :param cr: carry (n bits)
    """
    m = ut.bitsize(br)
    n = m + 1
    nc = ut.bitsize(cr)
    if not (nc == n - 1):
        raise ValueError(
            f"size mismatch: br[{ut.bitsize(br)}], cr[{ut.bitsize(cr)}]")
    if use_gates:
        k = 0
        ybit = y & 1
        qc.append(bb.icohsum_gate(ybit), [br[k]])
        qc.append(bb.cohcarry_gate(ybit), [br[k], cr[k]])

        for k in range(1, n-1):
            ybit = (y >> k) & 1
            qc.append(bb.icosum_gate(ybit), [cr[k-1], br[k]])
            qc.append(bb.cocarry_gate(ybit), [cr[k-1], br[k], cr[k]])
        k = n-1
        ybit = (y >> k) & 1
        qc.append(bb.icosum_gate(ybit), [cr[k-1], br[k]])
        if ybit:
            qc.x(br[k])
        qc.append(bb.icocarry_gate(ybit), [cr[k-1], br[k], br[k+1]])
        for k in range(n-2, 0, -1):
            qc.append(bb.icocarry_gate(ybit), [cr[k-1], br[k], cr[k]])
        k = 0
        qc.append(bb.icohcarry_gate(ybit), [br[k], cr[k]])
    else:
        k = 0
        ybit = y & 1
        bb.icohsum(qc, ybit, br[k])
        bb.cohcarry(qc, ybit, br[k], cr[k])
        for k in range(1, n-1):
            ybit = (y >> k) & 1
            bb.icosum(qc, cr[k-1], ybit, br[k])
            bb.cocarry(qc, cr[k-1], ybit, br[k], cr[k])
        k = n-1
        ybit = (y >> k) & 1
        bb.icosum(qc, cr[k-1], ybit, br[k])
        if ybit:
            qc.x(br[k])
        bb.icocarry(qc, cr[k-1], ybit, br[k], br[k+1])

        for k in range(n-2, 0, -1):
            ybit = (y >> k) & 1
            bb.icocarry(qc, cr[k-1], ybit, br[k], cr[k])
        k = 0
        ybit = y & 1
        bb.icohcarry(qc, ybit, br[k], cr[k])

def unsigned_subtractorv(qc: QuantumCircuit, ar: QuantumRegister,
                         br: QuantumRegister, cr: QuantumRegister, use_gates: bool=False):
    """ Emit a revsersed n bit adder circuit.

        This version supports unmatched register sizes.

        Effect:
          [ar, br, cr=0] -> [ar, br-ar, 0]
        
        :param qc: target circuit
        :param ar: left (m bits)
        :param br: right (n+1 bits (n > m))
        :param cr: carry (n bits)
    """
    m = ut.bitsize(ar)
    n = ut.bitsize(br)-1
    if not (n >= m and ut.bitsize(cr) == n-1):
        raise ValueError(
            f"size mismatch: ar[{n}], br[{ut.bitsize(br)}], cr[{ut.bitsize(cr)}]")
    if use_gates:
        k = 0
        qc.append(bb.iqhsum_gate(), [ar[k], br[k]])
        qc.append(bb.hcarry_gate(), [ar[k], br[k], cr[k]])
        for k in range(1, n-1):
            if k < m:
                qc.append(bb.iqsum_gate(), [cr[k-1], ar[k], br[k]])
                qc.append(bb.carry_gate(), [cr[k-1], ar[k], br[k], cr[k]])
            else:
                qc.cx(cr[k-1], br[k])
                qc.ccx(cr[k-1], br[k], cr[k])

        k = n-1
        if k < m:
            qc.append(bb.iqsum_gate(), [cr[k-1], ar[k], br[k]])
            qc.cx(ar[k], br[k])
            qc.append(bb.icarry_gate(), [cr[k-1], ar[k], br[k], br[k+1]])
        else:
            qc.cx(cr[k-1], br[k])
            qc.ccx(cr[k-1], br[k], br[k+1])

        for k in range(n-2, 0, -1):
            if k < m:
                qc.append(bb.icarry_gate(), [cr[k-1], ar[k], br[k], cr[k]])
            else:
                qc.ccx(cr[k-1], br[k], cr[k])
        k = 0
        qc.append(bb.ihcarry_gate(), [ar[k], br[k], cr[k]])
    else:
        k = 0
        bb.iqhsum(qc, ar[k], br[k])
        bb.hcarry(qc, ar[k], br[k], cr[k])
        for k in range(1, n-1):
            if k < m:
                bb.iqsum(qc, cr[k-1], ar[k], br[k])
                bb.carry(qc, cr[k-1], ar[k], br[k], cr[k])
            else:
                qc.cx(cr[k-1], br[k])
                qc.ccx(cr[k-1], br[k], cr[k])

        k = n-1
        if k < m:
            bb.iqsum(qc, cr[k-1], ar[k], br[k])
            qc.cx(ar[k], br[k])
            bb.icarry(qc, cr[k-1], ar[k], br[k], br[k+1])
        else:
            qc.cx(cr[k-1], br[k])
            qc.ccx(cr[k-1], br[k], br[k+1])

        for k in range(n-2, 0, -1):
            if k < m:
                bb.icarry(qc, cr[k-1], ar[k], br[k], cr[k])
            else:
                qc.ccx(cr[k-1], br[k], cr[k])
        k = 0
        bb.ihcarry(qc, ar[k], br[k], cr[k])


def unsigned_subtractorv_gate(m, n, label="usubv", use_gates: bool=False):
    """ Create an unsigned subtractor gate for mismatched length input.

        Usage:
            qc.append(unsigned_subtractorv_gate(m, n), [a1,...,an, b1,...,bn, c1,...,cn])
        
        Effect:
            [a, a+b, c=0] -> [a, b, c=0]
    """
    ar = QuantumRegister(m, name="a")
    br = QuantumRegister(n+1, name="b")
    cr = QuantumRegister(n-1, "c")
    qc = QuantumCircuit(ar, br, cr)
    unsigned_subtractorv(qc, ar, br, cr, use_gates=use_gates)
    return qc.to_gate(label=f"{label}({m},{n})")


def signed_cosubtractor(qc: QuantumCircuit, y: int,
                        br: QuantumRegister, cr: QuantumRegister,
                        use_gates: bool = False):
    """ Emit a signed constant subtractor circuit.

        Effect:
            [y, br, cr=0] = [y, br-y, cr=0]
        
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
        qc.append(bb.icohsum_gate(ybit), [br[0]])
        qc.append(bb.cohcarry_gate(ybit), [br[0], cr[0]])
        for k in range(1, n-1):
            ybit = (y >> k) & 1
            qc.append(bb.icosum_gate(ybit), [cr[k-1], br[k]])
            qc.append(bb.cocarry_gate(ybit), [cr[k-1], br[k], cr[k]])
        ybit = (y >> (n-1)) & 1
        qc.append(bb.icosum_gate(ybit), [cr[n-2], br[n-1]])
        for k in range(n-2, 0, -1):
            ybit = (y >> k) & 1
            qc.append(bb.icocarry_gate(ybit), [cr[k-1], br[k], cr[k]])
        ybit = y & 1
        qc.append(bb.icohcarry_gate(ybit), [br[0], cr[0]])
    else:
        ybit = y & 1
        bb.icohsum(qc, ybit, br[0])
        bb.cohcarry(qc, ybit, br[0], cr[0])
        for k in range(1, n-1):
            ybit = (y >> k) & 1
            bb.icosum(qc, cr[k-1], ybit, br[k])
            bb.cocarry(qc, cr[k-1], ybit, br[k], cr[k])
        ybit = (y >> (n-1)) & 1
        bb.icosum(qc, cr[n-2], ybit, br[n-1])
        for k in range(n-2, 0, -1):
            ybit = (y >> k) & 1
            bb.icocarry(qc, cr[k-1], ybit, br[k], cr[k])
        ybit = y & 1
        bb.icohcarry(qc, ybit, br[0], cr[0])

def signed_cosubtractor_gate(n: int, y: int, label: str="scosub", use_gates: bool = False) -> Gate:
    """ Create a signed subtractor gate.

        Usage:    
            qc.append(signed_cosubtractor_gate(n, y), [b1,...,bn+1, c1,...,cn])

        Effect:
            [y, b, c=0] -> [y, b-y, c=0]

        :param n: bit size of b - 1
        :param y: constant value to add
        :param label: label to put on the gate
    """
    br = QuantumRegister(n, name="b")
    cr = QuantumRegister(n-1, "c")
    qc = QuantumCircuit(br, cr)
    signed_cosubtractor(qc, y, br, cr, use_gates=use_gates)
    return qc.to_gate(label=f"{label}({n},{y})")

def signed_subtractor(qc: QuantumCircuit, ar: QuantumRegister,
                      br: QuantumRegister, cr: QuantumRegister,
                      use_gates: bool=False):
    """ Emit an n bit in-place subtractor circuit.

        Effect:
            [ar, ar+br, cr=0] -> [ar, br, cr=0]
        
        :param qc: target circuit
        :param ar: left (n bits)
        :param br: right (n bits)
        :param cr: carry (n bits)
    """
    n = ut.bitsize(ar)
    if not (ut.bitsize(br) == n and ut.bitsize(cr) == n - 1):
        raise ValueError(
            f"size mismatch: ar[{n}], br[{ut.bitsize(br)}], cr[{ut.bitsize(cr)}]")
    if use_gates:
        k = 0
        qc.append(bb.iqhsum_gate(), [ar[k], br[k]])
        qc.append(bb.hcarry_gate(), [ar[k], br[k], cr[k]])
        for k in range(1, n-1):
            qc.append(bb.iqsum_gate(), [cr[k-1], ar[k], br[k]])
            qc.append(bb.carry_gate(), [cr[k-1], ar[k], br[k], cr[k]])

        k = n-1
        qc.append(bb.iqsum_gate(), [cr[k-1], ar[k], br[k]])

        for k in range(n-2, 0, -1):
            qc.append(bb.icarry_gate(), [cr[k-1], ar[k], br[k], cr[k]])
        k = 0
        qc.append(bb.ihcarry_gate(), [ar[k], br[k], cr[k]])
    else:
        k = 0
        bb.iqhsum(qc, ar[k], br[k])
        bb.hcarry(qc, ar[k], br[k], cr[k])

        for k in range(1, n-1):
            bb.iqsum(qc, cr[k-1], ar[k], br[k])
            bb.carry(qc, cr[k-1], ar[k], br[k], cr[k])

        k = n-1
        bb.iqsum(qc, cr[k-1], ar[k], br[k])

        for k in range(n-2, 0, -1):
            bb.icarry(qc, cr[k-1], ar[k], br[k], cr[k])
        k = 0
        bb.ihcarry(qc, ar[k], br[k], cr[k])


def signed_o_subtractor(qc: QuantumCircuit, ar: QuantumRegister,
                        br: QuantumRegister, dr: QuantumRegister,
                        carry: QuantumRegister, use_gates: bool=False):
    """ Emit an n bit out-of-place subtractor circuit.
        Effect:
            [ar, br, dr=0, carry=0] => [ar, br, dr=br-ar, carry=0]
        :param qc: target circuit
        :param ar: left (n bits)
        :param br: right (n bits)
        :param dr: result (n bits)
        :param carry: carry (n bits)
    """
    n = ut.bitsize(ar)
    if not (ut.bitsize(br) == n and ut.bitsize(dr) == n and ut.bitsize(carry) == n-1):
        raise ValueError(
            f"size mismatch: ar[{n}], br[{ut.bitsize(br)}], " +
            f"dr[{ut.bitsize(dr)}], carry[{ut.bitsize(carry)}]"
        )
    # copy br to dr
    for k in range(n):
        qc.cx(br[k], dr[k])
    signed_subtractor(qc, ar, dr, carry, use_gates)


def signed_subtractor_gate(n: int, label: str="ssub", use_gates: bool = False) -> Gate:
    """ Create a signed subtractor gate.

        Usage:    
            qc.append(signed_subtractor_gate(n), [a1,...,an, b1,...,bn, c1,...,cn])

        Effect:
            [a, b+a, c=0] -> [a, b, c=0]

        :param n: bit size of a
        :param label: label to put on the gate
    """
    ar = QuantumRegister(n, name="a")
    br = QuantumRegister(n, name="b")
    cr = QuantumRegister(n-1, "c")
    qc = QuantumCircuit(ar, br, cr)
    signed_subtractor(qc, ar, br, cr, use_gates=use_gates)
    return qc.to_gate(label=f"{label}({n})")


def signed_o_subtractor_gate(n: int, label: str="ossub") -> Gate:
    """ Create a signed subtractor gate.

        Usage:    
            qc.append(signed_o_subtractor_gate(n), [a1,...,an, b1,...,bn, d1,...,dn, c1,...,cn])

        Effect:
            [a, b, d, c=0] -> [a, b, d=b-a, c=0]

        :param n: bit size of a
        :param label: label to put on the gate
    """
    ar = QuantumRegister(n, name="a")
    br = QuantumRegister(n, name="b")
    dr = QuantumRegister(n, name="d")
    cr = QuantumRegister(n-1, "carry")
    qc = QuantumCircuit(ar, br, dr, cr)
    signed_o_subtractor(qc, ar, br, dr, cr)
    return qc.to_gate(label=f"{label}({n})")


def signed_subtractorv(qc: QuantumCircuit, ar: QuantumRegister,
                      br: QuantumRegister, cr: QuantumRegister,
                      use_gates: bool=False):
    """ Emit an n bit in-place subtractor circuit.

        Effect:
            [ar, ar+br, cr=0] -> [ar, br, cr=0]
        
        :param qc: target circuit
        :param ar: left (m bits)
        :param br: right (n bits (n >= m))
        :param cr: carry (n bits)
    """
    m = ut.bitsize(ar)
    n = ut.bitsize(br)
    if not (m <= n and ut.bitsize(cr) == n - 1):
        raise ValueError(
            f"size mismatch: ar[{m}], br[{n}], cr[{ut.bitsize(cr)}]")
    if use_gates:
        k = 0
        qc.append(bb.iqhsum_gate(), [ar[k], br[k]])
        qc.append(bb.hcarry_gate(), [ar[k], br[k], cr[k]])
        for k in range(1, n-1):
            if k < m:
                qc.append(bb.iqsum_gate(), [cr[k-1], ar[k], br[k]])
                qc.append(bb.carry_gate(), [cr[k-1], ar[k], br[k], cr[k]])
            else:
                qc.append(bb.iqsum_gate(), [cr[k-1], ar[m-1], br[k]])
                qc.append(bb.carry_gate(), [cr[k-1], ar[m-1], br[k], cr[k]])

        k = n-1
        if k < m:
            qc.append(bb.iqsum_gate(), [cr[k-1], ar[k], br[k]])
        else:
            qc.append(bb.iqsum_gate(), [cr[k-1], ar[m-1], br[k]])

        for k in range(n-2, 0, -1):
            if k < m:
                qc.append(bb.icarry_gate(), [cr[k-1], ar[k], br[k], cr[k]])
            else:
                qc.append(bb.icarry_gate(), [cr[k-1], ar[m-1], br[k], cr[k]])
        k = 0
        qc.append(bb.ihcarry_gate(), [ar[k], br[k], cr[k]])
    else:
        k = 0
        bb.iqhsum(qc, ar[k], br[k])
        bb.hcarry(qc, ar[k], br[k], cr[k])

        for k in range(1, n-1):
            if k < m:
                bb.iqsum(qc, cr[k-1], ar[k], br[k])
                bb.carry(qc, cr[k-1], ar[k], br[k], cr[k])
            else:
                bb.iqsum(qc, cr[k-1], ar[m-1], br[k])
                bb.carry(qc, cr[k-1], ar[m-1], br[k], cr[k])

        k = n-1
        if k < m:
            bb.iqsum(qc, cr[k-1], ar[k], br[k])
        else:
            bb.iqsum(qc, cr[k-1], ar[m-1], br[k])

        for k in range(n-2, 0, -1):
            if k < m:
                bb.icarry(qc, cr[k-1], ar[k], br[k], cr[k])
            else:
                bb.icarry(qc, cr[k-1], ar[m-1], br[k], cr[k])
        k = 0
        bb.ihcarry(qc, ar[k], br[k], cr[k])


def signed_subtractorv_gate(m: int, n: int, label: str="ssubv", use_gates: bool = False) -> Gate:
    """ Create a signed subtractor gate.

        Usage:    
            qc.append(signed_subtractor_gate(n), [a1,...,am, b1,...,bn, c1,...,cn])

        Effect:
            [a, b+a, c=0] -> [a, b, c=0]

        :param m: bit size of a
        :param n: bit size of b
        :param label: label to put on the gate
    """
    ar = QuantumRegister(m, name="a")
    br = QuantumRegister(n, name="b")
    cr = QuantumRegister(n-1, "c")
    qc = QuantumCircuit(ar, br, cr)
    signed_subtractorv(qc, ar, br, cr, use_gates=use_gates)
    return qc.to_gate(label=f"{label}({m},{n})")
