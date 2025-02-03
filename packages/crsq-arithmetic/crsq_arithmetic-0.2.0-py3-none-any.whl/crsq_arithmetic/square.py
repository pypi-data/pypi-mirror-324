""" Square product functions
"""
from qiskit.circuit import QuantumCircuit, QuantumRegister, Gate
from crsq_arithmetic.adder import signed_adder, signed_adder_gate, unsigned_adder, unsigned_adder_gate, unsigned_adderv, unsigned_adderv_gate, signed_adderv, signed_adderv_gate
import crsq_arithmetic.utils as ut


def unsigned_square(qc: QuantumCircuit, ar: QuantumRegister, dr: QuantumRegister,
                    cr1: QuantumRegister, cr2: QuantumRegister, use_gates: bool = False):
    """ Emit an unsigned square circuit.

        Effect:
            [ar, dr, cr1=0, cr2=0] -> [ar, ar*ar, cr1=0, cr2=0]
        
        :param qc: target circuit
        :param ar: operand (n bits)
        :param dr: product (2*n bits)
        :param cr1: carry for the multiplier (((n+1)//2)*2-1 bits)
        :param cr2: carry for the internal adder (((n+1)//2)*2-2 bits)
    """
    n = ut.bitsize(ar)
    if not (ut.bitsize(cr1) == ((n+1)//2)*2-1 and ut.bitsize(cr2) == ((n+1)//2)*2-2
            and ut.bitsize(dr) == n*2):
        raise ValueError(
            f"size mismatch: ar[{ut.bitsize(ar)}], " +
            f"cr1[{ut.bitsize(cr1)}], cr2[{ut.bitsize(cr2)}], dr[{ut.bitsize(dr)}]")
    if use_gates:
        for k in range(n):
            qc.cx(ar[k], dr[k*2])
        for j in range(n - 3):
            dlen = min(((n+1)//2)*2, (2*n-(2+2*j)))
            for k in range(n - 1 - j):
                qc.ccx(ar[j], ar[j+k+1], cr1[k])
            qc.append(unsigned_adder_gate(dlen-1),
                      ut.register_range(cr1, 0, dlen-1)[:] + 
                      ut.register_range(dr, j*2+2, dlen)[:] +
                      ut.register_range(cr2, 0, dlen-2)[:])
            for k in range(n - 1 - j - 1, -1, -1):
                qc.ccx(ar[j], ar[j+k+1], cr1[k])
        j = n - 3
        qc.ccx(ar[j], ar[j+1], cr1[0])
        qc.ccx(ar[j], ar[j+2], cr1[1])
        qc.ccx(ar[j+1], ar[j+2], cr1[2])
        qc.append(unsigned_adder_gate(3),
                  ut.register_range(cr1, 0, 3)[:] +
                  ut.register_range(dr, j*2+2, 4)[:] +
                  ut.register_range(cr2, 0, 2)[:])
        qc.ccx(ar[j+1], ar[j+2], cr1[2])
        qc.ccx(ar[j], ar[j+2], cr1[1])
        qc.ccx(ar[j], ar[j+1], cr1[0])
    else:
        for k in range(n):
            qc.cx(ar[k], dr[k*2])
        for j in range(n - 3):
            dlen = min(((n+1)//2)*2, (2*n-(2+2*j)))
            for k in range(n - 1 - j):
                qc.ccx(ar[j], ar[j+k+1], cr1[k])
            unsigned_adder(qc, ut.register_range(cr1, 0, dlen-1),
                        ut.register_range(dr, j*2+2, dlen),
                        ut.register_range(cr2, 0, dlen-2))
            for k in range(n - 1 - j - 1, -1, -1):
                qc.ccx(ar[j], ar[j+k+1], cr1[k])
        j = n - 3
        qc.ccx(ar[j], ar[j+1], cr1[0])
        qc.ccx(ar[j], ar[j+2], cr1[1])
        qc.ccx(ar[j+1], ar[j+2], cr1[2])
        unsigned_adder(qc, ut.register_range(cr1, 0, 3),
                    ut.register_range(dr, j*2+2, 4),
                    ut.register_range(cr2, 0, 2))
        qc.ccx(ar[j+1], ar[j+2], cr1[2])
        qc.ccx(ar[j], ar[j+2], cr1[1])
        qc.ccx(ar[j], ar[j+1], cr1[0])


def unsigned_square_gate(n: int, label: str="usquare") -> Gate:
    """ Create an unsigned square gate.
        
        Usage:
            qc.append(unsigned_square_gate(n), [a1...an, d1...d2n, c11...c1n, c21...c2n])

        Effect:
            [a, d=0, c1=0, c2=0] -> [a, a*a, c1=0, c2=0]
        
        :param n: bit size of a
        :param label: label to put on the gate
    """
    ar = QuantumRegister(n, name="a")
    dr = QuantumRegister(2*n, "d")
    c1 = QuantumRegister(((n+1)//2)*2-1, "c1")
    c2 = QuantumRegister(((n+1)//2)*2-2, "c2")
    qc = QuantumCircuit(ar, dr, c1, c2)
    unsigned_square(qc, ar, dr, c1, c2)
    return qc.to_gate(label=f"{label}({n})")


def signed_square(qc: QuantumCircuit, ar: QuantumRegister, dr: QuantumRegister,
                  cr1: QuantumRegister, cr2: QuantumRegister, use_gates: bool = False):
    """ Emit a signed square circuit.

        Effect:
            [ar, dr, cr1=0, cr2=0] -> [ar, ar*ar, cr1=0, cr2=0]
        
        :param qc: target circuit
        :param ar: operand (n bits, n >= 2)
        :param dr: product (2*n bits)
        :param cr1: carry for the multiplier ( ((n+1)//2)*2-1 bits)
        :param cr2: carry for the internal adder ( (n//2)*2 bits)
    """
    n = ut.bitsize(ar)
    if not (n >= 2 and ut.bitsize(cr1) == ((n+1)//2)*2-1 and ut.bitsize(cr2) == (n//2)*2
            and ut.bitsize(dr) == n*2):
        raise ValueError(
            f"size mismatch: ar[{ut.bitsize(ar)}], dr[{ut.bitsize(dr)}], " +
            f"cr1[{ut.bitsize(cr1)}], cr2[{ut.bitsize(cr2)}]")
    if n == 2:
        # special simple case.
        qc.cx(ar[0], dr[0])
        qc.cx(ar[1], dr[2])
        qc.ccx(ar[0], ar[1], dr[2])
        return

    if use_gates:
        for k in range(n):
            qc.cx(ar[k], dr[k*2])

        if (n % 2) == 1:
            # insert one bit we want to add in a sparse
            # list of bits
            qc.x(dr[n])
        else:
            # The one bit we want to set is preoccupied.
            # Increment the bit taking care of the carry
            qc.cx(dr[n], dr[n+1])
            qc.x(dr[n])

        hn = n//2  # half of n
        for j in range(hn):
            # set up cr1
            # count k from the LSB of carry1
            sep = n - 2 - 2*j
            for k in range(0, sep):
                hk = (k+1)//2  # hk[k] = { 0, 1, 1, 2, 2, 3, 3, ... }
                s = hk + j*2 + 1   # first bit in A
                t = k - hk         # second bit in A
                qc.ccx(ar[s], ar[t], cr1[k])
            s = (n+1)//2 + j  # first bit in A
            for k in range((n % 2)+1+j*2):
                t = n - ((n+1)//2) - 1 - j + k  # second bit in A
                qc.ccx(ar[s], ar[t], cr1[sep + k])
                if s == n - 1:
                    qc.x(cr1[sep+k])

            areg_size = ((n+1)//2)*2 - 1
            if j < hn - 1:
                breg_size = min((n*2-1) - (2+2*j) - 1,  (n//2)*2 + 1)
                qc.append(unsigned_adderv_gate(areg_size, breg_size),
                        ut.register_range(cr1, 0, areg_size)[:] +
                        ut.register_range(dr, j*2+2, breg_size+1)[:] +
                        ut.register_range(cr2, 0, breg_size-1)[:])
            else:
                breg_size = ((n+1)//2)*2 - 1
                qc.append(signed_adderv_gate(areg_size, breg_size),
                        ut.register_range(cr1, 0, areg_size)[:] +
                        ut.register_range(dr, j*2+2, breg_size)[:] +
                        ut.register_range(cr2, 0, breg_size-1)[:])
            # undo cr1
            # count k from the LSB of carry1
            sep = n - 2 - 2*j
            s = (n+1)//2 + j  # first bit in A
            for k in range((n % 2)+1+j*2-1,-1,-1):
                if s == n - 1:
                    qc.x(cr1[sep+k])
                t = n - ((n+1)//2) - 1 - j + k  # second bit in A
                qc.ccx(ar[s], ar[t], cr1[sep + k])
            for k in range(sep-1,-1,-1):
                hk = (k+1)//2  # hk[k] = { 0, 1, 1, 2, 2, 3, 3, ... }
                s = hk + j*2 + 1   # first bit in A
                t = k - hk         # second bit in A
                qc.ccx(ar[s], ar[t], cr1[k])


    else:
        for k in range(n):
            qc.cx(ar[k], dr[k*2])

        if (n % 2) == 1:
            # insert one bit we want to add in a sparse
            # list of bits
            qc.x(dr[n])
        else:
            # The one bit we want to set is preoccupied.
            # Increment the bit taking care of the carry
            qc.cx(dr[n], dr[n+1])
            qc.x(dr[n])

        hn = n//2  # half of n
        for j in range(hn):
            # set up cr1
            # count k from the LSB of carry1
            sep = n - 2 - 2*j
            for k in range(0, sep):
                hk = (k+1)//2  # hk[k] = { 0, 1, 1, 2, 2, 3, 3, ... }
                s = hk + j*2 + 1   # first bit in A
                t = k - hk         # second bit in A
                qc.ccx(ar[s], ar[t], cr1[k])
            s = (n+1)//2 + j  # first bit in A
            for k in range((n % 2)+1+j*2):
                t = n - ((n+1)//2) - 1 - j + k  # second bit in A
                qc.ccx(ar[s], ar[t], cr1[sep + k])
                if s == n - 1:
                    qc.x(cr1[sep+k])

            areg_size = ((n+1)//2)*2 - 1
            if j < hn - 1:
                breg_size = min((n*2-1) - (2+2*j) - 1,  (n//2)*2 + 1)
                unsigned_adderv(qc, ut.register_range(cr1, 0, areg_size),
                            ut.register_range(dr, j*2+2, breg_size+1),
                            ut.register_range(cr2, 0, breg_size-1))
            else:
                breg_size = ((n+1)//2)*2 - 1
                signed_adderv(qc, ut.register_range(cr1, 0, areg_size),
                            ut.register_range(dr, j*2+2, breg_size),
                            ut.register_range(cr2, 0, breg_size-1))
            # undo cr1
            # count k from the LSB of carry1
            sep = n - 2 - 2*j
            s = (n+1)//2 + j  # first bit in A
            for k in range((n % 2)+1+j*2-1,-1,-1):
                if s == n - 1:
                    qc.x(cr1[sep+k])
                t = n - ((n+1)//2) - 1 - j + k  # second bit in A
                qc.ccx(ar[s], ar[t], cr1[sep + k])
            for k in range(sep-1,-1,-1):
                hk = (k+1)//2  # hk[k] = { 0, 1, 1, 2, 2, 3, 3, ... }
                s = hk + j*2 + 1   # first bit in A
                t = k - hk         # second bit in A
                qc.ccx(ar[s], ar[t], cr1[k])


def signed_square_gate(n: int, label: str="ssquare", use_gates=False) -> Gate:
    """ Create an signed square gate.
        
        Usage:
            qc.append(signed_square_gate(n), [a1...an, d1...d2n, c11...c1n, c21...c2n])

        Effect:
            [a, d=0, c1=0, c2=0] -> [a, a*a, c1=0, c2=0]
        
        :param n: bit size of a
        :param label: label to put on the gate
    """
    ar = QuantumRegister(n, name="a")
    dr = QuantumRegister(2*n, "d")
    c1 = QuantumRegister(((n+1)//2)*2-1, "c1")
    c2 = QuantumRegister((n//2)*2, "c2")
    qc = QuantumCircuit(ar, dr, c1, c2)
    signed_square(qc, ar, dr, c1, c2, use_gates=use_gates)
    return qc.to_gate(label=f"{label}({n})")
