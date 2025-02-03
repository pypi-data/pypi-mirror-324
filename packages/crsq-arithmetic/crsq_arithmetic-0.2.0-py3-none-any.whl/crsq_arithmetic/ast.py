""" abstract syntax tree types for arithmetic operations

    The entry function is :py:func:`new_scope`

    The main API classes are :py:class:`Scope` and :py:class:`QuantumValue`.
"""

from __future__ import annotations

import re
import math
import abc

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.quantumcircuit import QubitSpecifier
from qiskit.circuit import Gate

from crsq_heap.heap import Frame
import crsq_arithmetic as ari


class Scope(abc.ABC):
    """This is the factory class for AST leaf node objects.
    Use :py:func:`register` to wrap an existing QuantumRegister to
    create an AST node object.

    Arithmetic functions that work on AST nodes are also provided here:

    - :py:func:`square`
    - :py:func:`square_root`
    - :py:func:`abs`

    This class is an interface class. The implementation class is
    a private class defined later in the file.
    """

    # def __init__(self):
    #     self.reg_set: Frame
    #     self.circuit: QuantumCircuit
    #     self.use_gates: bool

    def close(self):
        """release resources"""

    @abc.abstractmethod
    def constant(
        self, value: int, total_bits: int, fraction_bits: int = 0, signed: bool = False
    ) -> Constant:
        """create a constant"""

    @abc.abstractmethod
    def register(
        self,
        register: QuantumRegister,
        fraction_bits: int = 0,
        signed: bool = True,
        min_value: int | None = None,
        max_value: int | None = None,
    ) -> Register:
        """create a register that refers to an externally allocated register

        :param register: The QuantumRegister to be wrapped by the AST node object.
        :param fraction_bits: The number of bits to represent the fraction part.
        :param signed: A flag to denote that the value is signed. (NOT IMPLEMENTED WIDELY YET)
        """

    @abc.abstractmethod
    def abs(self, value: QuantumValue) -> QuantumValue:
        """create a node that computes the absolute value of an input value"""

    @abc.abstractmethod
    def square(self, value: QuantumValue) -> QuantumValue:
        """create a node that computes the square value of an input value"""

    @abc.abstractmethod
    def square_root(self, value: QuantumValue) -> QuantumValue:
        """create a node that computes the square value of an input value"""

    @abc.abstractmethod
    def build_circuit(self) -> QuantumCircuit:
        """build the circuit based on the recorded operations."""

    @abc.abstractmethod
    def build_inverse_circuit(self) -> QuantumCircuit:
        """build a circuit that does the inverse of the operation sequence."""

    @abc.abstractmethod
    def clear_operations(self):
        """clear the recorded operations"""

    @abc.abstractmethod
    def set_verbose(self, flag: bool):
        """Sets verbose flag."""

    @abc.abstractmethod
    def set_use_square2(self, flag: bool):
        """Set to use square2 gate."""


class Value:
    """abstract base class"""

    def __init__(self, scope: _ScopeImp):
        self.scope: _ScopeImp = scope
        self.total_bits: int = 0
        self.fraction_bits: int = 0
        self.signed: bool = False
        self.min_value: int = 0
        self.max_value: int = 0

    def _value_fits_in_range(self) -> bool:
        M = 1 << self.total_bits
        HM = M / 2
        if self.signed:
            range_min = -HM
            range_max = HM - 1
        else:
            range_min = 0
            range_max = M - 1
        return self.min_value >= range_min and self.max_value <= range_max


class Constant(Value):
    """constant value node"""

    def __init__(
        self,
        scope: _ScopeImp,
        value: int,
        total_bits: int,
        fraction_bits: int,
        signed: bool,
    ):
        super().__init__(scope)
        self.value = value
        self.total_bits = total_bits
        self.fraction_bits = fraction_bits
        self.signed = signed
        self.min_value = int(value * 2**fraction_bits)
        self.max_value = int(value * 2**fraction_bits)

    def __iadd__(self, right: Value) -> Value:
        """custom operator implementation for +="""
        new_node = self.scope._create_ciadd(self, right)
        return new_node

    def __isub__(self, right: Value) -> Value:
        """custom operator implementation for -="""
        new_node = self.scope._create_cisub(self, right)
        return new_node

    def __sub__(self, right: Value) -> Value:
        """custom operator implementation for -"""
        new_node = self.scope._create_csub(self, right)
        return new_node

    def __mul__(self, right: Value) -> Value:
        """custom operator implementation for *"""
        new_node = self.scope._create_cmul(self, right)
        return new_node

    def __truediv__(self, right: Value) -> Value:
        """custom operator implementation  for /"""
        new_node = self.scope._create_cdiv(self, right)
        return new_node


class QuantumValue(Value):
    """This is a base class for AST node classes that has a
    value held on a quantum register.
    """

    def __init__(self, scope: _ScopeImp):
        super().__init__(scope)
        self.register: QuantumRegister  # shall be set later.

    def release(self):
        """Release any resources"""

    def __iadd__(self, right: Value) -> QuantumValue:
        """custom operator implementation for +="""
        new_node = self.scope._create_iadd(self, right)
        return new_node

    def __isub__(self, right: Value) -> QuantumValue:
        """custom operator implementation for -="""
        new_node = self.scope._create_isub(self, right)
        return new_node

    def __sub__(self, right: Value) -> QuantumValue:
        """custom operator implementation for -"""
        new_node = self.scope._create_sub(self, right)
        return new_node

    def __mul__(self, right: Value) -> QuantumValue:
        """custom operator implementation for *"""
        new_node = self.scope._create_mul(self, right)
        return new_node

    def __truediv__(self, right: Value) -> QuantumValue:
        """custom operator implementation  for /"""
        new_node = self.scope._create_div(self, right)
        return new_node

    def adjust_precision(
        self,
        total_bits: int,
        fraction_bits: int,
        new_high_bits: list[QubitSpecifier] | None = None,
        new_low_bits: list[QubitSpecifier] | None = None,
    ) -> QuantumValue:
        """Create a node that has some bits added/removed at either the LSB/MSB ends.

        This function will append provided optional bits at the corresponding LSB/MSB ends,
        then chop off bits that are unnecessary based on the new total_bits/fraction_bits
        values.

        :param total_bits: new value for total_bits.
        :param fraction_bits: new value for fraction bits.
        :param new_high_bits: (optional) bits to add at the LSB end.
                              (must be given in little endian order)
        :param new_low_bits: (optional) bits to add at the MSB end.
                             (must be given in little endian order)

        """
        new_node = self.scope.adjust_precision(
            self,
            total_bits,
            fraction_bits,
            new_high_bits=new_high_bits,
            new_low_bits=new_low_bits,
        )
        return new_node

    def mult_pow2(self, num_bits: int):
        new_node = self.scope.mult_pow2(self, num_bits)
        return new_node

    def register_name_with_precision(self) -> str:
        """return a string including name and precision"""
        return self.register.name + self.precision_str()

    def precision_str(self) -> str:
        """return value precision as a string such as '(6.3)'"""
        return f"({self.total_bits},{self.fraction_bits})"

    def emit_circuit(self):
        """emit the gates for this node."""
        # abstract method.

    def _emit_inverse_circuit(self):
        """emit the gates that does the inverse for this node."""

    def close(self):
        """Release resources, if any."""


