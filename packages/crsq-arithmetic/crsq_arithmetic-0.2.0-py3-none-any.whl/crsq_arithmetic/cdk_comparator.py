""" Adder gates
"""

from qiskit.circuit import QuantumCircuit, QuantumRegister, Gate
from qiskit.circuit.library import C3XGate
from qiskit.circuit.quantumcircuit import QubitSpecifier

import crsq_arithmetic.bit_ops as bb
import crsq_arithmetic.utils as ut

def _opt_ctl_x(qc:QuantumCircuit, target:QubitSpecifier, opt_ctrl_bit: QubitSpecifier|None, opt_ctrl_state:str="1"):
    if opt_ctrl_bit is None:
        qc.x(target)
    else:
        qc.cx(opt_ctrl_bit, target, ctrl_state=opt_ctrl_state)

def _opt_ctl_cx(qc:QuantumCircuit, ctrl_bit: QubitSpecifier, target:QubitSpecifier, opt_ctrl_bit: QubitSpecifier|None, opt_ctrl_state:str="1"):
    if opt_ctrl_bit is None:
        qc.cx(ctrl_bit, target)
    else:
        qc.ccx(ctrl_bit, opt_ctrl_bit, target, ctrl_state="1"+opt_ctrl_state)

def _opt_ctl_ccx(qc:QuantumCircuit, ctrl1_bit: QubitSpecifier, ctrl2_bit: QubitSpecifier,
                 target:QubitSpecifier, opt_ctrl_bit: QubitSpecifier|None, opt_ctrl_state:str="1"):
    if opt_ctrl_bit is None:
        qc.ccx(ctrl1_bit, ctrl2_bit, target)
    else:
        qc.append(C3XGate(ctrl_state="11"+opt_ctrl_state), [opt_ctrl_bit, ctrl1_bit, ctrl2_bit, target])

def cdk_comparator(
    qc: QuantumCircuit, ar: QuantumRegister, br: QuantumRegister, cr: QuantumRegister,
    opt_ctrl_bit: QubitSpecifier|None=None, opt_ctrl_state:str="1"
):
    """Emit an n bit comparator circuit

    Effect:
      [ar, br, cr=0] -> [ar, br, cr = 1] when ar > br, otherwise cr = 0

    :param qc: target circuit
    :param ar: left (n bits)
    :param br: right (n+1 bits for unsigned, n for signed)
    :param cr: helper bit (1 bits)
    :param opt_ctrl_bit: if not None, this will be used as a control bit.
    """
    n = ut.bitsize(ar)
    if not (n >= 2 and (ut.bitsize(br) == n+1) and ut.bitsize(cr) == 1):
        raise ValueError(
            f"size mismatch: ar[{n}], br[{ut.bitsize(br)}], cr[{ut.bitsize(cr)}]"
        )
    if n == 2:
        return _cdk_cmp_for_n2(qc, ar, br, cr, opt_ctrl_bit, opt_ctrl_state)
    if n == 3:
        return _cdk_cmp_for_n3(qc, ar, br, cr, opt_ctrl_bit, opt_ctrl_state)
    for i in range(1, n):
        qc.cx(ar[i], br[i])
    qc.cx(ar[1], cr[0])
    qc.x(br[0])
    qc.ccx(ar[0], br[0], cr[0])
    qc.x(br[1])
    qc.cx(ar[2], ar[1])
    qc.ccx(cr[0], br[1], ar[1])
    qc.x(br[2])
    qc.cx(ar[3], ar[2])
    for i in range(2, n-2):
        qc.ccx(ar[i-1], br[i], ar[i])
        qc.x(br[i+1])
        qc.cx(ar[i+2], ar[i+1])
    qc.ccx(ar[n-3], br[n-2], ar[n-2])
    qc.x(br[n-1])
    
    _opt_ctl_cx(qc, ar[n-1], br[n], opt_ctrl_bit, opt_ctrl_state)  # asymmetry
    _opt_ctl_ccx(qc, ar[n-2], br[n-1], br[n], opt_ctrl_bit, opt_ctrl_state)  # center

    # reverse the first half

    qc.x(br[n-1])
    qc.ccx(ar[n-3], br[n-2], ar[n-2])
    for i in range(n-3, 1, -1):
        qc.ccx(ar[i-1], br[i], ar[i])
        qc.x(br[i+1])
        qc.cx(ar[i+2], ar[i+1])
    qc.cx(ar[3], ar[2])
    qc.x(br[2])
    qc.ccx(cr[0], br[1], ar[1])
    qc.cx(ar[2], ar[1])
    qc.x(br[1])
    qc.ccx(ar[0], br[0], cr[0])
    qc.x(br[0])
    qc.cx(ar[1], cr[0])
    for i in range(n-1, 0, -1):
        qc.cx(ar[i], br[i])


