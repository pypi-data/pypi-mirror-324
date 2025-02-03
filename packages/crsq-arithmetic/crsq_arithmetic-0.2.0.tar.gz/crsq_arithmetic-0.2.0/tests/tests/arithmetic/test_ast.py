""" AST class test
"""
import math

from qiskit import QuantumCircuit, QuantumRegister

import crsq_arithmetic as ari
from crsq_arithmetic import ast, test_tools

def do_set_value(total_bits: int, fraction_bits: int, value: float,
                 min_value: int, max_value: int, expected_int_val: int):
    """ set_value test """
    ra = QuantumRegister(total_bits, 'a')
    qc = QuantumCircuit(ra)
    scope = ast.new_scope(qc, is_verbose=True)
    a = scope.register(ra, fraction_bits=fraction_bits, signed=True,
                       min_value=min_value, max_value=max_value)
    a.set_value(value)
    scope.build_circuit()
    qc.save_statevector('Result')
    scope.build_inverse_circuit()
    qc.save_statevector('Reset')
    scope.close()
    expected = {
        'Result': [
            {
                'regs': { 'a': expected_int_val },
                'amp': 1
            }
        ],
        'Reset': [
            {
                'regs': { 'a': 0 },
                'amp': 1
            }
        ]
    }
    test_tools.run_circuit_and_check_many(qc, expected)

def test_set_value():
    """ test set_value for various inputs"""
    do_set_value(5, 0, 13, 0, 31, 13)


def do_iadd(signed: bool, a_bits: int, aval: int, b_bits: int, bval: int,
            c_bits: int, cval: int, cy_bits, msb_bits, msb_value, use_gates: bool):
    """ test iadd
    """
    ra = QuantumRegister(a_bits, 'a')
    rb = QuantumRegister(b_bits, 'b')
    qc = QuantumCircuit(ra,rb)
    ari.set_value(qc, ra, aval)
    ari.set_value(qc, rb, bval)

    scope = ast.new_scope(qc, is_verbose=True)
    scope.use_gates = use_gates
    a = scope.register(ra, signed=signed, max_value=aval, min_value=aval)
    b = scope.register(rb, signed=signed, max_value=bval, min_value=bval)
    b += a  # IAdd
    scope.build_circuit()
    qc.save_statevector('Result')
    scope.build_inverse_circuit()
    qc.save_statevector('Reset')
    scope.close()

    tmp_regs = [ f"tmp{i}" for i in range(cy_bits)]
    expected: dict[str, list[dict[str, int|dict[str, int]]]] = {
        'Result': [
            {
                'regs': {
                    'a': aval,
                    'b': bval + aval,
                    f"[{','.join(tmp_regs)}]": 0
                },
                'amp': 1
            }
        ],
        'Reset': [
            {
                'regs': {
                    'a': aval,
                    'b': bval,
                    f"[{','.join(tmp_regs)}]": 0
                },
                'amp': 1
            }
        ]
    }
    if msb_bits > 0:
        expected['Result'][0]['regs']["msb0"] = msb_value
        expected['Reset'][0]['regs']["msb0"] = 0

    test_tools.run_circuit_and_check_many(qc, expected)


def test_iadd():
    """ test iadd """
    for use_gates in [False, True]:
        # signed. bit extension is suppressed.
        # do_iadd(signed, a_bits, a_val, b_bits, b_val, c_bits, c_val,
        #         cy_bits, msb_bits, msb_val, use_gates)
        do_iadd(True, 4,  3, 4,  2, 4,  5, 4, 0, 0, use_gates)
        do_iadd(True, 4,  7, 4,  1, 4, -8, 4, 0, 0, use_gates)
        do_iadd(True, 4, -8, 4, -8, 4,  0, 4, 0, 0, use_gates)
        # unsigned. bit extension is enabled.
        do_iadd(False, 3,  3, 3,  2, 4,  5, 3, 1, 0, use_gates)
        do_iadd(False, 2,  1, 3,  7, 4,  8, 3, 1, 1, use_gates)
        do_iadd(False, 4,  8, 4,  8, 5, 16, 4, 1, 1, use_gates)