class Operator(QuantumValue):
    """Node that performs some operation using circuits"""


class SetValueOperator(Operator):
    """A node to emit value preparation operations on a register."""

    def __init__(self, scope: _ScopeImp, register: QuantumRegister, value: int):
        super().__init__(scope)
        self.register = register
        self.value = value
        self.min_value = value
        self.max_value = value

    def emit_circuit(self):
        qc = self.scope.circuit
        ari.set_value(qc, self.register, self.value)

    def _emit_inverse_circuit(self):
        qc = self.scope.circuit
        ari.set_value(qc, self.register, self.value)


class Register(QuantumValue):
    """variable (register) class"""

    def __init__(
        self,
        scope: _ScopeImp,
        register: QuantumRegister,
        fraction_bits: int,
        signed: bool,
        min_value: int | None,
        max_value: int | None,
    ):
        super().__init__(scope)
        self.register = register
        self.total_bits = register.size
        self.fraction_bits = fraction_bits
        self.last_set_value = 0
        self.signed = signed
        M = 1 << self.total_bits
        HM = M // 2
        if min_value is None:
            if signed:
                min_value = -HM
            else:
                min_value = 0
        if max_value is None:
            if signed:
                max_value = HM - 1
            else:
                max_value = M - 1
        self.min_value = min_value
        self.max_value = max_value

    def set_value(self, value: float):
        """Record an operation to set value to the register.
        The former value that was set is recorded, and the
        different bits will be flipped.
        """
        new_value = int(value * (2**self.fraction_bits))
        xor_bits = self.last_set_value ^ new_value
        new_op = SetValueOperator(self.scope, self.register, xor_bits)
        self.scope.add_operator_node(new_op)
        self.last_set_value = new_value
        self.min_value = int(min(self.min_value, value))
        self.max_value = int(max(self.max_value, value))


class BinaryOp(Operator):
    """Binary operator node"""

    def __init__(self, scope: _ScopeImp, left: QuantumValue, right: Value):
        super().__init__(scope)
        self.left = left
        self.right = right
        self.scope.add_operator_node(self)


class UnaryOp(Operator):
    """Unary operator"""

    def __init__(self, scope: _ScopeImp, operand: QuantumValue):
        super().__init__(scope)
        self.operand = operand
        self.scope.add_operator_node(self)


def _make_dagger_gate(gate: Gate) -> Gate:
    inv_gate = gate.inverse()
    inv_gate.label = re.sub(r"\(", "\u2020(", gate.label)
    return inv_gate


