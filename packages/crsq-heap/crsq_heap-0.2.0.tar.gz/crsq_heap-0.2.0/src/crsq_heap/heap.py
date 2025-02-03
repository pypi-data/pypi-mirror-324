""" Qubit heap management module.

    This module provides a qubit allocator (:py:class:`TemporaryQubitAllocator`)
    and an abstract base class (:py:class:`Frame`) for register holder classes.

    Application programs should subclass Frame to
    define their specific register set class, and add member
    variables to hold QuantumRegister objects.
"""
from typing import List
import logging

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Qubit

logger = logging.getLogger(__name__)

class TemporaryQubitAllocator:
    """ This is a class that maintains a pool of qubits
        that can be allocated and freed.
    """

    def __init__(self, label:str, circuit: QuantumCircuit):
        """ pools free qubits and provides allocate/free functions.
        """
        self.label = label
        self.circuit = circuit
        self.free_qubits: list[QuantumRegister] = []
        self.peak_bit_count = 0
        self.chunk_serial = 0

    @property
    def size(self):
        """ Returns the size of the pool.  This is the sum of
            the number of qubits remaining in the pool and the
            number of qubits that are currently in use.
        """
        return self.peak_bit_count

    def allocate(self, requested: int, label: str) -> list[Qubit]:
        """ Allocate free bits and return as a list of Qubit objects.

            The state of all returned bits will be :math:`\ket{0}`

            After usage, the bits should be returned to the heap by
            free().  The order of calling free does not need to match
            the reverse order of allocation (as with a stack structure).

            :param requested: The number of qubits to allocate.
        """
        while requested > len(self.free_qubits):
            chunk = QuantumRegister(1, f"{label}{self.chunk_serial}")
            self.chunk_serial += 1
            new_bits = chunk[:]
            self.circuit.add_register(chunk)
            self.free_qubits += new_bits
            self.peak_bit_count += chunk.size
        allocated_bits = self.free_qubits[:requested]
        self.free_qubits = self.free_qubits[requested:]
        return allocated_bits

    def free(self, returned_bits: list[Qubit]):
        """ return bits to the allocator.

            Before returning, all bit states must be set to :math:`\ket{0}`

            :param returned_bits: the list of bits to return to the heap.
        """
        self.free_qubits = returned_bits + self.free_qubits


class Binding:
    """ A circuit meant to be turned into a gate, along with a dict of qubit
        specifiers for the parameters

        :param frame: The frame that will be converted to a callee gate and be
            applied to an external caller circuit.
        :param qargs: A dict of arguments. The key names and structures are
            decided by the callee gate. The value is a nested list of
            QuantumRegisters.

    """
    def __init__(self, frame: "Frame", qargs: dict[str, QuantumRegister|list]):
        self._frame = frame
        self._qargs = qargs

    @property
    def circuit(self) -> QuantumCircuit:
        """ The circuit to be invoked as a gate"""
        return self._frame.circuit

    @property
    def params(self) -> List[QuantumRegister]:
        """ The set of expected parameters as a list """
        return self._frame.param_regs

    @property
    def qargs(self) -> dict[str, QuantumRegister]:
        """ The set of argument bits being passed in as a dictionary """
        return self._qargs

    @property
    def label(self) -> str:
        """ The label to be used when converting the circuit into an instruction """
        return self._frame.label

    @classmethod
    def structure_matches(cls, param, arg) -> bool:
        """ Compare the structure of two nested lists of QuantumRegisters """
        if isinstance(param, QuantumRegister) and isinstance(arg, QuantumRegister):
            if param.size != arg.size:
                return False
            return True
        if isinstance(param, list) and isinstance(arg, list):
            if len(param) != len(arg):
                return False
            for (p,a) in zip(param, arg):
                if not cls.structure_matches(p,a):
                    return False
            return True
        return False

    @classmethod
    def flatten(cls, item):
        """ flatten a nested list of QuantumRegisters """
        if isinstance(item, QuantumRegister):
            return [item]
        if not isinstance(item, list):
            raise ValueError("Only list of QuantumRegisters are accepted.")
        result = []
        for child in item:
            result += cls.flatten(child)
        return result