def do_iadd_with_const(signed: bool, a_bits: int, aval: int, b_bits: int, bval: int, cy_bits: int, use_gates: bool):
    """ test iadd
    """
    rb = QuantumRegister(b_bits, 'b')
    qc = QuantumCircuit(rb)
    ari.set_value(qc, rb, bval)

    scope = ast.new_scope(qc, is_verbose=True)
    scope.use_gates = use_gates
    a = scope.constant(aval, total_bits=a_bits, signed=signed)
    b = scope.register(rb, signed=signed, max_value=bval, min_value=bval)
    b += a  # IAdd with const
    cval = bval + aval
    scope.build_circuit()
    qc.save_statevector('Result')
    scope.build_inverse_circuit()
    qc.save_statevector('Reset')
    scope.close()
    tmp_regs = [ f"tmp{i}" for i in range(cy_bits)]
    expected: dict[str, list[dict[str, int|dict[str, int]]]]  = {
        'Result': [
            {
                'regs': {
                    'a': aval,
                    'b': bval + aval,
                    f"[{','.join(tmp_regs)}]": 0
                },
                'amp': 1
            }
        ],
        'Reset': [
            {
                'regs': {
                    'a': aval,
                    'b': bval,
                    f"[{','.join(tmp_regs)}]": 0
                },
                'amp': 1
            }
        ]
    }

    test_tools.run_circuit_and_check_many(qc, expected)

def test_iadd_with_const():
    """ test iadd with const operand"""
    for use_gates in [False, True]:
        do_iadd_with_const(True, 3, 5, 4, 7, 4, use_gates)

def do_isub(n: int, aval: int, bval: int, cy_bits: int, use_gates: bool) -> None:
    """ test isub (in-place sub)"""
    ra = QuantumRegister(n, 'a')
    rb = QuantumRegister(n, 'b')
    qc = QuantumCircuit(ra,rb)
    ari.set_value(qc, ra, aval)
    ari.set_value(qc, rb, bval)

    scope = ast.new_scope(qc, is_verbose=True)
    scope.use_gates = use_gates
    a = scope.register(ra, signed=True, max_value=aval, min_value=0)
    b = scope.register(rb, signed=True, max_value=bval, min_value=0)
    b -= a  # ISub
    scope.build_circuit()
    qc.save_statevector('Result')
    scope.build_inverse_circuit()
    qc.save_statevector('Reset')
    scope.close()

    tmp_regs = [ f"tmp{i}" for i in range(cy_bits)]
    expected: dict[str, list[dict[str, int|dict[str, int]]]] = {
        'Result': [
            {
                'regs': {
                    'a': aval,
                    'b': bval - aval,
                    f"[{','.join(tmp_regs)}]": 0
                },
                'amp': 1
            }
        ],
        'Reset': [
            {
                'regs': {
                    'a': aval,
                    'b': bval,
                    f"[{','.join(tmp_regs)}]": 0
                },
                'amp': 1
            }
        ]
    }

    test_tools.run_circuit_and_check_many(qc, expected)


def test_isub():
    """ test isub """
    for use_gates in [False, True]:
        do_isub(4, 5, 3, 4, use_gates)