class IAdd(BinaryOp):
    """In-place addition node.
    This node will be created when the '+=' operator is used as in:

    ```
    left += right
    ```

    right operand may be a Constant object.
    """

    def __init__(self, scope: _ScopeImp, left: QuantumValue, right: Value):
        """ " constructor"""
        super().__init__(scope, left, right)
        self.right_is_constant = isinstance(right, Constant)
        if not (
            isinstance(left, QuantumValue)
            and (isinstance(right, QuantumValue) or isinstance(right, Constant))
        ):
            raise ValueError("Combination not implemented.")
        if not left.fraction_bits == right.fraction_bits:
            raise ValueError(
                "Fractional bits do not match: "
                + f"left={left.fraction_bits}, right={right.fraction_bits}"
            )
        if not left.total_bits >= right.total_bits:
            raise ValueError(
                "left bits must not be less than right bits.:"
                + f"left={left.total_bits}, right={right.total_bits}"
            )
        if not left.signed == right.signed:
            raise ValueError(
                "signed flag of left and right must match:"
                + f"left={left.signed}, right={right.signed}"
            )
        self.signed = left.signed
        self.total_bits = left.total_bits
        self.fraction_bits = left.fraction_bits
        self.min_value = left.min_value + right.min_value
        self.max_value = left.max_value + right.max_value
        self.register = left.register
        self.new_msb_reg: QuantumRegister = None
        if not self.signed:
            # unsigned adders always have a chance for overflow.
            self._expand_register()

    def _expand_register(self):
        self.new_msb_reg = self.scope.allocate_ancilla_register(1, "msb")
        self.register = QuantumRegister(bits=self.register[:] + self.new_msb_reg[:])
        self.total_bits += 1

    def release(self):
        if self.new_msb_reg is not None:
            self.scope.free_ancilla_register(self.new_msb_reg)

    def emit_circuit(self):
        if self.signed:
            if self.right_is_constant:
                self._emit_circuit_for_scoadder()
            else:
                self._emit_circuit_for_sadderv()
        else:
            if self.right_is_constant:
                self._emit_circuit_for_ucoadder()
            else:
                self._emit_circuit_for_uadderv()

    def _emit_circuit_for_scoadder(self):
        """matched bitsize signed constant adder version
        note that since left.total_bits > right.total_bits,
        we must use scoadderv with y = right, and br = left.
        """
        assert isinstance(self.right, Constant)
        aval = int(self.right.value * (1 << self.right.fraction_bits))
        carry1 = self.scope.allocate_temp_register(self.total_bits - 1)
        qc = self.scope.circuit
        if self.scope.is_verbose:
            print(
                "scoadderv(y) [br] -> [br(br+ar)] " +
                f"y:{aval}, " +
                f"br:{self.register_name_with_precision()}, cr:{carry1.name}")
        if self.right.value == 0:
            """ special case for zero """
            return
        if self.scope.use_gates:
            qc.append(
                ari.scoadder_gate(self.total_bits, aval), self.register[:] + carry1[:]
            )
        else:
            ari.scoadder(qc, aval, self.register, carry1)
        self.scope.free_temp_register(carry1)

    def _emit_circuit_for_sadderv(self):
        """unmatched bitsize signed adderv version
        note that since left.total_bits > right.total_bits,
        we must use signed_adderv with ar = right, and br = left.
        """
        carry1 = self.scope.allocate_temp_register(self.total_bits - 1)
        qc = self.scope.circuit
        assert isinstance(self.right, QuantumValue)
        if self.scope.is_verbose:
            print(
                "signed_adderv [ar,br] -> [ar, br(br+ar)] "
                + f"ar:{self.right.register_name_with_precision()}, "
                + f"br:{self.register_name_with_precision()}, cr:{carry1.name}"
            )
        if self.scope.use_gates:
            qc.append(
                ari.signed_adderv_gate(self.right.total_bits, self.register.size),
                self.right.register[:] + self.register[:] + carry1[:],
            )
        else:
            ari.signed_adderv(qc, self.right.register, self.register, carry1)
        self.scope.free_temp_register(carry1)

    def _emit_circuit_for_uadderv(self):
        """unmatched bitsize unsigned adderv version
        note that since left.total_bits > right.total_bits,
        we must use signed_adderv with ar = right, and br = left.
        """
        num_carry_bits = self.total_bits - 2
        carry1 = self.scope.allocate_temp_register(num_carry_bits)
        qc = self.scope.circuit
        assert isinstance(self.right, QuantumValue)
        if self.scope.is_verbose:
            print(
                "unsigned_adderv [ar,br] -> [ar, br(br+ar)] "
                + f"ar:{self.right.register_name_with_precision()}, "
                + f"br:{self.register_name_with_precision()}, cr:{carry1.name}"
            )
        if self.scope.use_gates:
            qc.append(
                ari.unsigned_adderv_gate(self.right.total_bits, self.register.size - 1),
                self.right.register[:] + self.register[:] + carry1[:],
            )
        else:
            ari.unsigned_adderv(qc, self.right.register, self.register, carry1)
        self.scope.free_temp_register(carry1)

    def _emit_circuit_for_ucoadder(self):
        """matched bitsize unsigned constant adder version
        note that since left.total_bits > right.total_bits,
        we must use scoadderv with y = right, and br = left.
        """
        assert isinstance(self.right, Constant)
        aval = int(self.right.value * (1 << self.right.fraction_bits))
        carry1 = self.scope.allocate_temp_register(self.total_bits - 2)
        qc = self.scope.circuit
        if self.scope.is_verbose:
            print(
                "ucoadder(y) [br] -> [br(br+ar)] "
                + f"y:{aval}, "
                + f"br:{self.register_name_with_precision()}, cr:{carry1.name}"
            )
        if self.scope.use_gates:
            qc.append(
                ari.unsigned_coadder_gate(self.total_bits-1, aval),
                self.register[:] + carry1[:],
            )
        else:
            ari.unsigned_coadder(qc, aval, self.register, carry1)
        self.scope.free_temp_register(carry1)

    def _emit_inverse_circuit(self):
        if self.signed:
            if self.right_is_constant:
                self._emit_inverse_circuit_for_scoadder()
            else:
                self._emit_inverse_circuit_for_sadderv()
        else:
            if self.right_is_constant:
                self._emit_inverse_circuit_for_ucoadder()
            else:
                self._emit_inverse_circuit_for_uadderv()

    def _emit_inverse_circuit_for_scoadder(self):
        """mismatch bitsize signed const adder version"""
        assert isinstance(self.right, Constant)
        if self.right.value == 0:
            """ special case for zero """
            return
        aval = self.right.value * (1 << self.right.fraction_bits)
        carry1 = self.scope.allocate_temp_register(self.total_bits - 1)
        qc = self.scope.circuit
        if self.scope.is_verbose:
            print(
                "inv scoadder (y) [br] <- [br(br+y)] "
                + f"y:{aval}, "
                + f"br:{self.register_name_with_precision()}, cr:{carry1.name}"
            )
        inv_gate = _make_dagger_gate(ari.scoadder_gate(self.register.size, aval))
        qc.append(inv_gate, self.register[:] + carry1[:])
        self.scope.free_temp_register(carry1)

    def _emit_inverse_circuit_for_sadderv(self):
        """mismatch bitsize signed adderv version"""
        carry1 = self.scope.allocate_temp_register(self.total_bits - 1)
        qc = self.scope.circuit
        assert isinstance(self.right, QuantumValue)
        if self.scope.is_verbose:
            print(
                "inv signed_adderv [ar,br] <- [ar, br(br+ar)] "
                + f"ar:{self.right.register_name_with_precision()}, "
                + f"br:{self.register_name_with_precision()}, cr:{carry1.name}"
            )
        inv_gate = _make_dagger_gate(
            ari.signed_adderv_gate(self.right.total_bits, self.register.size)
        )
        qc.append(inv_gate, self.right.register[:] + self.register[:] + carry1[:])
        self.scope.free_temp_register(carry1)

    def _emit_inverse_circuit_for_uadderv(self):
        """mismatch bitsize signed adderv version"""
        num_carry_bits = self.total_bits - 2
        carry1 = self.scope.allocate_temp_register(num_carry_bits)
        qc = self.scope.circuit
        assert isinstance(self.right, QuantumValue)
        if self.scope.is_verbose:
            print(
                "inv unsigned_adderv [ar,br] <- [ar, br(br+ar)] "
                + f"ar:{self.right.register_name_with_precision()}, "
                + f"br:{self.register_name_with_precision()}, cr:{carry1.name}"
            )
        inv_gate = _make_dagger_gate(
            ari.unsigned_adderv_gate(self.right.total_bits, self.register.size - 1)
        )
        qc.append(inv_gate, self.right.register[:] + self.register[:] + carry1[:])
        self.scope.free_temp_register(carry1)

    def _emit_inverse_circuit_for_ucoadder(self):
        """mismatch bitsize unsigned const adder version"""
        assert isinstance(self.right, Constant)
        aval = int(self.right.value * (1 << self.right.fraction_bits))
        carry1 = self.scope.allocate_temp_register(self.total_bits - 2)
        qc = self.scope.circuit
        if self.scope.is_verbose:
            print(
                "inv ucoadder (y) [br] <- [br(br+y)] "
                + f"y:{aval}, "
                + f"br:{self.register_name_with_precision()}, cr:{carry1.name}"
            )
        inv_gate = _make_dagger_gate(
            ari.unsigned_coadder_gate(self.register.size-1, aval)
        )
        qc.append(inv_gate, self.register[:] + carry1[:])
        self.scope.free_temp_register(carry1)