class Frame():
    """ Base class for RegisterSet classes.
        It maintains a set of registers for a program block that will
        be turned into a Qiskit gate or instruction.

        The registers are grouped into arguments, local variables,
        and temporary variables.
    """

    def __init__(self, circuit: QuantumCircuit = None, label: str = ''):
        if circuit is None:
            self._circuit = QuantumCircuit()
        else:
            self._circuit = circuit
        self._label = label
        self._temp_allocator = TemporaryQubitAllocator("tmp", self._circuit)
        self._ancilla_allocator = TemporaryQubitAllocator("anc", self._circuit)
        self._param_regs: list[QuantumRegister] = []
        self._locals: list[QuantumRegister] = []
        self.parent: Frame | None = None
        self._args_fixed: bool = False
        self._locals_fixed: bool = False
        self._heap_fixed: bool = False
        self.alias_regs: dict[str, QuantumRegister] = {}
        self._args_in_parent: list[Qubit]
        self._parent_frame: Frame|None = None
        self._ignore_local_regs: bool = False

    def attach_to_parent_frame(self, parent_frame: "Frame"):
        """ Make this frame a part of the parent frame and belong to the same gate."""
        self._parent_frame = parent_frame

    def param_bits_list(self) -> list[Qubit]:
        """ Return a list of qubits that belong to the arguments.
        """
        assert self._parent_frame is None

        lst = []
        for reg in self._param_regs:
            lst += reg[:]
        return lst

    @property
    def param_regs(self) -> list[QuantumRegister]:
        """ Get a list of argument registers"""
        assert self._parent_frame is None

        return self._param_regs

    @property
    def circuit(self) -> QuantumCircuit:
        """ the associated quantum circuit """
        if self._parent_frame is not None:
            return self._parent_frame.circuit

        return self._circuit

    @property
    def label(self) -> str:
        """ The label for the gate """
        assert self._parent_frame is None

        return self._label

    @property
    def opaque_bit_count(self) -> int:
        """ Return the number of bits that the block requires for
            local vars including ancilla bits and temporary bits.
        """
        assert self._parent_frame is None

        s = 0
        for reg in self._locals:
            s += reg.size
        s += self._ancilla_allocator.size
        s += self._temp_allocator.size
        return s

    def add_param(self, *regs: QuantumRegister|tuple[str,list]):
        """ Declare that a register is an argument.

            The register will be added to the circuit.

            All arguments must be added before locals are added.

            :param regs: Register or a dict.  Entries of the dict are nested
                list of Registers

        """
        if self._parent_frame is not None:
            self._parent_frame.add_param(*regs)
            return

        if self._args_fixed:
            raise ValueError("Argument was added after locals or pool was used.")
        for reg in regs:
            if reg is None:
                pass
            elif isinstance(reg, QuantumRegister):
                self._param_regs.append(reg)
                self._circuit.add_register(reg)
            elif isinstance(reg, tuple):
                (_name, registers) = reg
                self._param_regs.append(reg)
                self._add_nested_registers_to_circuit(registers)
            else:
                raise ValueError(f"Unexpected type in param list: {type(reg)}")

    def _add_nested_registers_to_circuit(self, item):
        if isinstance(item, QuantumRegister):
            self._circuit.add_register(item)
        elif isinstance(item, list):
            for t in item:
                self._add_nested_registers_to_circuit(t)
        else:
            raise ValueError(f"Unexpected type {type(item)}")

    def set_ignore_local_regs(self, ignore_local_regs):
        """ set flag to ignore add_local() calls.
            This is useful when drawing circuit diagrams.
        """
        self._ignore_local_regs = ignore_local_regs

    def add_local(self, *regs: QuantumRegister):
        """ Declare that a register is a local variable.

            The register will be added to the circuit.

            All locals must be added before temporary qubits are allocated.

            Adding the first local variable has the effect of locking
            the list of arguments.
        """
        if self._ignore_local_regs:
            return

        if self._parent_frame is not None:
            self._parent_frame.add_local(*regs)
            return

        if self._locals_fixed:
            raise ValueError("Local var was added after pool was used.")
        if not self._args_fixed:
            self._args_fixed = True
        for reg in regs:
            if reg is None:
                pass
            elif isinstance(reg, QuantumRegister):
                self._locals.append(reg)
                self._circuit.add_register(reg)
            elif isinstance(reg, tuple):
                (_name, registers) = reg
                self._locals.append(reg)
                self._add_nested_registers_to_circuit(registers)
            else:
                raise ValueError(f"Unexpected type in local list: {type(reg)}")

    def allocate_temp_bits(self, n: int) -> list[Qubit]:
        """ allocate temporary bits """
        if self._parent_frame is not None:
            return self._parent_frame.allocate_temp_bits(n)

        if not self._locals_fixed:
            self._locals_fixed = True
            if not self._args_fixed:
                self._args_fixed = True
        return self._temp_allocator.allocate(n, 'tmp')

    def free_temp_bits(self, bit_list: list[Qubit]):
        """ free temporary bits """
        if self._parent_frame is not None:
            self._parent_frame.free_temp_bits(bit_list)
            return

        self._temp_allocator.free(bit_list)

    def allocate_ancilla_bits(self, n: int, label: str) -> list[Qubit]:
        """ allocate temporary bits """
        if self._parent_frame is not None:
            return self._parent_frame.allocate_ancilla_bits(n, label)

        if not self._locals_fixed:
            self._locals_fixed = True
            if not self._args_fixed:
                self._args_fixed = True
        return self._ancilla_allocator.allocate(n, label)

    def free_ancilla_bits(self, bit_list: list[Qubit]):
        """ free temporary bits """
        if self._parent_frame is not None:
            self._parent_frame.free_ancilla_bits(bit_list)
            return

        self._ancilla_allocator.free(bit_list)

    def set_parent(self, parent: "Frame"):
        """ (internal) set the parent register set. """
        self.parent = parent

    def to_gate(self):
        """ convert the circuit into a gate with the label set."""
        assert self._parent_frame is None

        return self._circuit.to_gate(label=self._label)

    def to_instruction(self):
        """ use this when some internals prevent the use of to_gate """
        assert self._parent_frame is None

        return self._circuit.to_instruction(label=self._label)

    def apply(self, sub_frame: "Frame"):
        """ Apply the instructions on the sub_reg_set to this register set.

            :param sub_reg_set: The RegisterSet that holds the instructions to be appended.
        """
        assert self._parent_frame is None

        sub_frame.set_parent(self)
        sub_inst = sub_frame.circuit.to_instruction(label=sub_frame.label)
        temp_bits = self.allocate_temp_bits(sub_frame.opaque_bit_count)
        target_bits = sub_frame.param_bits_list() + temp_bits
        self._circuit.append(sub_inst, target_bits)
        sub_frame.set_args_in_parent(target_bits)
        self.free_temp_bits(temp_bits)

    def set_args_in_parent(self, args_in_parent):
        """ set what the parent is passing as args"""
        self._args_in_parent = args_in_parent

    def apply_instructions(self, circuit: QuantumCircuit):
        """ Apply the instructions in the given circuit as
            individual instructions
        """
        assert self._parent_frame is None

        for inst in circuit.data:
            self._circuit.append(inst.operation, inst.qubits)

    def invoke(self, binding: Binding, invoke_as_instruction=False, inverse=False, label=None):
        """
            Invoke the given circuit with arguments on this receiving
            circuit.
        """
        assert self._parent_frame is None
        self.invoke_with_control(binding, [], '',
                                 invoke_as_instruction=invoke_as_instruction,
                                 inverse=inverse,
                                 label=label)

    def invoke_with_control(self, binding: Binding,
                            ctrl_bits: List[Qubit], ctrl_str: str,
                            invoke_as_instruction=False,
                            inverse=False, label=None):
        """
            Invoke with control bits.
            
            :param binding: The binding object
            :param ctrl_bits: list of control qubits
            :param ctrl_str: a string of '0' and '1' specifying the control bit value.
        """
        params_list = binding.params   # this list is declared as parameters
        qargs_dict = binding.qargs     # the name of params must appear as keys in qargs
        non_none_arg_count = sum(1 for _k, v in qargs_dict.items() if v is not None)
        if len(params_list) != non_none_arg_count:
            raise ValueError("Number of arguments does not match number of expected parameters")
        # make a flat list of registers for both params and args, in the order in the param_list
        flat_params = []
        flat_qargs = []
        for pitem in params_list:
            if pitem is None:
                pass
            if isinstance(pitem, QuantumRegister):
                if not pitem.name in qargs_dict:
                    raise ValueError(f"param '{pitem.name}' not found in bound arguments")
                arg = qargs_dict[pitem.name]
                flat_params.append(pitem)
                flat_qargs.append(arg)
            elif isinstance(pitem, tuple):
                (name, plist) = pitem
                if not name in qargs_dict:
                    raise ValueError(f"param '{name}' not found in bound arguments")
                qarg_item = qargs_dict[name]
                if not Binding.structure_matches(plist, qarg_item):
                    raise ValueError("Parameter structures do not match")
                flat_params += Binding.flatten(plist)
                flat_qargs += Binding.flatten(qarg_item)
            else:
                raise ValueError("Unexpected type")

        # walk through the registers declared on the circuit, and build the target qubit list
        target_qargs: List[Qubit] = []
        used_temp_qubits: List[Qubit] = []
        target_qc = binding.circuit
        qregs = target_qc.qregs
        param_index = 0
        for reg in qregs:
            if param_index < len(flat_params):
                next_param = flat_params[param_index]
                if reg == next_param:
                    qarg = flat_qargs[param_index]
                    self._add_item_to_target(target_qargs, reg, qarg)
                    param_index += 1
                    continue
            self._add_temp_bits_to_target(target_qargs, reg, used_temp_qubits)
        # check if we are at the end of the params list.
        if param_index != len(flat_params):
            raise ValueError("Parameter mismatch. Unused parameter exists.")
        # handle control bits.
        if label is None:
            label = binding.label
        if ctrl_str == '':
            if invoke_as_instruction:
                # logger.info("call to_instruction(1)")
                target_inst = target_qc.to_instruction(label=label)
                # logger.info("call append(1)")
                self._circuit.append(target_inst, target_qargs)
                # logger.info("end append(1)")
                if inverse:
                    raise ValueError("inverse flag is not supported for instruction invocation")
            else:
                # logger.info("call to_gate(2)")
                target_gate = target_qc.to_gate(label=label)
                if inverse:
                    target_gate = target_gate.inverse()
                    target_gate.label = label
                # logger.info("call append(2)")
                self._circuit.append(target_gate, target_qargs)
                # logger.info("end append(2)")
        else:
            # logger.info("call to_gate(3)")
            target_gate = target_qc.to_gate(label=label)
            nb = len(ctrl_str)
            controlled_gate = target_gate.control(nb, ctrl_state=ctrl_str)
            all_bits = ctrl_bits + target_qargs
            # logger.info("call append(3)")
            self._circuit.append(controlled_gate, all_bits)
            # logger.info("end append(3)")
        self.free_temp_bits(used_temp_qubits)

    def _add_item_to_target(self, target_qargs: List[Qubit],
                           param_item: QuantumRegister, arg_item: QuantumRegister):
        if param_item.size != arg_item.size:
            raise ValueError("Register size mismatch between arg " +
                             f"{arg_item.name} and param {param_item.name}.")
        target_qargs += arg_item[:]

    def _add_temp_bits_to_target(self, target_qargs: List[Qubit],
                                 reg: QuantumRegister, used_temp_qubits: List[Qubit]):
        num_bits = reg.size
        temp_qubits = self.allocate_temp_bits(num_bits)
        target_qargs += temp_qubits
        used_temp_qubits += temp_qubits