def do_sub(n: int, aval: int, bval: int, cy_bits: int, use_gates: bool):
    """ test sub """
    ra = QuantumRegister(n, 'a')
    rb = QuantumRegister(n, 'b')
    qc = QuantumCircuit(ra,rb)
    ari.set_value(qc, ra, aval)
    ari.set_value(qc, rb, bval)

    scope = ast.new_scope(qc, is_verbose=True)
    scope.use_gates = use_gates
    a = scope.register(ra, signed=True, max_value=aval, min_value=0)
    b = scope.register(rb, signed=True, max_value=bval, min_value=0)
    c = b - a  # Sub
    scope.build_circuit()
    qc.save_statevector('Result')
    scope.build_inverse_circuit()
    qc.save_statevector('Reset')
    scope.close()

    sub_regs = [ f"sub{i}" for i in range(n)]
    tmp_regs = [ f"tmp{i}" for i in range(cy_bits)]
    expected: dict[str, list[dict[str, int|dict[str, int]]]] = {
        'Result': [
            {
                'regs': {
                    'a': aval,
                    'b': bval,
                    f"[{','.join(sub_regs)}]": bval - aval,
                    f"[{','.join(tmp_regs)}]": 0,
                },
                'amp': 1
            }
        ],
        'Reset': [
            {
                'regs': {
                    'a': aval,
                    'b': bval,
                    f"[{','.join(sub_regs)}]": 0,
                    f"[{','.join(tmp_regs)}]": 0,
                },
                'amp': 1
            }
        ]
    }

    test_tools.run_circuit_and_check_many(qc, expected)

def test_sub():
    """ test sub"""
    for use_gates in [False, True]:
        do_sub(4, 5, 3, 4, use_gates)

def do_mul(n: int, aval: int, bval: int, use_gates: bool):
    """ test mul """
    ra = QuantumRegister(n, 'a')
    rb = QuantumRegister(n, 'b')
    qc = QuantumCircuit(ra,rb)
    ari.set_value(qc, ra, aval)
    ari.set_value(qc, rb, bval)
    scope = ast.new_scope(qc, is_verbose=True)
    scope.use_gates = use_gates
    a = scope.register(ra)
    b = scope.register(rb)

    _c = a * b  # Multiply

    scope.build_circuit()
    qc.save_statevector('Result')
    scope.build_inverse_circuit()
    qc.save_statevector('Reset')
    scope.close()

    tmp_regs = [ f"tmp{i}" for i in range(2*n)]
    prod_regs = [ f"prod{i}" for i in range(2*n)]
    expected: dict[str, list[dict[str, int|dict[str, int]]]] = {
        'Result': [
            {
                'regs': {
                    'a': aval,
                    'b': bval,
                    f"[{','.join(prod_regs)}]": bval * aval,
                    f"[{','.join(tmp_regs)}]": 0,
                },
                'amp': 1
            }
        ],
        'Reset': [
            {
                'regs': {
                    'a': aval,
                    'b': bval,
                    f"[{','.join(prod_regs)}]": 0,
                    f"[{','.join(tmp_regs)}]": 0,
                },
                'amp': 1
            }
        ]
    }

    test_tools.run_circuit_and_check_many(qc, expected)

def test_mul():
    """ test mul """
    for use_gates in [False, True]:
        do_mul(4, 5, 3, use_gates)


def do_div(m: int, mf: int, n: int, nf: int, z: int, d: int, use_gates: bool):
    """ test div """
    rz = QuantumRegister(m, 'z')
    rd = QuantumRegister(n, 'd')
    qc = QuantumCircuit(rz, rd)
    zval = int(z * (1 << mf))
    dval = int(d * (1 << nf))
    ari.set_value(qc, rz, zval)
    ari.set_value(qc, rd, dval)
    scope = ast.new_scope(qc, is_verbose=True)
    scope.use_gates = use_gates
    z = scope.register(rz, mf)
    d = scope.register(rd, nf)

    q = z / d  # Divide

    assert q.total_bits == m
    assert q.fraction_bits == mf - nf

    scope.build_circuit()
    qc.save_statevector('Result')
    scope.build_inverse_circuit()
    qc.save_statevector('Reset')
    scope.close()

    qq = zval // dval
    rr = zval % dval
    d_str = bin((1<<n) + dval)[-n:]
    qq_str = bin((1<<m) + qq)[-m:]
    rr_str = bin((1<<n) + rr)[-n:]
    qqrr_str = qq_str + rr_str
    zzr_str = qqrr_str[:n]
    zr_str = qqrr_str[n:]

    z_val = int(zr_str, 2)
    zz_val = int(zzr_str, 2)

    tmp_regs = [ f"tmp{i}" for i in range(n)]
    zz_regs = [ f"zz{i}" for i in range(n)]
    expected: dict[str, list[dict[str, int|dict[str, int]]]] = {
        'Result': [
            {
                'regs': {
                    'z': z_val, # result value
                    'd': dval,
                    f"[{','.join(zz_regs)}]": zz_val,
                    f"[{','.join(tmp_regs)}]": 0,
                },
                'amp': 1
            }
        ],
        'Reset': [
            {
                'regs': {
                    'z': zval, # original value
                    'd': dval,
                    f"[{','.join(zz_regs)}]": 0,
                    f"[{','.join(tmp_regs)}]": 0,
                },
                'amp': 1
            }
        ]
    }
    test_tools.run_circuit_and_check_many(qc, expected)