class ISub(BinaryOp):
    """In-place subtraction node.
    This node will be created when the '-=' operator is used as in:

    ```
    left -= right
    ```
    """

    def __init__(self, scope: _ScopeImp, left: QuantumValue, right: Value):
        """ " constructor"""
        super().__init__(scope, left, right)
        self.right_is_constant = isinstance(right, Constant)
        if not (
            isinstance(self.left, QuantumValue)
            and (
                isinstance(self.right, QuantumValue) or isinstance(self.right, Constant)
            )
        ):
            raise ValueError("Combination not implemented.")
        if not left.fraction_bits == right.fraction_bits:
            raise ValueError(
                "Fractional bits do not match: "
                + f"left={left.fraction_bits}, right={right.fraction_bits}"
            )
        if not left.total_bits >= right.total_bits:
            raise ValueError(
                "right bits must not be greater than left bits.:"
                + f"left={left.total_bits}, right={right.total_bits}"
            )
        if not left.signed == right.signed:
            raise ValueError(
                "signed flag of left and right must match:"
                + f"left={left.signed}, right={right.signed}"
            )
        self.signed = left.signed
        self.total_bits = left.total_bits
        self.fraction_bits = left.fraction_bits
        self.min_value = left.min_value - right.max_value
        self.max_value = left.max_value - right.min_value
        self.register = left.register
        self.new_msb_reg: QuantumRegister = None
        if not self.signed:
            # unsigned subtractors always have a chance for underflow.
            self._expand_register()

    def _expand_register(self):
        self.new_msb_reg = self.scope.allocate_ancilla_register(1, "msb")
        self.register = QuantumRegister(bits=self.register[:] + self.new_msb_reg[:])
        self.total_bits += 1

    def release(self):
        if self.new_msb_reg is not None:
            self.scope.free_ancilla_register(self.new_msb_reg)

    def emit_circuit(self):
        if self.signed:
            if self.right_is_constant:
                self._emit_circuit_for_signed_cosubtractor()
            else:
                self._emit_circuit_for_ssubtractorv()
        else:
            if self.right_is_constant:
                self._emit_circuit_for_ucosubtractor()
            else:
                self._emit_circuit_for_usubtractorv()

    def _emit_circuit_for_signed_cosubtractor(self):
        """unmatched bitsize signed constant subtractorv version
        note that since left.total_bits > right.total_bits,
        we must use scoadderv with y = right, and br = left.
        """
        assert isinstance(self.right, Constant)
        print(f"ISub: signed_cosubtractor. value = {self.right.value}")
        if self.right.value == 0:
            """ special case for zero """
            return
        aval = int(self.right.value * (1 << self.right.fraction_bits))
        carry1 = self.scope.allocate_temp_register(self.total_bits - 1)
        qc = self.scope.circuit
        if self.scope.is_verbose:
            print(
                "signed_cosubtractor(y) [br] -> [br(br-ar)] "
                + f"y:{aval}, "
                + f"br:{self.register_name_with_precision()}, cr:{carry1.name}"
            )
        if self.scope.use_gates:
            qc.append(
                ari.signed_cosubtractor_gate(self.total_bits, aval),
                self.register[:] + carry1[:],
            )
        else:
            ari.signed_cosubtractor(qc, aval, self.register, carry1)
        self.scope.free_temp_register(carry1)

    def _emit_circuit_for_ssubtractorv(self):
        """emit for mismatched bit length"""
        carry1 = self.scope.allocate_temp_register(self.total_bits - 1)
        qc = self.scope.circuit
        assert isinstance(self.right, QuantumValue)
        if self.scope.is_verbose:
            print(
                "signed_subtractorv [ar,br] -> [ar, br(br-ar)] "
                + f"ar:{self.right.register_name_with_precision()}, "
                + f"br:{self.register_name_with_precision()}, cr:{carry1.name}"
            )
        if self.scope.use_gates:
            qc.append(
                ari.signed_subtractorv_gate(self.right.total_bits, self.register.size),
                self.right.register[:] + self.register[:] + carry1[:],
            )
        else:
            ari.signed_subtractorv(qc, self.right.register, self.register, carry1)
        self.scope.free_temp_register(carry1)

    def _emit_circuit_for_ucosubtractor(self):
        """unmatched bitsize unsigned constant subtractorv version
        note that since left.total_bits > right.total_bits,
        we must use scoadderv with y = right, and br = left.
        """
        assert isinstance(self.right, Constant)
        aval = int(self.right.value * (1 << self.right.fraction_bits))
        carry1 = self.scope.allocate_temp_register(self.total_bits - 1)
        qc = self.scope.circuit
        if self.scope.is_verbose:
            print(
                "ucoadder(y) [br] -> [br(br-ar)] "
                + f"y:{aval}, "
                + f"br:{self.register_name_with_precision()}, cr:{carry1.name}"
            )
        if self.scope.use_gates:
            qc.append(
                ari.unsigned_cosubtractor_gate(self.total_bits, aval),
                self.register[:] + carry1[:],
            )
        else:
            ari.unsigned_cosubtractor(qc, aval, self.register, carry1)
        self.scope.free_temp_register(carry1)

    def _emit_circuit_for_usubtractorv(self):
        """emit for unsigned subtractor for mismatched input"""
        carry1 = self.scope.allocate_temp_register(self.total_bits - 1)
        qc = self.scope.circuit
        assert isinstance(self.right, QuantumValue)
        if self.scope.is_verbose:
            print(
                "unsigned_subtractorv [ar,br] -> [ar, br(br-ar)] "
                + f"ar:{self.right.register_name_with_precision()}, "
                + f"br:{self.register_name_with_precision()}, cr:{carry1.name}"
            )
        if self.scope.use_gates:
            qc.append(
                ari.unsigned_subtractorv_gate(
                    self.right.total_bits - 1, self.register.size
                ),
                self.right.register[:] + self.register[:] + carry1[:],
            )
        else:
            ari.unsigned_subtractorv(qc, self.right.register, self.register, carry1)
        self.scope.free_temp_register(carry1)

    def _emit_inverse_circuit(self):
        if self.signed:
            if self.right_is_constant:
                self._emit_inverse_circuit_for_signed_cosubtractor()
            else:
                self._emit_inverse_circuit_for_ssubtractorv()
        else:
            self._emit_inverse_circuit_for_usubtractorv()

    def _emit_inverse_circuit_for_signed_cosubtractor(self):
        """mismatch bitsize signed const adder version"""
        assert isinstance(self.right, Constant)
        if self.right.value == 0:
            """ special case for zero """
            return
        aval = self.right.value * (1 << self.right.fraction_bits)
        carry1 = self.scope.allocate_temp_register(self.total_bits - 1)
        qc = self.scope.circuit
        if self.scope.is_verbose:
            print(
                "inv signed_cosubtractor (y) [br] <- [br(br-y)] "
                + f"y:{aval}, "
                + f"br:{self.register_name_with_precision()}, cr:{carry1.name}"
            )
        inv_gate = _make_dagger_gate(
            ari.signed_cosubtractor_gate(self.register.size, aval)
        )
        qc.append(inv_gate, self.register[:] + carry1[:])
        self.scope.free_temp_register(carry1)

    def _emit_inverse_circuit_for_ssubtractorv(self):
        """emit inverse for mismatched bit length"""
        carry1 = self.scope.allocate_temp_register(self.total_bits - 1)
        qc = self.scope.circuit
        assert isinstance(self.right, QuantumValue)
        if self.scope.is_verbose:
            print(
                "inv signed_subtractorv [ar,br] <- [ar, br(br-ar)] "
                + f"ar:{self.right.register_name_with_precision()}, "
                + f"br:{self.register_name_with_precision()}, cr:{carry1.name}"
            )
        inv_gate = _make_dagger_gate(
            ari.signed_subtractorv_gate(self.right.register.size, self.register.size)
        )
        qc.append(inv_gate, self.right.register[:] + self.register[:] + carry1[:])
        self.scope.free_temp_register(carry1)

    def _emit_inverse_circuit_for_usubtractorv(self):
        """ """
        carry1 = self.scope.allocate_temp_register(self.total_bits - 1)
        qc = self.scope.circuit
        assert isinstance(self.right, QuantumValue)
        if self.scope.is_verbose:
            print(
                "inv unsigned_subtractorv [ar,br] <- [ar, br(br-ar)] "
                + f"ar:{self.right.register_name_with_precision()}, "
                + f"br:{self.register_name_with_precision()}, cr:{carry1.name}"
            )
        inv_gate = _make_dagger_gate(
            ari.unsigned_subtractorv_gate(
                self.right.register.size - 1, self.register.size
            )
        )
        qc.append(inv_gate, self.right.register[:] + self.register[:] + carry1[:])
        self.scope.free_temp_register(carry1)


