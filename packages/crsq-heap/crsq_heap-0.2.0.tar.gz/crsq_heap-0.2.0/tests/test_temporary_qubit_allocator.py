""" Tests for crsq_heap.heap.TemporaryQubitAllocator """

from qiskit import QuantumCircuit
from crsq_heap import heap

def test_allocate_first():
    """ allocate for the first time"""
    qc = QuantumCircuit()
    allocator = heap.TemporaryQubitAllocator("abc", qc)
    assert allocator.size == 0
    bits = allocator.allocate(3, 'c')
    assert len(bits) == 3
    assert allocator.size == 3

def test_free():
    """ allocate, then free """
    qc = QuantumCircuit()
    allocator = heap.TemporaryQubitAllocator("abc", qc)
    bits = allocator.allocate(3, 'c')
    allocator.free(bits)
    assert len(allocator.free_qubits) == 3

def test_allocate_reuse():
    """ allocate, free, then allocate again """
    qc = QuantumCircuit()
    allocator = heap.TemporaryQubitAllocator("abc", qc)
    bits = allocator.allocate(3, 'c')
    allocator.free(bits)
    bits2 = allocator.allocate(3, 'c')
    assert len(bits2) == 3
    assert len(allocator.free_qubits) == 0

def test_size():
    """ the size method"""
    qc = QuantumCircuit()
    allocator = heap.TemporaryQubitAllocator("abc", qc)
    bits1 = allocator.allocate(3, 'c')
    bits2 = allocator.allocate(5, 'c')
    assert allocator.size == 8
    allocator.free(bits2)
    allocator.free(bits1)
    assert allocator.size == 8


if __name__ == '__main__':
    test_allocate_first()
    test_free()
    test_allocate_reuse()
    test_size()
