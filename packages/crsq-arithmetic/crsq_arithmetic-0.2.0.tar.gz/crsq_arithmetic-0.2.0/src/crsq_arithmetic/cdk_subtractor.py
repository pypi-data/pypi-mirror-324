""" subtractor gates
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

def cdk_subtractor(
    qc: QuantumCircuit, ar: QuantumRegister, br: QuantumRegister, cr: QuantumRegister,
    is_unsigned: bool=False, opt_ctrl_bit: QubitSpecifier|None=None, opt_ctrl_state:str="1"
):
    """Emit an n bit subtractor circuit

    Effect:
      [ar, br+ar, cr=0] -> [ar, br, cr = 0]

    :param qc: target circuit
    :param ar: left (n bits)
    :param br: right (n+1 bits for unsigned, n for signed)
    :param cr: helper bit (1 bits)
    :param is_unsigned: if True, unsigned subtractor is emitted.
    """
    n = ut.bitsize(ar)
    if not (n >= 2 and
            ((is_unsigned and ut.bitsize(br) == n+1) or (not is_unsigned and ut.bitsize(br) == n)) and
             ut.bitsize(cr) == 1):
        raise ValueError(
            f"size mismatch: ar[{n}], br[{ut.bitsize(br)}], cr[{ut.bitsize(cr)}]"
        )
    if n == 2:
        return _cdk_subtractor_for_n2(qc, ar, br, cr, is_unsigned, opt_ctrl_bit, opt_ctrl_state)
    if n == 3:
        return _cdk_subtractor_for_n3(qc, ar, br, cr, is_unsigned, opt_ctrl_bit, opt_ctrl_state)
    _opt_ctl_cx(qc, ar[0], br[0], opt_ctrl_bit, opt_ctrl_state)
    for i in range(1, n):
        qc.cx(ar[i], br[i])
    qc.cx(ar[1], cr[0])
    _opt_ctl_x(qc, br[1], opt_ctrl_bit, opt_ctrl_state)
    qc.cx(ar[2], ar[1])
    qc.ccx(ar[0], br[0], cr[0])
    _opt_ctl_x(qc, br[2], opt_ctrl_bit, opt_ctrl_state)
    qc.cx(ar[3], ar[2])
    qc.ccx(cr[0], br[1], ar[1])
    for i in range(2, n-2):
        _opt_ctl_x(qc, br[i+1], opt_ctrl_bit, opt_ctrl_state)
        qc.cx(ar[i+2], ar[i+1])
        qc.ccx(ar[i-1], br[i], ar[i])
    qc.ccx(ar[n-3], br[n-2], ar[n-2])
    for i in range(n-1, 1, -1):
        _opt_ctl_cx(qc, ar[i-1], br[i], opt_ctrl_bit, opt_ctrl_state)
    _opt_ctl_cx(qc, cr[0], br[1], opt_ctrl_bit, opt_ctrl_state)
    for i in range(n-2, 0, -1):
        _opt_ctl_x(qc, br[i], opt_ctrl_bit, opt_ctrl_state)
    if is_unsigned:
        _opt_ctl_ccx(qc, ar[n-2], br[n-1], br[n], opt_ctrl_bit, opt_ctrl_state)
        _opt_ctl_cx(qc, ar[n-1], br[n], opt_ctrl_bit, opt_ctrl_state)
    qc.ccx(ar[n-3], br[n-2], ar[n-2])
    for i in range(n-3, 1, -1):
        qc.cx(ar[i+2], ar[i+1])
        qc.ccx(ar[i-1], br[i], ar[i])
    qc.cx(ar[3], ar[2])
    qc.ccx(cr[0], br[1], ar[1])
    qc.cx(ar[2], ar[1])
    qc.ccx(ar[0], br[0], cr[0])
    qc.cx(ar[1], cr[0])
    for i in range(n-1, 0, -1):
        qc.cx(ar[i], br[i])

def _cdk_subtractor_for_n2(
    qc: QuantumCircuit, ar: QuantumRegister, br: QuantumRegister, cr: QuantumRegister,
    is_unsigned: bool, opt_ctrl_bit: QubitSpecifier|None=None, opt_ctrl_state:str="1"):
    """Emit an 3 bit subtractor circuit
    """
    n = ut.bitsize(ar)
    assert(n == 2)

    _opt_ctl_cx(qc, ar[0], br[0], opt_ctrl_bit, opt_ctrl_state)
    qc.cx(ar[1], br[1])
    qc.cx(ar[1], cr[0])
    qc.ccx(ar[0], br[0], cr[0])
    _opt_ctl_cx(qc, cr[0], br[1], opt_ctrl_bit, opt_ctrl_state)
    if is_unsigned:
        _opt_ctl_ccx(qc, cr[0], br[1], br[2], opt_ctrl_bit, opt_ctrl_state)
        _opt_ctl_cx(qc, ar[1], br[2], opt_ctrl_bit, opt_ctrl_state)
    qc.ccx(ar[0], br[0], cr[0])
    qc.cx(ar[1], cr[0])
    qc.cx(ar[1], br[1])


def _cdk_subtractor_for_n3(
    qc: QuantumCircuit, ar: QuantumRegister, br: QuantumRegister, cr: QuantumRegister,
    is_unsigned: bool, opt_ctrl_bit: QubitSpecifier|None=None, opt_ctrl_state:str="1"):
    """Emit an 3 bit subtractor circuit
    """
    n = ut.bitsize(ar)
    assert(n == 3)

    _opt_ctl_cx(qc, ar[0], br[0], opt_ctrl_bit, opt_ctrl_state)
    for i in range(1, n):
        qc.cx(ar[i], br[i])
    qc.cx(ar[1], cr[0])
    _opt_ctl_x(qc, br[1], opt_ctrl_bit, opt_ctrl_state)
    qc.cx(ar[2], ar[1])
    qc.ccx(ar[0], br[0], cr[0])
    qc.ccx(cr[0], br[1], ar[1])
    _opt_ctl_cx(qc, ar[1], br[2], opt_ctrl_bit, opt_ctrl_state)
    _opt_ctl_cx(qc, cr[0], br[1], opt_ctrl_bit, opt_ctrl_state)
    _opt_ctl_x(qc, br[1], opt_ctrl_bit, opt_ctrl_state)
    if is_unsigned:
        _opt_ctl_ccx(qc, ar[1], br[2], br[3], opt_ctrl_bit, opt_ctrl_state)
        _opt_ctl_cx(qc, ar[2], br[3], opt_ctrl_bit, opt_ctrl_state)
    qc.ccx(cr[0], br[1], ar[1])
    qc.cx(ar[2], ar[1])
    qc.ccx(ar[0], br[0], cr[0])
    qc.cx(ar[1], cr[0])
    for i in range(n-1, 0, -1):
        qc.cx(ar[i], br[i])


def cdk_subtractor_gate(n: int, label: str="add", is_unsigned:bool=False, opt_ctrl_state:str|None=None) -> Gate:
    """ Crete an unsigned subtractor gate.
     
        Usage:
          qc.append(unsigned_subtractor_gate(n), [a1,...,an, b1,...,bn+1, c1])

        Effect:
          [a, b+a, c=0] -> [a, b, c=0]
        
        :param n: bit size of a
        :param label: label for the gate.
    """
    ar = QuantumRegister(n, name="a")
    if is_unsigned:
        br = QuantumRegister(n+1, name="b")
    else:
        br = QuantumRegister(n, name="b")
    cr = QuantumRegister(1, "c")
    if opt_ctrl_state is None:
        opt_ctrl_bit = None
        qc = QuantumCircuit(ar, br, cr)
    else:
        opt_ctrl_bit = QuantumRegister(1, "ctrl")
        qc = QuantumCircuit(opt_ctrl_bit, ar, br, cr)
    cdk_subtractor(qc, ar, br, cr, is_unsigned, opt_ctrl_bit, opt_ctrl_state)
    return qc.to_gate(label=f"{label}({n})")