class Sub(BinaryOp):
    """out-of-place subtraction node.
    This node will be created when the '-' operator is used as in:

    ```
    x = left - right
    ```
    """

    def __init__(self, scope: _ScopeImp, left: QuantumValue, right: Value):
        """ " constructor"""
        super().__init__(scope, left, right)
        if (
            not left.total_bits == right.total_bits
            and left.fraction_bits == right.fraction_bits
        ):
            # complex case
            raise ValueError("bit length mismatch is not implemented yet.")
        # simple case
        self.signed = True
        self.total_bits = left.total_bits
        self.fraction_bits = left.fraction_bits
        self.register = self.scope.allocate_ancilla_register(self.total_bits, "sub")
        self.min_value = left.min_value - right.max_value
        self.max_value = left.max_value - right.min_value
        if not self._value_fits_in_range():
            raise ValueError("Sub result may cause overflow.")

    def release(self):
        self.scope.free_ancilla_register(self.register)

    def emit_circuit(self):
        if not (
            isinstance(self.left, QuantumValue) and isinstance(self.right, QuantumValue)
        ):
            raise ValueError("Combination not implemented.")
        carry1 = self.scope.allocate_temp_register(self.total_bits - 1)
        qc = self.scope.circuit
        if self.scope.is_verbose:
            print(
                "signed_o_subtractor [ar,br] -> [ar, br(br-ar)] "
                + f"ar:{self.right.register_name_with_precision()}, "
                + f"br:{self.left.register_name_with_precision()}, "
                + f"dr:{self.register_name_with_precision()}, "
                + f"cr:{carry1.name}"
            )
        if self.scope.use_gates:
            qc.append(
                ari.signed_o_subtractor_gate(self.register.size),
                self.right.register[:]
                + self.left.register[:]
                + self.register[:]
                + carry1[:],
            )
        else:
            ari.signed_o_subtractor(
                qc, self.right.register, self.left.register, self.register, carry1
            )
        self.scope.free_temp_register(carry1)

    def _emit_inverse_circuit(self):
        if not (
            isinstance(self.left, QuantumValue) and isinstance(self.right, QuantumValue)
        ):
            raise ValueError("Combination not implemented.")
        carry1 = self.scope.allocate_temp_register(self.total_bits - 1)
        qc = self.scope.circuit
        if self.scope.is_verbose:
            print(
                "inv signed_o_subtractor [ar,br=dr+ar,dr=0] <- [ar, br, dr] "
                + f"ar:{self.right.register_name_with_precision()}, "
                + f"br:{self.left.register_name_with_precision()}, "
                + f"dr:{self.register_name_with_precision()}, "
                + f"cr:{carry1.name}"
            )
        inv_gate = _make_dagger_gate(ari.signed_o_subtractor_gate(self.register.size))
        qc.append(
            inv_gate,
            self.right.register[:]
            + self.left.register[:]
            + self.register[:]
            + carry1[:],
        )
        self.scope.free_temp_register(carry1)


class Multiply(BinaryOp):
    """Multiplication node
    This node will be created when the '*' operator is used as in:

    ```
    left * right
    ```
    """

    def __init__(self, scope: _ScopeImp, left: QuantumValue, right: Value):
        """ " constructor"""
        super().__init__(scope, left, right)
        if not left.total_bits == right.total_bits:
            # complex case
            raise ValueError("bit length mismatch is not implemented yet.")
        # simple case
        self.total_bits = left.total_bits + right.total_bits
        self.fraction_bits = left.fraction_bits + right.fraction_bits
        # TODO signed flag
        values = [
            left.min_value * right.min_value,
            left.min_value * right.max_value,
            left.max_value * right.min_value,
            left.max_value * right.max_value,
        ]
        if (
            left.min_value * left.max_value <= 0
            or right.min_value * right.max_value <= 0
        ):
            values.append(0)
        self.min_value = int(min(values))
        self.max_value = int(max(values))
        self.carry1_bits = left.total_bits
        self.carry2_bits = left.total_bits - 1
        # self.register = self.scope._new_register('r', self.total_bits)
        self.register = self.scope.allocate_ancilla_register(self.total_bits, "prod")

    def release(self):
        self.scope.free_ancilla_register(self.register)

    def emit_circuit(self):
        if not (
            isinstance(self.left, QuantumValue) and isinstance(self.right, QuantumValue)
        ):
            raise ValueError("Combination not implemented.")
        carry1 = self.scope.allocate_temp_register(self.carry1_bits)
        carry2 = self.scope.allocate_temp_register(self.carry2_bits)
        qc = self.scope.circuit
        if self.scope.is_verbose:
            print(
                "signed_multiplier [ar,br,dr(0)] -> [ar,br,dr(ar*br)]"
                + f"ar:{self.right.register_name_with_precision()}, "
                + f"br:{self.register_name_with_precision()}, cr1:{carry1.name}, "
                + f"cr2:{carry2.name}, dr:{self.register_name_with_precision()}"
            )
        if self.scope.use_gates:
            qc.append(
                ari.signed_multiplier_gate(self.left.register.size),
                self.left.register[:]
                + self.right.register[:]
                + self.register[:]
                + carry1[:]
                + carry2[:],
            )
        else:
            ari.signed_multiplier(
                qc,
                self.left.register,
                self.right.register,
                self.register,
                carry1,
                carry2,
            )
        self.scope.free_temp_register(carry2)
        self.scope.free_temp_register(carry1)

    def _emit_inverse_circuit(self):
        if not (
            isinstance(self.left, QuantumValue) and isinstance(self.right, QuantumValue)
        ):
            raise ValueError("Combination not implemented.")
        carry1 = self.scope.allocate_temp_register(self.carry1_bits)
        carry2 = self.scope.allocate_temp_register(self.carry2_bits)
        qc = self.scope.circuit
        if self.scope.is_verbose:
            print(
                "inv signed_multiplier [ar,br,dr(0)] <- [ar,br,dr(ar*br)]"
                + f"ar:{self.right.register_name_with_precision()}, "
                + f"br:{self.register_name_with_precision()}, cr1:{carry1.name}, "
                + f"cr2:{carry2.name}, dr:{self.register_name_with_precision()}"
            )
        inv_gate = _make_dagger_gate(
            ari.signed_multiplier_gate(self.left.register.size)
        )
        qc.append(
            inv_gate,
            self.left.register[:]
            + self.right.register[:]
            + self.register[:]
            + carry1[:]
            + carry2[:],
        )
        self.scope.free_temp_register(carry2)
        self.scope.free_temp_register(carry1)


