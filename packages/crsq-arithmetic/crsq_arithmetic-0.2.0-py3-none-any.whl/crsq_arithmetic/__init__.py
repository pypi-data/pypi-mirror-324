""" This module provide functions that generate quantum circuits
    for arithmetic functions.

    The suggested usage is::

        import crsq_arithmetic as ari

        def some_func(a, b, c):
            ari.signed_adder(a,b,c)
    
    The available functions are:

    - adders

      - :py:func:`signed_adder`, :py:func:`signed_adder_gate` - signed adders
      - :py:func:`signed_adderv`, :py:func:`signed_adderv_gate` - signed adders for mismatched bit length
      - :py:func:`controlled_signed_adder`, :py:func:`controlled_signed_adderv` - signed adders with a control bit
      - :py:func:`unsigned_adder`, :py:func:`unsigned_adder_gate` - unsigned adders
      - :py:func:`unsigned_adderv`, :py:func:`unsigned_adderv_gate` - unsigned adders for mismatched bit length
      - :py:func:`scoadder`, :py:func:`scoadder_gate` - signed constant value adders

    - subtractors

      - :py:func:`signed_subtractor`, :py:func:`signed_subtractor_gate` - signed subtractors
      - :py:func:`unsigned_subtractor`, :py:func:`unsigned_subtractor_gate` - unsigned subtractors
      - :py:func:`unsigned_subtractorv`, :py:func:`unsigned_subtractorv_gate` - unsigned subtractors for mismatched bit length

    - multipliers

      - :py:func:`signed_multiplier`, :py:func:`signed_multiplier_gate` - signed multipliers
      - :py:func:`unsigned_multiplier`, :py:func:`unsigned_multiplier_gate` - unsigned multipliers

    - dividers

      - :py:func:`unsigned_divider`, :py:func:`unsigned_divider_gate` - unsigned dividers

    - functions

      - :py:func:`signed_square`, :py:func:`signed_square_gate` - signed squares
      - :py:func:`unsigned_square`, :py:func:`unsigned_square_gate` - unsigned squares
      - :py:func:`square_root`, :py:func:`square_root_gate` - square roots
      - :py:func:`absolute`, :py:func:`absolute_gate` - absolute value
    
"""
from crsq_arithmetic.adder import (
    scoadder, scoadder_gate,
    signed_adder, signed_adder_gate,
    signed_adderv, signed_adderv_gate,
    unsigned_adder, unsigned_adder_gate,
    unsigned_coadder, unsigned_coadder_gate,
    unsigned_adderv, unsigned_adderv_gate,
    controlled_signed_adder, controlled_signed_adder_gate,
    controlled_signed_adderv, controlled_signed_adderv_gate,
    controlled_unsigned_adderv, controlled_unsigned_adderv_gate,
)

names = [
    "scoadder", "scoadder_gate",
    "signed_adder", "signed_adder_gate",
    "signed_adderv", "signed_adderv_gate",
    "unsigned_adder", "unsigned_adder_gate",
    "unsigned_coadder", "unsigned_coadder_gate",
    "unsigned_adderv", "unsigned_adderv_gate",
    "controlled_signed_adder", "controlled_signed_adderv"
]

from crsq_arithmetic.cdk_adder import (
    cdk_adder, cdk_adder_gate
)

names += [ "cdk_adder", "cdk_adder_gate" ]

from crsq_arithmetic.subtractor import (
    signed_subtractor, signed_subtractor_gate,
    signed_cosubtractor, signed_cosubtractor_gate,
    signed_subtractorv, signed_subtractorv_gate,
    signed_o_subtractor, signed_o_subtractor_gate,
    unsigned_subtractor, unsigned_subtractor_gate,
    unsigned_subtractorv, unsigned_subtractorv_gate
)

names += [
    "signed_subtractor", "signed_subtractor_gate",
    "signed_cosubtractor", "signed_cosubtractor_gate",
    "unsigned_subtractor", "unsigned_subtractor_gate",
    "unsigned_subtractorv", "unsigned_subtractorv_gate"
]

from crsq_arithmetic.cdk_subtractor import (
    cdk_subtractor, cdk_subtractor_gate
)

names += [ "cdk_subtractor", "cdk_subtractor_gate" ]

from crsq_arithmetic.cdk_comparator import (
    cdk_comparator, cdk_comparator_gate
)

names += [ "cdk_comparator", "cdk_comparator_gate" ]

from crsq_arithmetic.multiplier import (
    signed_multiplier, signed_multiplier_gate,
    unsigned_multiplier, unsigned_multiplier_gate
)

names += [
    "signed_multiplier", "signed_multiplier_gate",
    "unsigned_multiplier", "unsigned_multiplier_gate"
]

from crsq_arithmetic.square import (
    signed_square, signed_square_gate,
    unsigned_square, unsigned_square_gate
)

names += [
    "signed_square", "signed_square_gate",
    "unsigned_square", "unsigned_square_gate"
]

from crsq_arithmetic.square2 import (
    signed_square2, signed_square2_gate,
    unsigned_square2, unsigned_square2_gate
)

names += [
    "signed_square2", "signed_square2_gate",
    "unsigned_square2", "unsigned_square2_gate"
]

from crsq_arithmetic.divider import (
    unsigned_divider, unsigned_divider_gate
)

names += [
    "unsigned_divider", "unsigned_divider_gate"
]

from crsq_arithmetic.cdk_divider import (
    unsigned_cdk_divider, unsigned_cdk_divider_gate
)

names += [
    "unsigned_cdk_divider", "unsigned_cdk_divider_gate"
]

from crsq_arithmetic.square_root import (
    square_root, square_root_gate
)

names += [
    "square_root", "square_root_gate"
]

from crsq_arithmetic.absolute import (
    absolute, absolute_gate
)

names += [
    "absolute", "absolute_gate"
]

from crsq_arithmetic.cdk_absolute import (
    cdk_absolute, cdk_absolute_gate
)

names += [
    "cdk_absolute", "cdk_absolute_gate"
]

from crsq_arithmetic.utils import (
    bitsize,
    register_range,
    set_bit,
    set_bits,
    set_value
)

names += [
    "bitsize",
    "register_range",
    "set_bit",
    "set_bits",
    "set_value"
]

from crsq_arithmetic.vsqrom import (
    vsqrom1, vsqrom2, vsqrom2_gate
)

names += [
    "vsqrom1", "vsqrom2", "vsqrom2_gate"
]
__all__ = names
