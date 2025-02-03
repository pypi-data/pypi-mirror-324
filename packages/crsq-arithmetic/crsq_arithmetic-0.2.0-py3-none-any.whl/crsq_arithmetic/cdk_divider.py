""" cdk_divider gates
"""

from qiskit.circuit import QuantumCircuit, QuantumRegister, Gate
from crsq_arithmetic import cdk_adder, cdk_adder_gate
from crsq_arithmetic import cdk_subtractor, cdk_subtractor_gate
import crsq_arithmetic.utils as ut


def unsigned_cdk_divider(
    qc: QuantumCircuit,
    zr: QuantumRegister,
    zzr: QuantumRegister,
    dr: QuantumRegister,
    cr: QuantumRegister,
    use_gates: bool = False,
):
    """Emit an unsigned cdk_divider circuit.

    Compute rr such that zr = qq * dr + rr.

    Effect:
      [zr, zzr=0, dr, cr=0] -> [ rr[:]+qq[n:], qq[:n], dr, cr=0]

    zzr will hold higher n bits or qq.
    lower m-n bits of qq will be held in the higher bits of zr.

    :param qc: target circuit
    :param zr: [in]left (m bits) / [out] lower mbits of qqrr
    :param zzr: [in] extra result (n bits) = 0 / [out] higher nbits of qqrr
    :param dr: right (n bits)
    :param cr: carry (1 bits)
    """
    m = ut.bitsize(zr)
    n = ut.bitsize(dr)
    nzzr = ut.bitsize(zzr)
    ncr = ut.bitsize(cr)
    if not (nzzr == n and ncr == 1):
        raise ValueError(
            f"size mismatch: zr[{m}], dr[{n}]," + f" zzr[{nzzr}] cr1[{ncr}]"
        )
    if use_gates:
        exz = list(zr) + list(zzr)
        for j in range(m - 1, -1, -1):
            qc.append(
                cdk_subtractor_gate(n, is_unsigned=True),
                dr[:] + ut.register_range(exz, j, n + 1)[:] + cr[:],
            )
            qc.append(
                cdk_adder_gate(n, is_unsigned=False, opt_ctrl_state="1"),
                [exz[j + n]] + dr[:] + ut.register_range(exz, j, n)[:] + cr[:],
            )
            qc.x(exz[j + n])
    else:
        exz = list(zr) + list(zzr)
        for j in range(m - 1, -1, -1):
            cdk_subtractor(
                qc, dr, ut.register_range(exz, j, n + 1), cr, is_unsigned=True
            )
            cdk_adder(
                qc,
                dr,
                ut.register_range(exz, j, n),
                cr,
                is_unsigned=False,
                opt_ctrl_state="1",
                opt_ctrl_bit=exz[j + n],
            )
            qc.x(exz[j + n])


def unsigned_cdk_divider_gate(m: int, n: int, label: str = "udiv") -> Gate:
    """Create an unsigned cdk_divider gate.

    Compute qq, rr such that z = qq * d + rr.

    Usage:
        qc.append(unsigned_cdk_divider_gate(m, n), [z1...zm, zz1...zzn, d1...dn, c1...cn])

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
    cr = QuantumRegister(1, "c")
    qc = QuantumCircuit(zr, zzr, dr, cr)
    unsigned_cdk_divider(qc, zr, zzr, dr, cr)
    return qc.to_gate(label=f"{label}({m},{n})")