class Divide(BinaryOp):
    """Division node
    This node will be created when the '/' operator is used as in:

    ```
    left / right
    ```
    """

    def __init__(self, scope: _ScopeImp, left: QuantumValue, right: Value):
        """ " constructor"""
        super().__init__(scope, left, right)
        if left.signed or right.signed:
            raise ValueError(
                "Divide can take unsigned values only."
                + f"left={left.signed}, right={right.signed}"
            )
        self.new_lower_reg: QuantumRegister | None = None
        if left.total_bits < right.total_bits:
            left = self._expand_left()
            self.left = left
        n = left.total_bits
        m = right.total_bits
        self.signed = False
        self.total_bits = n
        self.fraction_bits = left.fraction_bits - right.fraction_bits
        if scope.use_cdk_divider:
            self.carry_bits = 1
        else:
            self.carry_bits = m - 1
        # self.zz_register = self.scope._new_register('zz', m)
        # self.zz_register = self.scope.allocate_ancilla_register(m, 'zz')
        self.zz_register = self.scope.allocate_temp_register(m)
        self._make_qq_alias()

    def _expand_left(self) -> QuantumValue:
        nl = self.right.total_bits - self.left.total_bits
        self.new_lower_reg = self.scope.allocate_ancilla_register(nl, "lsb")
        new_total_bits = self.left.total_bits + nl
        new_fraction_bits = self.left.fraction_bits + nl
        new_left = self.scope.adjust_precision(
            self.left, new_total_bits, new_fraction_bits, None, self.new_lower_reg[:]
        )
        return new_left

    def release(self):
        # self.scope.free_ancilla_register(self.zz_register)
        self.scope.free_temp_register(self.zz_register)

    def _make_qq_alias(self):
        n = self.total_bits
        quotient_bits = (self.left.register[:] + self.zz_register[:])[-n:]
        alias_serial = self.scope.issue_serial("divider.q")

        self.register = QuantumRegister(bits=quotient_bits, name=f"qq{alias_serial}")

    def emit_circuit(self):
        if not (
            isinstance(self.left, QuantumValue) and isinstance(self.right, QuantumValue)
        ):
            raise ValueError("Combination not implemented.")
        m = self.right.total_bits
        carry = self.scope.allocate_temp_register(self.carry_bits)
        qc = self.scope.circuit
        if self.scope.is_verbose:
            print(
                f"unsigned_divider zr:{self.left.register_name_with_precision()}, "
                + f"zzr:{self.zz_register.name}, dr:{self.right.register_name_with_precision()}, "
                + f"cr:{carry.name} qr:{self.register_name_with_precision()}"
            )
        if self.scope.use_gates:
            if self.scope.use_cdk_divider:
                qc.append(
                    ari.unsigned_cdk_divider_gate(
                        self.left.total_bits, self.right.total_bits
                    ),
                    self.left.register[:]
                    + self.zz_register[:]
                    + self.right.register[:]
                    + carry[:],
                )
            else:
                qc.append(
                    ari.unsigned_divider_gate(
                        self.left.total_bits, self.right.total_bits
                    ),
                    self.left.register[:]
                    + self.zz_register[:]
                    + self.right.register[:]
                    + carry[:],
                )
        else:
            if self.scope.use_cdk_divider:
                ari.unsigned_cdk_divider(
                    qc, self.left.register, self.zz_register, self.right.register, carry
                )
            else:
                ari.unsigned_divider(
                    qc, self.left.register, self.zz_register, self.right.register, carry
                )
        self.scope.free_temp_register(carry)

    def _emit_inverse_circuit(self):
        if not (
            isinstance(self.left, QuantumValue) and isinstance(self.right, QuantumValue)
        ):
            raise ValueError("Combination not implemented.")
        carry = self.scope.allocate_temp_register(self.carry_bits)
        qc = self.scope.circuit
        if self.scope.is_verbose:
            print(
                f"inv unsigned_divider zr:{self.left.register_name_with_precision()}, "
                + f"zzr:{self.zz_register.name}, dr:{self.right.register_name_with_precision()}, "
                + f"cr:{carry.name} qr:{self.register_name_with_precision()}"
            )
        if self.scope.use_cdk_divider:
            inv_gate = _make_dagger_gate(
                ari.unsigned_cdk_divider_gate(
                    self.left.total_bits, self.right.total_bits
                )
            )
        else:
            inv_gate = _make_dagger_gate(
                ari.unsigned_divider_gate(self.left.total_bits, self.right.total_bits)
            )
        qc.append(
            inv_gate,
            self.left.register[:]
            + self.zz_register[:]
            + self.right.register[:]
            + carry[:],
        )
        self.scope.free_temp_register(carry)


class Absolute(UnaryOp):
    """Absolute value node.
    This node will be created when the scope.abs() function is used as in:

    ```
    scope.abs(value)
    ```
    """

    def __init__(self, scope: _ScopeImp, operand: QuantumValue):
        """ " constructor"""
        super().__init__(scope, operand)
        if not isinstance(operand, QuantumValue):
            raise ValueError("Unsupported type")
        if not operand.signed:
            raise ValueError("Absolute can take signed values only.")
        self.total_bits = operand.total_bits
        self.fraction_bits = operand.fraction_bits
        # result is an unsigned value.
        self.signed = False
        # evaluate the resulting range.
        values = [abs(operand.min_value), abs(operand.max_value)]
        if operand.min_value * operand.max_value <= 0:
            values.append(0)
        self.min_value = int(min(values))
        self.max_value = int(max(values))
        self.carry_bits = operand.total_bits - 1
        self.register = operand.register
        self.sign_register = self.scope.allocate_ancilla_register(1, "sign")

    def release(self):
        self.scope.free_ancilla_register(self.sign_register)

    def emit_circuit(self):
        if not isinstance(self.operand, QuantumValue):
            raise ValueError("Combination not implemented.")
        carry = self.scope.allocate_temp_register(self.carry_bits)
        qc = self.scope.circuit
        if self.scope.is_verbose:
            print(
                "absolute [br,s(0)] -> [br(abs(br)),s(sign(br))]"
                + f"br:{self.register_name_with_precision()}, cr:{carry.name}, "
                + f"s:{self.sign_register.name}"
            )
        if self.scope.use_gates:
            qc.append(
                ari.absolute_gate(self.operand.total_bits),
                self.register[:] + self.sign_register[:] + carry[:],
            )
        else:
            ari.absolute(qc, self.operand.register, self.sign_register[0], carry)
        self.scope.free_temp_register(carry)

    def _emit_inverse_circuit(self):
        if not isinstance(self.operand, QuantumValue):
            raise ValueError("Combination not implemented.")
        carry = self.scope.allocate_temp_register(self.carry_bits)
        qc = self.scope.circuit
        if self.scope.is_verbose:
            print(
                "inv absolute [br,s(0)] -> [br(abs(br)),s(sign(br))]"
                + f"br:{self.register_name_with_precision()}, cr:{carry.name}, "
                + f"s:{self.sign_register.name}"
            )
        inv_gate = _make_dagger_gate(ari.absolute_gate(self.operand.total_bits))
        qc.append(inv_gate, self.register[:] + self.sign_register[:] + carry[:])
        self.scope.free_temp_register(carry)