def test_div():
    """ test div """
    for use_gates in [False, True]:
        do_div(7, 3, 5, 1, 7, 2.5, use_gates)

def do_abs(n: int, bval: int, sval, use_gates: bool):
    """ test abs """
    rb = QuantumRegister(n, 'b')
    qc = QuantumCircuit(rb)
    ari.set_value(qc, rb, bval)
    scope = ast.new_scope(qc, is_verbose=True)
    b = scope.register(rb, signed=True)
    b.use_gates = use_gates

    _c = scope.abs(b)  # Absolute

    scope.build_circuit()
    qc.save_statevector('Result')
    scope.build_inverse_circuit()
    qc.save_statevector('Reset')
    scope.close()

    tmp_regs = [ f"tmp{i}" for i in range(n-1)]
    b_res = abs(bval)
    expected: dict[str, list[dict[str, int|dict[str, int]]]] = {
        'Result': [
            {
                'regs': {
                    'b': b_res, # result value
                    'sign0': sval,
                    f"[{','.join(tmp_regs)}]": 0,
                },
                'amp': 1
            }
        ],
        'Reset': [
            {
                'regs': {
                    'b': bval, # original value
                    'sign0': 0,
                    f"[{','.join(tmp_regs)}]": 0,
                },
                'amp': 1
            }
        ]
    }
    test_tools.run_circuit_and_check_many(qc, expected)


def test_abs():
    """ test abs"""
    for use_gates in [False, True]:
        do_abs(4, 3, 0, use_gates)
        do_abs(4, -6, 1, use_gates)

def do_square(n: int, aval: int, use_gates: bool, use_square2: bool):
    """ test square """
    ra = QuantumRegister(n, 'a')
    qc = QuantumCircuit(ra)
    ari.set_value(qc, ra, aval)

    scope = ast.new_scope(qc, is_verbose=True)
    scope.use_gates = use_gates
    scope.set_use_square2(use_square2)
    a = scope.register(ra)
    _c = scope.square(a)  # Square

    scope.build_circuit()
    qc.save_statevector('Result')
    scope.build_inverse_circuit()
    qc.save_statevector('Reset')
    scope.close()

    tmp_regs = [ f"tmp{i}" for i in range(2*n)]
    square_regs = [ f"square{i}" for i in range(2*n)]
    square_val = aval*aval

    expected: dict[str, list[dict[str, int|dict[str, int]]]] = {
        'Result': [
            {
                'regs': {
                    'a': aval,
                    f"[{','.join(square_regs)}]": square_val,
                    f"[{','.join(tmp_regs)}]": 0,
                },
                'amp': 1
            }
        ],
        'Reset': [
            {
                'regs': {
                    'a': aval,
                    f"[{','.join(square_regs)}]": 0,
                    f"[{','.join(tmp_regs)}]": 0,
                },
                'amp': 1
            }
        ]
    }
    test_tools.run_circuit_and_check_many(qc, expected)

