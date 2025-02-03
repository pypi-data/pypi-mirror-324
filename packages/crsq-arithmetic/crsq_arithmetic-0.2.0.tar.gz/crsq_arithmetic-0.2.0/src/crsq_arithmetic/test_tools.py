""" Test Tools for qiskit quantum circuits
"""

from typing import Any
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
from qiskit.compiler import transpile
from qiskit.quantum_info import Statevector

def _pack_expected_dict(expected: dict[str,complex|float]):
    return { k.replace(' ',''): v for k, v in expected.items() }

def _decompose_key_map(key_map) -> dict[str, int]:
    """ Look for items of style  { "[reg1,reg2,reg3]: val } and
        replace it with { "reg1": bit(val,0), "reg2": bit(val,1), "reg3": bit(val,2)}

        example:
        input : { "x": 1, "y": 2, "[c0,c1,c2]":3 }
        output: { "x": 1, "y": 2, "c0":1, "c1",1, "c2":0 }
    """
    result: dict[str, int] = {}
    for key, val in key_map.items():
        if key[0] == '[':
            if key[len(key)-1] != ']':
                raise ValueError(f"bracket mismatch: '{key}'")
            # key = "[reg1,reg2,reg3]"
            regs_str = key[1:len(key)-1]
            # reg_str = "reg1,reg2,reg3"
            regs = regs_str.split(',')
            # regs = ["reg1", "reg2", "reg3"]
            for i, reg in enumerate(regs):
                mask = 1 << i
                if val & mask != 0:
                    result[reg] = 1
                else:
                    result[reg] = 0
        else:
            result[key] = val
    return result

def _stringify_dict(qc: QuantumCircuit, state_dict: dict[str,int]) -> str:
    """ encode the content of state_dict into a string using the
        register-to-bit position information from qc.
        state_dict contains entries of "register-name" : int_value pairs.
        The register name can be found within qc and the order within qc
        determines the bit range.

        We walk through the register names within qc from the LSB to the MSB
        order. Each name is looked up in state_dict to obtain the bit values.
        The values are encoded in binary digit strings. The strings are
        concatenated.

        Example
        qc.qregs = [ ('a',3), ('b, 4) ]   # LSB is a0, MSB is b3
        state_dict = { 'a': 5, 'b': 11 }
        result: "1011" + "101" = "1011101" # LSB is at the last character in the string.
    """
    result = ""
    d_state_dict = _decompose_key_map(state_dict)
    for reg in qc.qregs:
        if not reg.name in d_state_dict:
            raise ValueError(f"register {reg.name} not found in keymap")
        int_val = d_state_dict[reg.name]
        n = reg.size
        str_val = bin((1<<n+1) + int_val)[-n:]
        # prepend to result
        result = str_val + result
    return result

def _stringify_dict_list(qc: QuantumCircuit, expected: list[dict]) -> dict:
    """ create a dict with entries corresponding to the expected list.
        The items of expected is a dict with keys 'regs' and 'amp' such as:
        { 'regs': {'a': 10, 'b':7, 'x':3, '[c1,c2,c3]':5, }, 'amp': 0.5 }
        The regs dict expresses the values of the registers in qc.
        amp is the amplitude for that combination of register values.
        The register values will be encoded to a binary string whose bit order
        is determined by the registers in the circuit qc.
        The output will look like:
        {
          "100101010": 0.5,
          "010101101": 0.1,
          ...
        }
        This output dict can be compared to a state vector object.
    """
    result = { _stringify_dict(qc, entry['regs']) : entry['amp'] for entry in expected }
    return result

def _decode_state_vector_string(qc: QuantumCircuit, state_vector_string: str) -> dict:
    result = {}
    pos = len(state_vector_string)
    for reg in qc.qregs:
        name = reg.name
        n = reg.size
        bits = state_vector_string[pos-n:pos]
        pos -= n
        result[name] = bits
    return result

EPS=1e-6
INVEPS=1e+6

def _round(v):
    return int(v.real*INVEPS+0.5)*EPS + int(v.imag*INVEPS+0.5)*EPS*1j


def _compare_dicts(qc: QuantumCircuit, result: dict, expected: dict):
    error_count = 0
    for k, v in result.items():
        if k in expected:
            if _round(v) != _round(expected[k]):
                msg = (f"Unexpected: [{k} : {_decode_state_vector_string(qc, k)}] " +
                       f": {v} should be {expected[k]}")
                print(msg)
                error_count += 1
        else:
            if _round(v) != 0:
                msg = (f"Unexpected: [{k} : {_decode_state_vector_string(qc, k)}] , expected : {expected}")
                print(msg)
                error_count += 1
    if error_count > 0:
        raise ValueError(f"{error_count} state(s) did not match expected value : {expected}.")


def run_circuit_and_check(qc: QuantumCircuit,
                          expected: dict[str,complex]|list[dict[str,Any]]):
    """ returns True when qc results match with expected
        qc: Quantum circuit to run
        expected: dict or an array.

        For a dict, the key is state string and value is expected amplitude.
        key may include spaces for readability. e.g. "000100 011010 0"
        The spaces will be removed and the string will be packed before comparison.
        The comparison of the amplitudes is done by comparing 6 digits below the
        decimal point. int(value*1e+6+0.5)

        For an array, each element is a dict with keys 'regs' and 'amp'.
        For key 'regs', the value is a dict from register name to integer value.
        For key 'amp', the value is amplitude for that key (can be in complex numbers).

    """
    if isinstance(expected, list):
        str_dict = _stringify_dict_list(qc, expected)
    else:
        str_dict = _pack_expected_dict(expected)
    aersim = AerSimulator()
    qctr = transpile(qc, aersim)
    result = aersim.run(qctr, shots=1).result()
    sv: Statevector = result.get_statevector()
    result_dict = sv.to_dict()
    _compare_dicts(qc, result_dict, str_dict)

def run_circuit_and_check_many(qc: QuantumCircuit, expected_states: dict):
    """ returns True when qc result statevectors match with the expected values.
        The circuit must include savestatevector(label) calls to store state vectors with labels.

        :param qc: Quantum circuit to run
        :param expected: { 'statevector_label': [{ 'regs': {'reg_name': int_val, }, 'amp': amplitude }, ],  }
    """
    aersim = AerSimulator()
    transpiled = transpile(qc, aersim)
    result = aersim.run(transpiled, shots=1).result()
    for sv_label, one_state in expected_states.items():
        sv: Statevector = result.data()[sv_label]
        result_dict = sv.to_dict()
        str_dict_list = _stringify_dict_list(qc, one_state)
        _compare_dicts(qc, result_dict, str_dict_list)

def dump_statevector_raw(sv: Statevector, eps=1.0e-6):
    """ dump statevector using complex values for the phase """
    for k, z in sorted(sv.to_dict().items()):
        r = abs(z)
        if r > eps:
            # we return the inverse to the original v
            print(f"{k} : z={z:19.6f}")

def dump_statevector_polar(sv: Statevector, eps=1.0e-6):
    """ dump statevector using polar expression for the phase """
    for k, z in sorted(sv.to_dict().items()):
        r = abs(z)
        if r > eps:
            # we return the inverse to the original v
            print(f"{k} : z={z:.6f} |z|={r:.6f} p={r*r:.6f}")
