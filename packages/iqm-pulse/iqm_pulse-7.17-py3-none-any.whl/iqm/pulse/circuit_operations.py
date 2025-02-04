#  ********************************************************************************
#  Copyright (c) 2022-2025 IQM Finland Oy.
#  All rights reserved. Confidential and proprietary.
#
#  Distribution or reproduction of any information contained herein
#  is prohibited without IQM Finland Oy’s prior written permission.
#  ********************************************************************************
"""Methods for operating on lists of CircuitOperation objects."""
from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from typing import Self

import numpy as np

from iqm.pulse.builder import CircuitOperation, build_quantum_ops, validate_quantum_circuit
from iqm.pulse.quantum_ops import QuantumOpTable


def reorder(mat: np.ndarray, perm: list[int]) -> np.ndarray:
    """Reorders the qubits in the n-qubit operator A according to the permutation vector perm.

    Args:
        mat: Matrix to reorder
        perm: Permutation

    Returns:
        Reordered matrix
    """

    iperm = np.argsort(perm)
    shape = mat.shape
    assert shape[0] == shape[1]  # must be square
    n_qubits = int(np.log2(shape[0]))  # must be a power of two

    if set(iperm) != set(range(n_qubits)):
        raise ValueError(f"Invalid {n_qubits}-qubit permutation: {perm}.")

    dims = [2] * n_qubits
    total_dims = dims * 2
    iperm = np.array(iperm)
    total_perm = np.r_[iperm, iperm + n_qubits]

    # big-endian ordering
    # reshape A into another tensor which has one index per qubit, permute dimensions,
    # back into a tensor with the original number of indices
    return mat.reshape(total_dims).transpose(total_perm).reshape(shape)


def reshape_unitary(unitary: np.ndarray, indices: Sequence[int], n_qubits: int) -> np.ndarray:
    """Extend a unitary propagator to act on a larger system.

    Given a unitary matrix acting on N qubits, indices of N qubits in a larger Hilbert space, and the number
    of qubits in that Hilbert space, calculate a unitary acting on the larger Hilbert space, which acts as
    the given unitary on the N selected qubits and as identity on the others.

    Args:
        unitary: original unitary
        indices: qubit indices in the larger Hilbert space, all in ``range(num_qubits)``
        n_qubits: number of qubits in the larger Hilbert space

    Returns:
        Unitary matrix acting as ``unitary`` on the selected qubits in the larger Hilbert space.
    """
    n_indices = len(indices)
    dim = 1 << n_indices
    if unitary.shape != (dim, dim):
        raise ValueError(f"Unitary does not have the correct dimension {dim}.")

    permutation = list(indices) + [i for i in range(n_qubits) if i not in indices]
    big_unitary = np.kron(unitary, np.eye(1 << (n_qubits - n_indices)))
    return reorder(big_unitary, permutation)


def get_unitary_from_op(op: CircuitOperation, table: QuantumOpTable, qubits: list[str]) -> np.ndarray:
    """Unitary matrix representing an operation within the context of the circuit.

    First, fetches the unitary corresponding to the correct operation from the QuantumOpTable. If that unitary
    is a function, gets the matrix by calling the function with values of quantum operation params stored
    in the operation. Checks whether the size of the unitary is correct. Then, optionally extends that unitary to act
    on the Hilbert space of the entire circuit.

    Args:
        op: quantum operation instance
        table: registered quantum operations
        qubits: qubits of the whole circuit, in big-endian order

    Returns:
        Unitary matrix representing ``op`` on the Hilbert space of the circuit.
    """
    try:
        parent_op = table[op.name]
    except KeyError as excp:
        raise KeyError(f"The operation {op.name} cannot be found in the QuantumOpTable.") from excp

    if parent_op.arity == 0:
        return np.eye(2 ** len(qubits))

    base_unitary_gen = parent_op.unitary
    if base_unitary_gen is None:
        raise ValueError(f"The operation {op.name} is not unitary or not fully defined over the computational space.")

    base_unitary = base_unitary_gen(**op.args)

    locus_indices = [qubits.index(qb) for qb in op.locus]

    return reshape_unitary(base_unitary, locus_indices, len(qubits))