def _cdk_cmp_for_n2(
    qc: QuantumCircuit, ar: QuantumRegister, br: QuantumRegister, cr: QuantumRegister,
    opt_ctrl_bit: QubitSpecifier|None=None, opt_ctrl_state:str="1"):
    """Emit an 3 bit adder circuit
    """
    n = ut.bitsize(ar)
    assert(n == 2)

    qc.cx(ar[1], br[1])

    qc.x(br[0])
    qc.cx(ar[1], cr[0])

    qc.ccx(ar[0], br[0], cr[0])
    qc.x(br[1])

    _opt_ctl_cx(qc, ar[1], br[2], opt_ctrl_bit, opt_ctrl_state)  # asymmetry
    _opt_ctl_ccx(qc, cr[0], br[1], br[2], opt_ctrl_bit, opt_ctrl_state)  # center

    qc.x(br[1])
    qc.ccx(ar[0], br[0], cr[0])

    qc.cx(ar[1], cr[0])
    qc.x(br[0])

    qc.cx(ar[1], br[1])


def _cdk_cmp_for_n3(
    qc: QuantumCircuit, ar: QuantumRegister, br: QuantumRegister, cr: QuantumRegister,
    opt_ctrl_bit: QubitSpecifier|None=None, opt_ctrl_state:str="1"):
    """Emit an 3 bit adder circuit
    """
    n = ut.bitsize(ar)
    assert(n == 3)
    for i in range(1, n):
        qc.cx(ar[i], br[i])

    qc.x(br[0])
    qc.cx(ar[1], cr[0])

    qc.ccx(ar[0], br[0], cr[0])
    qc.x(br[1])

    qc.cx(ar[2], ar[1])
    qc.ccx(cr[0], br[1], ar[1])
    qc.x(br[2])

    _opt_ctl_cx(qc, ar[2], br[3], opt_ctrl_bit, opt_ctrl_state)
    _opt_ctl_ccx(qc, ar[1], br[2], br[3], opt_ctrl_bit, opt_ctrl_state)

    qc.x(br[2])
    qc.ccx(cr[0], br[1], ar[1])
    qc.cx(ar[2], ar[1])

    qc.x(br[1])
    qc.ccx(ar[0], br[0], cr[0])

    qc.cx(ar[1], cr[0])
    qc.x(br[0])

    for i in range(n-1, 0, -1):
        qc.cx(ar[i], br[i])


def cdk_comparator_gate(n: int, label: str="cmp", opt_ctrl_state:str|None=None) -> Gate:
    """ Crete an unsigned adder gate.
     
        Usage:
          qc.append(unsigned_adder_gate(n), [a1,...,an, b1,...,bn+1, c1])

        Effect:
          [a, b, c=0] -> [a, b, c=1] when ar > br, otherwise cr = 0
        
        :param n: bit size of a
        :param label: label for the gate.
    """
    ar = QuantumRegister(n, name="a")
    br = QuantumRegister(n+1, name="b")
    cr = QuantumRegister(1, "c")
    if opt_ctrl_state is None:
        opt_ctrl_bit = None
        qc = QuantumCircuit(ar, br, cr)
    else:
        opt_ctrl_bit = QuantumRegister(1, "ctrl")
        qc = QuantumCircuit(opt_ctrl_bit, ar, br, cr)
    cdk_comparator(qc, ar, br, cr,opt_ctrl_bit, opt_ctrl_state)
    return qc.to_gate(label=f"{label}({n})")
