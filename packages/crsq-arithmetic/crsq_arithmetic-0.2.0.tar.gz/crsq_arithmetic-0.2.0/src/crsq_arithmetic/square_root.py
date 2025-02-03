""" Square Root gates
"""
from qiskit.circuit import QuantumCircuit, QuantumRegister, Gate
from crsq_arithmetic.adder import controlled_unsigned_adderv, controlled_unsigned_adderv_gate
from crsq_arithmetic.subtractor import unsigned_subtractorv, unsigned_subtractorv_gate
import crsq_arithmetic.utils as ut

def square_root(qc: QuantumCircuit,
                zr: QuantumRegister,
                rr: QuantumRegister,
                wr: QuantumRegister,
                cr: QuantumRegister,
                use_gates: bool = False):
    """ Emit a square root circuit.

        Effect:
            [zr, rr=0, wr=0, cr=0] -> [zr-rr*rr, int(sqrt(zr)), rr*2, cr=0]
        
        :param qc: target circuit
        :param zr: operand (2*m bits)
        :param rr: root (m bits)
        :param wr: work (m+1 bits)
        :param cr: carry (2*m-1 bits)
    """
    nz = ut.bitsize(zr)
    nr = ut.bitsize(rr)
    nw = ut.bitsize(wr)
    ncr = ut.bitsize(cr)
    if not (nz == 2*nr and nw == nr+1 and ncr == nz-1):
        raise ValueError(f"size mismatch: zr[{nz}]," +
                         f" rr[{nr}], wr[{nw}], cr[{ncr}]")
    if use_gates:
        for k in range(nw-1):
            qc.x(wr[k])  # set wr[k] to 1
        for j in range(nr):
            # bits used in w
            if j == 0:
                wb = j + 1
            else:
                wb = j + 2
            # bits used in z
            zb = (j+1)*2
            par = ut.register_range(wr, nw-2-j, wb)
            pbr = ut.register_range(zr, nz-zb, zb) + [rr[nr-1-j]]
            pcr = ut.register_range(cr, ncr-zb, zb-1)
            qc.append(unsigned_subtractorv_gate(wb, zb),
                      par + pbr + pcr)
            ctrl = [rr[nr-1-j]]
            par = ut.register_range(wr, nw-2-j, wb)
            pbr = ut.register_range(zr, nz-zb, zb)
            pcr = ut.register_range(cr, ncr-zb+1, zb-2)
            qc.append(controlled_unsigned_adderv_gate(wb, zb-1),
                      ctrl + par + pbr + pcr)
            qc.x(wr[nw-2-j])
            # negative controlled not
            qc.x(rr[nr-1-j])
            qc.cx(rr[nr-1-j], wr[nw-1-j])
            # qc.x(rr[nr-1-j])
            # end of negative controlled not
            # qc.x(rr[nr-1-j])
    else:
        for k in range(nw-1):
            qc.x(wr[k])  # set wr[k] to 1
        for j in range(nr):
            if j == 0:
                wb = j + 1
            else:
                wb = j + 2
            zb = (j+1)*2
            par = ut.register_range(wr, nw-2-j, wb)
            pbr = ut.register_range(zr, nz-zb, zb) + [rr[nr-1-j]]
            pcr = ut.register_range(cr, ncr-zb, zb-1)
            unsigned_subtractorv(qc, par, pbr, pcr)
            ctrl = rr[nr-1-j]
            par = ut.register_range(wr, nw-2-j, wb)
            pbr = ut.register_range(zr, nz-zb, zb)
            pcr = ut.register_range(cr, ncr-zb+1, zb-2)
            controlled_unsigned_adderv(qc, ctrl, par, pbr, pcr)
            qc.x(wr[nw-2-j])
            # negative controlled not
            qc.x(rr[nr-1-j])
            qc.cx(rr[nr-1-j], wr[nw-1-j])
            # qc.x(rr[nr-1-j])
            # end of negative controlled not
            # qc.x(rr[nr-1-j])



def square_root_gate(n: int, label: str="sqrt", use_gates: bool = False) -> Gate:
    """ Emit a square root gate.

        Usage:
            qc.append(square_root_gate(n), [z1...z2n, r1...rn, w1...wn+1, c1...c2n])
        
        Effect:
            [z, r=0, w=0, c=0] -> [z-r*r, int(sqrt(z)), r*2, c=0]

        :param n: half of the bit size of z
        :param label: label to put on the gate
        :param use_gates: use custom gates for sum and carry gates
    """
    zr = QuantumRegister(2*n, name="z")
    rr = QuantumRegister(n, name="r")
    wr = QuantumRegister(n+1, name="w")
    cr = QuantumRegister(2*n-1, "c")
    qc = QuantumCircuit(zr, rr, wr, cr)
    square_root(qc, zr, rr, wr, cr, use_gates=use_gates)
    return qc.to_gate(label=f"{label}({n})")