def test_square():
    """ test square """
    for use_gates in [False, True]:
        for use_square2 in [False, True]:
            do_square(4, 3, use_gates, use_square2)

def do_square_root(n: int, zval: int, use_gates: bool):
    """ test square root """
    rz = QuantumRegister(n, 'z')
    qc = QuantumCircuit(rz)
    ari.set_value(qc, rz, zval)

    scope = ast.new_scope(qc, is_verbose=True)
    scope.use_gates = use_gates
    z = scope.register(rz)
    _q = scope.square_root(z)  # SquareRoot

    scope.build_circuit()
    qc.save_statevector('Result')
    scope.build_inverse_circuit()
    qc.save_statevector('Reset')
    scope.close()

    ans = int(math.sqrt(zval))
    m = n // 2
    zout = zval - ans*ans
    wout = ans << 1

    tmp_regs = [ f"tmp{i}" for i in range(n)]
    sqrt_regs = [ f"sqrt{i}" for i in range(m)]
    w_regs = [ f"w{i}" for i in range(m, m+m+1)]

    expected: dict[str, list[dict[str, int|dict[str, int]]]] = {
        'Result': [
            {
                'regs': {
                    'z': zout,
                    f"[{','.join(sqrt_regs)}]": ans,
                    f"[{','.join(w_regs)}]": wout,
                    f"[{','.join(tmp_regs)}]": 0,
                },
                'amp': 1
            }
        ],
        'Reset': [
            {
                'regs': {
                    'z': zval,
                    f"[{','.join(sqrt_regs)}]": 0,
                    f"[{','.join(w_regs)}]": 0,
                    f"[{','.join(tmp_regs)}]": 0,
                },
                'amp': 1
            }
        ]
    }
    test_tools.run_circuit_and_check_many(qc, expected)

def test_square_root():
    """ test square root """
    for use_gates in [False, True]:
        do_square_root(8, 144, use_gates)

def do_adjust_precision(total_bits, fraction_bits,
                        new_low_bits, new_high_bits,
                        new_total_bits, new_fraction_bits,
                        old_min_value, old_max_value,
                        new_min_value, new_max_value):
    """ run one test for adjust_precision """
    qr = QuantumRegister(total_bits, 'r')
    qc = QuantumCircuit()
    if new_low_bits is not None:
        qc.add_register(new_low_bits)
    qc.add_register(qr)
    if new_high_bits is not None:
        qc.add_register(new_high_bits)
    scope = ast.new_scope(qc, is_verbose=True)
    r = scope.register(qr, fraction_bits=fraction_bits, signed=False,
                       min_value=old_min_value, max_value=old_max_value)
    s = r.adjust_precision(new_total_bits, new_fraction_bits,
                           new_high_bits, new_low_bits)
    assert s.total_bits == new_total_bits
    assert s.total_bits == s.register.size
    assert s.fraction_bits == new_fraction_bits
    assert s.min_value == new_min_value
    assert s.max_value == new_max_value

def test_adjust_precision():
    """ test adjust_precision """
    do_adjust_precision(8, 3, None, None, 6, 3, 1, 32, 1, 32)  # shrink higher bits
    do_adjust_precision(8, 3, None, None, 6, 1, 4, 128, 1, 32)  # shrink lower bits
    do_adjust_precision(8, 3, None, None, 6, 2, 2, 64, 1, 32)  # shrink lower and higher bits
    do_adjust_precision(6, 2, QuantumRegister(2, "lo"), None, 8, 4, 1, 32, 4, 128)  # add lower bits
    do_adjust_precision(6, 2, None, QuantumRegister(2, "hi"), 8, 2, 1, 32, 1, 32)  # add higher bits

if __name__ == "__main__":
    test_set_value()
    test_iadd()
    test_iadd_with_const()
    test_isub()
    test_sub()
    test_mul()
    test_div()
    test_abs()
    test_square()
    test_square_root()
    test_adjust_precision()
