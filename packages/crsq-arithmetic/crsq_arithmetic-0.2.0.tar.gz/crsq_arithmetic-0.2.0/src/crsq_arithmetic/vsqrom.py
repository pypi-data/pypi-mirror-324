""" Variable spacing QROM
"""

from qiskit.circuit import QuantumRegister, QuantumCircuit

def _set_data(qc: QuantumCircuit, ctrlbit: QuantumRegister, qdarray: list[QuantumRegister], values: list[int]):
    prev_bit = ctrlbit
    n = len(qdarray)
    nd = len(values)
    assert n == nd
    for i in range(n):
        qd = qdarray[i]
        bits = values[i]
        nbits = len(qd)
        mask = 1<<(nbits-1)
        for j in range(nbits-1,-1,-1):
            if mask & bits:
                qc.cx(prev_bit, qd[j])
                prev_bit = qd[j]
            mask >>= 1

def vsqrom1(qc: QuantumCircuit, qk: QuantumRegister, qd: list[QuantumRegister],
            qctrl: QuantumRegister, qtmp: QuantumRegister, data: list[list[int]]):
    """ Emit a variable spacing QROM circuit based on given data
        :param qc: target circuit
        :param qk: key (n bits)
        :param qd: data (m bits, little endian, of course)
        :param qctrl: control bit (in a register of its own)
        :param qtmp: temporary bits (n bits)
        :param data: data table (n+1 elements of integers. value will be taken as a bit pattern, stored in qd)
    """
    nkey = len(qk)
    nval = len(qd)
    nctrl = len(qctrl)
    ntmp = len(qtmp)
    ndata = len(data)
    if not (ntmp == nkey and nctrl == 1 and ndata == nkey + 1):
        raise ValueError(f"size mismatch: qk[{nkey}], qd[{nval}], qctrl[{nctrl}] qtmp[{ntmp}] data[{ndata}]")
    j = nkey - 1
    qc.ccx(qk[j], qctrl[0], qtmp[j], ctrl_state='10')
    for j in range(nkey-2, -1, -1):
        qc.ccx(qk[j], qtmp[j+1], qtmp[j], ctrl_state='10')
    j = 0
    _set_data(qc, qtmp[j], qd, data[j])
    for j in range(nkey-1):
        qc.cx(qtmp[j+1], qtmp[j])
        _set_data(qc, qtmp[j], qd, data[j+1])
        qc.ccx(qk[j], qtmp[j+1], qtmp[j])
    j = nkey - 1
    qc.cx(qctrl, qtmp[j])
    _set_data(qc, qtmp[j], qd, data[j+1])
    qc.ccx(qk[j], qctrl, qtmp[j])

def vsqrom2(qc: QuantumCircuit, qk: QuantumRegister, qd: list[QuantumRegister],
            qctrl: QuantumRegister, qtmp: QuantumRegister, data: list[list[int]]):
    """ Emit a variable spacing QROM circuit based on given data
        :param qc: target circuit
        :param qk: key (n bits)
        :param qd: data (m bits, little endian, of course)
        :param qctrl: control bit (0 or 1 bits, in a register of its own)
        :param qtmp: temporary bits (n bits)
        :param data: data table (2*n elements of integers. value will be taken as a bit pattern, stored in qd)
    """
    nkey = len(qk)
    nval = len(qd)
    nctrl = len(qctrl)
    ntmp = len(qtmp)
    ndata = len(data)
    if not (ntmp == nkey and (nctrl == 0 or nctrl == 1) and ndata == 2*nkey):
        raise ValueError(f"size mismatch: qk[{nkey}], qd[{nval}], qctrl[{nctrl}] qtmp[{ntmp}] data[{ndata}]")
    j = nkey - 1

    if nctrl > 0:
        qc.ccx(qk[j], qctrl[0], qtmp[j], ctrl_state='10')
    else:
        qc.cx(qk[j], qtmp[j], ctrl_state=0)

    for j in range(nkey-2, 0, -1):
        qc.ccx(qk[j], qtmp[j+1], qtmp[j], ctrl_state='10')
    j = 0
    _do_half(qc, qk, qtmp, j, qd, data, 2*j)
    for j in range(nkey-2):
        qc.cx(qtmp[j+2], qtmp[j+1])
        _do_half(qc, qk, qtmp, j, qd, data, 2*(j+1))
        qc.ccx(qk[j+1], qtmp[j+2], qtmp[j+1])
    j = nkey - 2

    if nctrl > 0:
        qc.cx(qctrl[0], qtmp[j+1])
    else:
        qc.x(qtmp[j+1])

    _do_half(qc, qk, qtmp, j, qd, data, 2*(j+1))
    if nctrl > 0:
        qc.ccx(qk[j+1], qctrl[0], qtmp[j+1])
    else:
        qc.cx(qk[j+1], qtmp[j+1])

def _do_half(qc: QuantumCircuit, qk: QuantumRegister, qtmp: QuantumRegister, j: int, qd: QuantumRegister, data: list, k):
    qc.ccx(qk[j], qtmp[j+1], qtmp[j], ctrl_state='10')
    # qc.barrier()
    _set_data(qc, qtmp[j], qd, data[k])
    # qc.barrier()
    qc.cx(qtmp[j+1], qtmp[j])
    # qc.barrier()
    _set_data(qc, qtmp[j], qd, data[k+1])
    # qc.barrier()
    qc.ccx(qk[j], qtmp[j+1], qtmp[j])

def vsqrom2_gate(nkey: int, ndata_bits: list[int], data: list[list[int]], num_ctrl = 0, label="vsqrom2"):
    qx = QuantumRegister(nkey, "x")
    num_reg = len(ndata_bits)
    qd = [QuantumRegister(ndata_bits[i], f"a{i}") for i in range(num_reg)]
    qtmp = QuantumRegister(nkey, "tmp")
    qctrl = QuantumRegister(num_ctrl, "ctrl")
    if (num_ctrl > 0) :
        qc = QuantumCircuit(qx, *qd, qctrl, qtmp)
    else:
        qc = QuantumCircuit(qx, *qd, qtmp)
    vsqrom2(qc, qx, qd, qctrl, qtmp, data)
    return qc.to_gate(label=f"{label}({nkey})")
