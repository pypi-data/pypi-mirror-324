""" Divider gates
"""
from qiskit.circuit import QuantumCircuit, QuantumRegister, Gate
from crsq_arithmetic.adder import controlled_signed_adder, controlled_signed_adder_gate
from crsq_arithmetic.subtractor import unsigned_subtractor, unsigned_subtractor_gate
import crsq_arithmetic.utils as ut


def unsigned_divider(qc: QuantumCircuit,
                     zr: QuantumRegister,
                     zzr: QuantumRegister,
                     dr: QuantumRegister,
                     cr: QuantumRegister,
                     use_gates: bool = False):
    """ Emit an unsigned divider circuit.

        Compute rr such that zr = qq * dr + rr.

        Effect:
          [zr, zzr=0, dr, cr=0] -> [ rr[:]+qq[n:], qq[:n], dr, cr=0]
        
        zzr will hold higher n bits or qq.
        lower m-n bits of qq will be held in the higher bits of zr.

        :param qc: target circuit
        :param zr: [in]left (m bits) / [out] lower mbits of qqrr
        :param zzr: [in] extra result (n bits) = 0 / [out] higher nbits of qqrr
        :param dr: right (n bits)
        :param cr: carry (n-1 bits)
    """
    m = ut.bitsize(zr)
    n = ut.bitsize(dr)
    nzzr = ut.bitsize(zzr)
    ncr = ut.bitsize(cr)
    if not (nzzr == n and ncr == n-1):
        raise ValueError(f"size mismatch: zr[{m}], dr[{n}]," +
                         f" zzr[{nzzr}] cr1[{ncr}]")
    if use_gates:
        exz = list(zr) + list(zzr)
        for j in range(m-1, -1, -1):
            qc.append(unsigned_subtractor_gate(n),
                      dr[:] + ut.register_range(exz, j, n+1)[:] + cr[:])
            qc.append(controlled_signed_adder_gate(n),
                      [exz[j+n]] + dr[:] + ut.register_range(exz, j, n)[:] + cr[:])
            qc.x(exz[j+n])
    else:
        exz = list(zr) + list(zzr)
        for j in range(m-1, -1, -1):
            unsigned_subtractor(qc, dr, ut.register_range(exz, j, n+1), cr)
            controlled_signed_adder(qc, exz[j+n], dr,
                                    ut.register_range(exz, j, n), cr)
            qc.x(exz[j+n])


def unsigned_divider_gate(m: int, n: int, label: str="udiv") -> Gate:
    """ Create an unsigned divider gate.

        Compute qq, rr such that z = qq * d + rr.

        Usage:
            qc.append(unsigned_divider_gate(m, n), [z1...zm, zz1...zzn, d1...dn, c1...cn])
        
        Effect:
          [z, zz=0, d, c=0] -> [ qq[n:]+rr[:], qq[:n], dr, c=0]
        
        zzr will hold higher n bits or qq.
        lower m-n bits of qq will be held in the higher bits of zr.

        :param m: bit size of z
        :param n: bit size of d
        :param label: label to put on the gate
    """
    zr = QuantumRegister(m, name="z")
    zzr = QuantumRegister(n, name="zz")
    dr = QuantumRegister(n, name="d")
    cr = QuantumRegister(n-1, "c")
    qc = QuantumCircuit(zr, zzr, dr, cr)
    unsigned_divider(qc, zr, zzr, dr, cr)
    return qc.to_gate(label=f"{label}({m},{n})")