class Square(UnaryOp):
    """Square node.
    This node will be created when the scope.square() function is used as in:

    ```
    scope.square(value)
    ```
    """

    def __init__(self, scope: _ScopeImp, operand: QuantumValue):
        """ " constructor"""
        super().__init__(scope, operand)
        if not isinstance(operand, QuantumValue):
            raise ValueError("Unsupported type")
        self.total_bits = operand.total_bits * 2
        self.fraction_bits = operand.fraction_bits * 2
        self.signed = False
        values = [
            operand.min_value * operand.min_value,
            operand.max_value * operand.max_value,
        ]
        if operand.min_value * operand.max_value <= 0:
            values.append(0)
        self.min_value = int(min(values))
        self.max_value = int(max(values))
        # self.register = scope._new_register('d', self.total_bits)
        self.register = scope.allocate_ancilla_register(self.total_bits, "square")
        if self.scope.use_square2:
            self.carry1_bits = operand.total_bits + 1
            self.carry2_bits = 1
        else:
            self.carry1_bits = ((operand.total_bits + 1) // 2) * 2 - 1
            self.carry2_bits = (operand.total_bits // 2) * 2

    def release(self):
        self.scope.free_ancilla_register(self.register)

    def emit_circuit(self):
        if not isinstance(self.operand, QuantumValue):
            raise ValueError("Combination not implemented.")
        carry1 = self.scope.allocate_temp_register(self.carry1_bits, "c1")
        carry2 = self.scope.allocate_temp_register(self.carry2_bits, "c2")
        qc = self.scope.circuit
        if self.scope.is_verbose:
            print(
                f"signed_square ar:{self.operand.register_name_with_precision()}, "
                + f"cr1:{carry1.name}, cr2:{carry2.name}, "
                + f"dr:{self.register_name_with_precision()}"
            )
        if self.scope.use_gates:
            # argument order ar, dr, cr1, cr2: dr = ar * ar
            if self.scope.use_square2:
                qc.append(
                    ari.signed_square2_gate(self.operand.register.size),
                    self.operand.register[:] + self.register[:] + carry1[:] + carry2[:],
                )
            else:
                qc.append(
                    ari.signed_square_gate(self.operand.register.size),
                    self.operand.register[:] + self.register[:] + carry1[:] + carry2[:],
                )
        else:
            # argument order qc, ar, cr1, cr2, dr: dr = ar * ar
            if self.scope.use_square2:
                ari.signed_square2(
                    qc, self.operand.register, self.register, carry1, carry2
                )
            else:
                ari.signed_square(
                    qc, self.operand.register, self.register, carry1, carry2
                )
        self.scope.free_temp_register(carry2)
        self.scope.free_temp_register(carry1)

    def _emit_inverse_circuit(self):
        if not isinstance(self.operand, QuantumValue):
            raise ValueError("Combination not implemented.")
        carry1 = self.scope.allocate_temp_register(self.carry1_bits, "c")
        carry2 = self.scope.allocate_temp_register(self.carry2_bits, "c")
        qc = self.scope.circuit
        if self.scope.is_verbose:
            print(
                f"inv signed_square ar:{self.operand.register_name_with_precision()}, "
                + f"cr1:{carry1.name}, cr2:{carry2.name}, "
                + f"dr:{self.register_name_with_precision()}"
            )
        # argument order ar, dr, cr1, cr2: dr = ar * ar
        if self.scope.use_square2:
            inv_gate = _make_dagger_gate(
                ari.signed_square2_gate(self.operand.register.size)
            )
        else:
            inv_gate = _make_dagger_gate(
                ari.signed_square_gate(self.operand.register.size)
            )
        qc.append(
            inv_gate,
            self.operand.register[:] + self.register[:] + carry1[:] + carry2[:],
        )
        self.scope.free_temp_register(carry2)
        self.scope.free_temp_register(carry1)


class SquareRoot(UnaryOp):
    """Square root node.
    This node will be created when the scope.square_root() function is used as in:

    ```
    scope.square_root(value)
    ```
    """

    def __init__(self, scope: _ScopeImp, operand: QuantumValue):
        """ " constructor"""
        super().__init__(scope, operand)
        if not isinstance(operand, QuantumValue):
            raise ValueError("Unsupported type")
        if operand.signed:
            raise ValueError("SquareRoot can take unsigned values only.")
        self.new_msb_reg: QuantumRegister = None
        if operand.total_bits % 2 == 1:
            # input has odd number of bits.
            operand = self._expand_operand()
            self.operand = operand
        self.total_bits = operand.total_bits // 2
        self.fraction_bits = operand.fraction_bits // 2
        self.signed = False
        self.min_value = int(math.sqrt(operand.min_value))
        self.max_value = int(math.sqrt(operand.max_value))
        self.register = scope.allocate_ancilla_register(self.total_bits, "sqrt")
        self.work_register = scope.allocate_ancilla_register(self.total_bits + 1, "w")
        self.carry_bits = self.total_bits * 2 - 1

    def _expand_operand(self):
        operand = self.operand
        self.new_msb_reg = self.scope.allocate_ancilla_register(1, "msb")
        new_operand = self.scope.adjust_precision(
            operand,
            operand.total_bits + 1,
            operand.fraction_bits,
            new_high_bits=self.new_msb_reg[:],
            new_low_bits=None,
        )
        return new_operand

    def release(self):
        self.scope.free_ancilla_register(self.work_register)
        self.scope.free_ancilla_register(self.register)
        if self.new_msb_reg is not None:
            self.scope.free_ancilla_register(self.new_msb_reg)

    def emit_circuit(self):
        if not isinstance(self.operand, QuantumValue):
            raise ValueError("Combination not implemented.")
        carry = self.scope.allocate_temp_register(self.carry_bits)
        qc = self.scope.circuit
        if self.scope.is_verbose:
            print(
                f"square_root zr:{self.operand.register_name_with_precision()}, "
                + f"rr:{self.register_name_with_precision()}, wr:{self.work_register.name}, "
                + f"cr:{carry.name}"
            )
        if self.scope.use_gates:
            qc.append(
                ari.square_root_gate(self.total_bits),
                self.operand.register[:]
                + self.register[:]
                + self.work_register[:]
                + carry[:],
            )
        else:
            # argument order qc, zr, rr, wr, cr: zr = rr * rr + wr
            ari.square_root(
                qc, self.operand.register, self.register, self.work_register, carry
            )
        self.scope.free_temp_register(carry)

    def _emit_inverse_circuit(self):
        if not isinstance(self.operand, QuantumValue):
            raise ValueError("Combination not implemented.")
        carry = self.scope.allocate_temp_register(self.carry_bits)
        qc = self.scope.circuit
        if self.scope.is_verbose:
            print(
                f"square_root zr:{self.operand.register_name_with_precision()}, "
                + f"rr:{self.register_name_with_precision()}, wr:{self.work_register.name}, "
                + f"cr:{carry.name}"
            )
        inv_gate = _make_dagger_gate(ari.square_root_gate(self.total_bits))
        qc.append(
            inv_gate,
            self.operand.register[:]
            + self.register[:]
            + self.work_register[:]
            + carry[:],
        )
        self.scope.free_temp_register(carry)


class _ScopeImp(Scope):
    """Scope implementation"""

    def __init__(self, src: Frame | QuantumCircuit, is_verbose: bool):
        """constructor"""
        super().__init__()
        if isinstance(src, Frame):
            frame = src
        if isinstance(src, QuantumCircuit):
            frame = Frame(src)
        self.reg_set = frame
        self.circuit = frame._circuit
        self.operator_nodes: list[QuantumValue] = []
        self.use_gates = True
        self._register_index = 0
        self.is_closed = False
        self.pending_registers_are_added = False
        self.pending_new_registers: list[QuantumRegister] = []
        self.serial_counters: dict[str, int] = {}
        self.is_verbose = is_verbose
        self.use_square2 = True
        self.use_cdk_divider = True

    def close(self):
        if self.is_closed:
            return
        self.is_closed = True
        self.clear_operations()

    def _new_register(self, label: str, num_bits: int) -> QuantumRegister:
        idx = self._register_index
        self._register_index += 1
        name = label + str(idx)
        reg = QuantumRegister(num_bits, name)
        self.pending_new_registers.append(reg)
        return reg

    def _remove_register_from_pending_list(self, reg: QuantumRegister):
        if reg in self.pending_new_registers:
            self.pending_new_registers.remove(reg)

    def allocate_temp_register(self, num_bits: int, label="tmp") -> QuantumRegister:
        """Allocate temporary register from bits in the heap"""
        bits = self.reg_set.allocate_temp_bits(num_bits)
        label = f"{label}{self.issue_serial(label)}"
        reg = QuantumRegister(name=label, bits=bits)
        return reg

    def free_temp_register(self, reg: QuantumRegister):
        """Return allocated register to the heap"""
        self.reg_set.free_temp_bits(reg[:])

    def allocate_ancilla_register(self, num_bits: int, label="anc") -> QuantumRegister:
        """Allocate temporary register from bits in the heap"""
        bits = self.reg_set.allocate_ancilla_bits(num_bits, label)
        label = f"{label}{self.issue_serial(label)}"
        reg = QuantumRegister(name=label, bits=bits)
        return reg

    def free_ancilla_register(self, reg: QuantumRegister):
        """Return allocated register to the heap"""
        self.reg_set.free_ancilla_bits(reg[:])

    def issue_serial(self, key: str) -> int:
        """Issue a serial number with given key."""
        if not key in self.serial_counters:
            self.serial_counters[key] = 0
        count = self.serial_counters[key]
        self.serial_counters[key] += 1
        return count

    def constant(
        self, value: int, total_bits: int, fraction_bits: int = 0, signed: bool = False
    ) -> Constant:
        new_const = Constant(self, value, total_bits, fraction_bits, signed)
        return new_const

    def register(
        self,
        register: QuantumRegister,
        fraction_bits: int = 0,
        signed: bool = False,
        min_value: int | None = None,
        max_value: int | None = None,
    ) -> Register:
        new_register = Register(
            self, register, fraction_bits, signed, min_value, max_value
        )
        return new_register

    def abs(self, value: QuantumValue) -> QuantumValue:
        new_abs = Absolute(self, value)
        return new_abs

    def square(self, value: QuantumValue) -> QuantumValue:
        new_square = Square(self, value)
        return new_square

    def square_root(self, value: QuantumValue) -> QuantumValue:
        new_square_root = SquareRoot(self, value)
        return new_square_root

    def add_operator_node(self, node: QuantumValue):
        """add an operator node to the operator list"""
        self.operator_nodes.append(node)

    def _create_iadd(self, left: QuantumValue, right: Value) -> QuantumValue:
        new_iadd = IAdd(self, left, right)
        return new_iadd

    def _create_isub(self, left: QuantumValue, right: Value) -> QuantumValue:
        new_isub = ISub(self, left, right)
        return new_isub

    def _create_sub(self, left: QuantumValue, right: Value) -> QuantumValue:
        new_sub = Sub(self, left, right)
        return new_sub

    def _create_mul(self, left: QuantumValue, right: Value) -> QuantumValue:
        new_mul = Multiply(self, left, right)
        return new_mul

    def _create_div(self, left: QuantumValue, right: Value) -> QuantumValue:
        new_div = Divide(self, left, right)
        return new_div

    def adjust_precision(
        self,
        operand: QuantumValue,
        total_bits: int,
        fraction_bits: int,
        new_high_bits: list[QubitSpecifier] | None,
        new_low_bits: list[QubitSpecifier] | None,
    ) -> QuantumValue:
        """Adjust precision
                      |<--1-->|<-2->|         1+2: operand.total_bits, 2: operand.fraction_bits
        input:        |z|z|z|z|f|f|f|
                  |<3>|             |<4>|     3: new_high_bits.size, 4: new_low_bits.size
        new_bits: |h|h|             |l|l|
                  |<----5---->|<---6--->|     5+6: base_total_bits, 6: base_fraction_bits
                    |<---7--->|<--8-->|       7+8: total_bits, 8: fraction_bits
        output:     |z|z|z|z|z|f|f|f|f|
                                      |<|     start_pos
                    |<------------------|     end_pos
        """
        if operand.signed:
            raise ValueError("adjust_precision can take unsigned values only.")
        if new_high_bits is None:
            new_high_bits = []
        if new_low_bits is None:
            new_low_bits = []
        base_reg = operand.register
        reg_name = base_reg.name + "_adj"
        base_bits = new_low_bits[:] + base_reg[:] + new_high_bits[:]
        base_total_bits = len(base_bits)
        base_fraction_bits = operand.fraction_bits + len(new_low_bits)
        if fraction_bits > base_fraction_bits:
            raise ValueError(
                f"requested fraction_bits {fraction_bits} "
                + f"exceeds available bits {base_fraction_bits}"
            )
        end_pos = base_fraction_bits - fraction_bits + total_bits
        avail_for_total = base_total_bits - fraction_bits
        if end_pos > base_total_bits:
            raise ValueError(
                f"requested total_bits {total_bits} exceeds "
                + f"available bits {avail_for_total}"
            )
        start_pos = base_fraction_bits - fraction_bits
        new_bits = base_bits[start_pos:end_pos]

        new_reg = QuantumRegister(name=reg_name, bits=new_bits)
        base_value_shift = len(new_low_bits) - start_pos
        if base_value_shift > 0:
            new_min_value = operand.min_value << base_value_shift
            new_max_value = operand.max_value << base_value_shift
        else:
            new_min_value = operand.min_value >> -base_value_shift
            new_max_value = operand.max_value >> -base_value_shift
        new_reg_node = Register(
            self, new_reg, fraction_bits, operand.signed, new_min_value, new_max_value
        )
        return new_reg_node

    def mult_pow2(self, operand: QuantumValue, num_bits: int) -> QuantumValue:
        new_fraction_bits = operand.fraction_bits - num_bits
        if new_fraction_bits > operand.total_bits:
            raise ValueError("Fraction bits exceeds total bits.")
        if num_bits > 0:
            new_min_value = operand.min_value << num_bits
            new_max_value = operand.max_value << num_bits
        else:
            new_min_value = operand.min_value >> -num_bits
            new_max_value = operand.max_value >> -num_bits
        new_node = Register(
            self,
            operand.register,
            new_fraction_bits,
            operand.signed,
            new_min_value,
            new_max_value,
        )
        return new_node

    def _add_registers_to_circuit(self):
        if self.pending_registers_are_added:
            return
        self.pending_registers_are_added = True
        self.circuit.add_register(*self.pending_new_registers)

    def build_circuit(self) -> QuantumCircuit:
        """build the circuit."""
        self._add_registers_to_circuit()
        for node in self.operator_nodes:
            node.emit_circuit()
        return self.circuit

    def build_inverse_circuit(self) -> QuantumCircuit:
        """build the inverse circuit."""
        for node in reversed(self.operator_nodes):
            node._emit_inverse_circuit()
        return self.circuit

    def clear_operations(self):
        """clear the recorded operations"""
        for node in reversed(self.operator_nodes):
            node.release()
        self.operator_nodes.clear()

    def set_verbose(self, flag):
        """set the verbose flag."""
        self.is_verbose = flag

    def set_use_square2(self, flag):
        self.use_square2 = flag

    def set_use_cdk_divider(self, flag):
        self.use_cdk_divider = flag


def new_scope(reg_set: Frame | QuantumCircuit, is_verbose=False) -> Scope:
    """API to create a new scope object.  The entry point for the AST package."""
    return _ScopeImp(reg_set, is_verbose)