def get_unitary_from_circuit(
    circuit: list[CircuitOperation], table: QuantumOpTable | None = None, qubit_names: list[str] | None = None
) -> np.ndarray:
    """Calculate the overall unitary implemented by a sequence of CircuitOperations.

    Iterate through the list of operations, skipping over barrier operations, and calculate the unitary
    for each operation, and then calculate the matrix product of all of them. The unitary definition must be present
    in the QuantumOpTable given as the second argument.

    Args:
        circuit: list of CircuitOperations in order
        table: Table of all registered quantum ops.
        qubit_names: Optionally, the ordering of the qubits.
    Returns:
        Array describing the action of the circuit in big endian convention.
    """
    table = table or build_quantum_ops({})
    qubit_names = qubit_names or _get_qubit_order_from_circuit(circuit)
    unitary = np.eye(2 ** len(qubit_names))  # in case of empty list
    for operation in circuit:
        unitary = get_unitary_from_op(operation, table, qubit_names) @ unitary

    return unitary


def _get_qubit_order_from_circuit(circuit: list[CircuitOperation]):
    """Get all qubits which are in the circuit in order."""
    # unique items, in the same order
    return list(dict.fromkeys(qb for op in circuit for qb in op.locus))


class CircuitOperationList(list):
    """A list of :class:`iqm.pulse.builder.CircuitOperation` objects with methods to add, remove and transform them.

    The class is used to work with :class:`~iqm.pulse.builder.CircuitOperation` s directly. It is mostly meant as
    convenience to enable easy creation of circuits, calculations of their properties, and mapping them onto physical
    qubits. In addition to the list of contents, this class has two important attributes: ``qubits`` and ``table``.
    The former defines the list of qubits which are allowed to be in the loci of all the
    :class:`~iqm.pulse.builder.CircuitOperation` s present in the list. Think about it as the qiskit's Quantum
    Register. The latter is a :class:`iqm.pulse.quantum_ops.QuantumOpTable`, which contains all the
    :class:`~iqm.pulse.quantum_ops.QuantumOp` s which are allowed to be in the circuit. In most cases, the table is
    simply taken to contain all the default operations defined in iqm-pulse. If using this class in the context of a
    :class:`~iqm.pulse.builder.ScheduleBuilder`, it is good practice to set ``table = builder.op_table``. The
    :class:`~iqm.pulse.quantum_ops.QuantumOpTable` is mutable, so any additional registered gates will automatically
    be possible to be used in any CircuitOperationList associated with that
    :class:`~iqm.pulse.builder.ScheduleBuilder` instance.

    The fundamental use of the class would be to first define a new instance::

        circuit = CircuitOperationList(num_qubits=2)

    The `num_qubits` parameter populates the `.qubits` argument with qubits QB1-QBn, in this case ``['QB1', 'QB2']``.

    Alternatively, you can use ``qubits`` directly::

        circuit = CircuitOperationList(qubits=['QB1', 'QB2'])

    To add your own QuantumOpTable, initialize like this::

        circuit = CircuitOperationList(num_qubits=2, table=my_table)

    Remembering that the table is mutable.

    If you already have a list of CircuitOperations, you can initialize with it::

        circuit = CircuitOperationList(circuit_ops, table=my_table)
        circuit.find_qubits()

    Calling the :meth:`find_qubits` populates the :attr:`qubits` attribute with the qubits found in loci of
    the operations included in the original circuit. If the list is empty, it will set :attr:`qubits` to an empty list,
    which most of the time is not what you want to do.

    The class has the add, multiply, and get_item methods redefined, which means all the following: ``circuit * 3``,
    ``circuit1 + circuit2``, and ``circuit[0:4]`` will produce a CircuitOperationList with the same :attr:`qubits`
    and :attr:`table` attributes as the original.

    To add a prx operation to the list, call::

        circuit.add_op('prx', [0], angle, phase, impl_name='drag_crf')

    The class also has shortcut methods defined, so the above can be shortened to::

        circuit.prx(angle, phase, 0, impl_name='drag_crf')

    Which is exactly the same syntax as in qiskit + implementation name, which usually does not need to be used. The
    names of the shortcut methods are taken from the attached `table` at init. All the operations with non-zero arity
    will be added as shortcuts.

    If all the operations in the circuit are unitary, you can quickly calculate the unitary of the entire circuit
    by calling::

        U = circuit.get_unitary()

    The dimension of the unitary will always be defined by the :attr:`qubits` attribute. In particular, if your circuit
    contains 3 qubits, ``'QB1', 'QB2', 'QB3'``, but you only add gates to the first two, the resulting unitary will
    still be an 8x8 matrix, corresponding to the three qubits ``'QB1', 'QB2', 'QB3'``, in the big endian convention.
    With no operations affecting ``'QB3'``, you should expect the action of the unitary on this qubit to be an identity.

    To map the circuit onto physical qubits, all you need to do is call::

        physical_circuit = circuit.map_loci(physical_qubits)

    This will create a copy of the circuit, with all the placeholder qubits replaced by the physical qubits, with the
    order defined by the :attr:`qubits` attribute. For example, if ``qubits = ['QB1', 'QB2', 'QB3']``, and
    ``physical_qubits = ['QB2', 'QB5', 'QB10']``, all occurrences of ``'QB1'`` will be mapped to ``'QB2'``, ``'QB2'``
    to ``'QB5'`` and ``'QB3'`` to ``'QB10'``. The original circuit is not modified, so you can create many copies with
    different physical qubits, which is helpful when running parallel experiments on a large chip.

    Args:
        args: a list of CircuitOperation objects. Can be empty.
        qubits: a list of qubits allowed to be in the circuit.
        num_qubits: the number of qubits allowed to be in the circuit. Ignored if ``qubits`` is given.
        table: table containing allowed quantum operations.
    """

    qubits: list[str] = []

    def __init__(
        self, *args, qubits: list[str] | None = None, num_qubits: int = 0, table: QuantumOpTable | None = None
    ):
        list.__init__(self, *args)
        if qubits:
            self.qubits = qubits
        else:
            self.add_qubits(num_qubits)
        self.table: QuantumOpTable = table or build_quantum_ops({})
        for op_name in self.table:
            if self.table[op_name].arity:
                self._set_specific_operation_shortcut(op_name)

    def __getitem__(self, item) -> CircuitOperationList | CircuitOperation:
        """For the builtin list, this method is used both for accessing a single element: ``mylist[0]`` and accessing
        a slice: ``mylist[1:3]``. The latter should generate a new CircuitOperationList, so we override the method to
        ensure that it does."""
        result = list.__getitem__(self, item)
        if isinstance(result, list):
            new = CircuitOperationList(result)
            new.qubits = self.qubits
            new.table = self.table
            return new

        return result

    def __add__(self, other) -> CircuitOperationList:
        new = CircuitOperationList(list.__add__(self, other))
        new.qubits = self.qubits
        new.table = self.table

        return new

    def __mul__(self, other) -> CircuitOperationList:
        new = CircuitOperationList(list.__mul__(self, other))
        new.qubits = self.qubits
        new.table = self.table
        return new

    def find_qubits(self) -> None:
        """Set attribute qubits to qubits in the loci of operations in the list."""
        self.qubits = list(dict.fromkeys(qb for operation in self for qb in operation.locus))

    def add_qubits(self, n: int) -> None:
        """Adds generic placeholder qubits from 1 to n."""
        self.qubits = [f"QB{i+1}" for i in range(n)]

    def get_unitary(self, qubit_names: list[str] | None = None) -> np.ndarray:
        """Calculate the overall unitary implemented by a sequence of CircuitOperations.

        Args:
            self: list of CircuitOperations in order
            qubit_names: Optionally, the ordering of the qubits.
        Returns:
            Array describing the action of the circuit in big endian convention.
        """
        qubit_names = qubit_names or self.qubits
        validate_quantum_circuit(self, self.table)
        return get_unitary_from_circuit(self, self.table, qubit_names)

    def add_op(
        self,
        name: str,
        locus_indices: Sequence[int],
        *args,
        impl_name: str | None = None,
    ) -> None:
        """Adds a new :class:`CircuitOperation` to the circuit.

        Appends a new :class:`~iqm.pulse.builder.CircuitOperation` at the end of the list. The
        :class:`CircuitOperation` is created using a :class:`~iqm.pulse.quantum_ops.QuantumOp` name from the
        QuantumOpTable attached to the CircuitOperationList. The locus of that
        :class:`~iqm.pulse.builder.CircuitOperation` is built from the qubits stored in :attr:`qubits`, by selecting
        the qubits at indices given by ``locus_indices``. For example, if :attr:`qubits` is ``['QB1', 'QB2',
        'QB4']``, and the ``locus_indices`` is ``[2, 1]``, the locus of the new
        :class:`~iqm.pulse.builder.CircuitOperation` will be ``('QB4', 'QB2')``. All arguments for the values of the
        params of the requested :class:`~iqm.pulse.quantum_ops.QuantumOp` need to be provided.

        Args:
            name: Name of the :class:`QuantumOp` which will generate a new :class:`CircuitOperation`.
            locus_indices: Indices of the qubits in the attribute .qubits which will become the locus of the operation.
            args: Any arguments the CircuitOperation needs, must correspond to the params of the :class:`QuantumOp`.
            impl_name: Name of the implementation to use when converting the :class:`CircuitOperation` into
                a :class:`Timebox` later.
        """
        qubit_names = self.qubits
        if name not in self.table:
            raise KeyError(f"QuantumOp with name {name} is not in the gate definitions table.")
        arity = self.table[name].arity
        if len(locus_indices) != len(set(locus_indices)):
            raise ValueError("Repeated locus indices.")
        if arity and arity != len(locus_indices):  # arity = 0 is barrier and measure
            raise ValueError(f"Operation {name} has {arity=} but {len(locus_indices)} target qubits were provided.")

        try:
            locus = tuple(qubit_names[idx] for idx in locus_indices)
        except IndexError as e:
            raise IndexError(
                "To add new operations in this way, make sure the attribute 'qubits' has enough qubits. "
                "It can also be automatically populated by calling the find_qubits() method if there"
                "already are operations, or set_qubits(n) if the list is empty."
            ) from e

        params = self.table[name].params
        if len(params) != len(args):
            raise TypeError(
                f"Operation {name} has the following arguments: {params}, but {len(args)} values were provided."
            )
        new_op = CircuitOperation(name=name, args=dict(zip(params, args)), implementation=impl_name, locus=locus)
        new_op.validate(self.table)
        self.append(new_op)

    # define method for barrier separately as it is meta and behaves differently
    def barrier(self, *locus_indices) -> None:
        """Add barrier to the circuit"""
        indices = list(locus_indices) if locus_indices else list(np.arange(len(self.qubits), dtype=int))
        self.add_op("barrier", indices)

    def compose(
        self,
        other,
        locus_indices: list[int],
    ) -> Self:
        """A safer way to add circuits together, but will probably take time.

        All the :class:`~iqm.pulse.builder.CircuitOperation` s from the ``'other'`` list are appended to the end of
        this list. The wire ``k`` of the second circuit is connected to wire ``locus_indices[k]`` of the first. This
        is achieved by mapping the locus of each operation in the second circuit onto the qubits of the first.

        For example, if the :attr:`qubits` of the first list are ``['QB1', 'QB2']``, the second list has
        ``['QB3', 'QB4']``, and the locus_indices argument is ``[1,0]``, all the operations in the second list will have
        their ``'QB3'`` mapped to ``'QB2'`` and ``'QB4'`` mapped to ``'QB1'``.

        Args:
            other: Second CircuitOperationList. Must have less or equal qubits than this one.
            locus_indices: Indices of the qubits in this CircuitOperationList onto which the qubits in the second
                circuit ar mapped.

        Returns:
            Self, with new operations added.
        """
        qubit_names1 = self.qubits
        qubit_names2 = other.qubits

        if len(locus_indices) != len(qubit_names2):
            raise IndexError(
                f"There are {len(qubit_names2)} qubits in the second circuit, but provided mapping is"
                f" {locus_indices}. Make sure the length of the mapping is equal to number of qubits."
            )

        new_locus = [qubit_names1[idx] for idx in locus_indices]

        new_circuit = other.map_loci(new_locus)

        self.extend(new_circuit)

        return self

    def count_ops(self) -> Counter:
        """Count each type of operation in the circuit.

        Returns:
            Counter mapping operation names to numbers of times they occur in the circuit.
        """
        return Counter(operation.name for operation in self)

    def map_loci(
        self,
        locus: list[str] | None,
    ) -> CircuitOperationList:
        """Creates a new list of :class:`CircuitOperation` s with locus mapped onto physical qubits.

        Creates a fresh list of fresh :class:`~iqm.pulse.builder.CircuitOperation` s with fresh arguments. If
        ``locus`` is provided, it needs to have the same length as the total number of qubits across the circuit,
        and the qubits will then be mapped onto the new locus. If it is not provided, this is identical to a deepcopy
        of the original list.

        Args:
            locus: List of new qubits to replace the qubits in the loci of the operations in the circuit.

        Returns:
            New CircuitOperationList with loci mapped onto new locus.
        """
        logical_locus = self.qubits
        locus = locus or logical_locus
        if len(locus) != len(set(locus)):
            raise ValueError("Repeated locus elements.")
        if len(logical_locus) != len(locus):
            raise IndexError(
                "The number of qubits in the new locus must be equal to the number of qubits in the old locus."
            )
        mapping = dict(zip(logical_locus, locus))
        new_circuit = CircuitOperationList(qubits=locus, table=self.table)
        for inst in self:
            new_args = inst.args.copy()
            # The classically conditioned operation has a key which specifies which qubit to receive feedback from.
            # This should be correctly mapped.
            # TODO: remove this exception after Pulla/CoCos compilation handles feedback sources in a more regular way
            if "feedback_qubit" in new_args:
                new_args["feedback_qubit"] = mapping[new_args["feedback_qubit"]]
            new_circuit.append(
                CircuitOperation(
                    name=inst.name,
                    locus=tuple(mapping[qb] for qb in inst.locus),
                    args=new_args,
                    implementation=inst.implementation,
                )
            )

        return new_circuit

    def _set_specific_operation_shortcut(self, name: str) -> None:
        """Add the convenience methods for adding new operations, based on the default :class:`QuantumOpTable`."""
        op = self.table[name]
        num_params = len(op.params)
        arity = op.arity

        def _add_specific_op(
            self,
            *args_and_locus,
            impl_name: str | None = None,
        ):
            if len(args_and_locus) != num_params + arity:
                raise TypeError(
                    f"The operation {name} requires {arity} locus/qubit indices and {num_params} additional"
                    f" arguments. A total of {len(args_and_locus)} were provided."
                )
            args = args_and_locus[:num_params]
            locus_indices = [int(idx) for idx in args_and_locus[num_params:]]
            self.add_op(name, locus_indices, *args, impl_name=impl_name)

        _add_specific_op.__doc__ = (
            f"Add a new operation {name}. The first {num_params} arguments are arguments to"
            f" the operation, if any, eg. angle and phase. The last {arity} arguments are indices"
            f" of the qubits the operation acts on. The keyword argument impl_name can be provided"
            f" optionally to fix the implementation of the operation in iqm-pulse."
        )
        setattr(CircuitOperationList, name, _add_specific_op)
