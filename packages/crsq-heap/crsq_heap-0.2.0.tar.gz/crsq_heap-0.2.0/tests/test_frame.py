""" test crsq_heap.heap.Frame
"""

from qiskit.circuit import QuantumCircuit, QuantumRegister
from crsq_heap import heap

class AFrame(heap.Frame):
    """ AFrame """
    def __init__(self, qc: QuantumCircuit):
        super().__init__(qc)
        self.x = QuantumRegister(4, "x")
        self.y = QuantumRegister(2, "y")
        self.a = QuantumRegister(3, "a")
        self.b = QuantumRegister(5, "b")
        self.add_param(self.x, self.y)
        self.add_local(self.a, self.b)

def test_arg_bits_list():
    """ test arg_bits_list """
    qc = QuantumCircuit()
    rb = AFrame(qc)
    bits = rb.param_bits_list()
    assert len(bits) == 6
    assert bits[0] == rb.x[0]
    assert bits[4] == rb.y[0]

def test_local_bit_count():
    """ test local_bit_count """
    qc = QuantumCircuit()
    rb = AFrame(qc)
    temp_bits = rb.allocate_temp_bits(2)
    anc_bits = rb.allocate_ancilla_bits(3, 'anc')
    assert rb.opaque_bit_count == 3+5+2+3
    rb.free_ancilla_bits(anc_bits)
    rb.free_temp_bits(temp_bits)

if __name__ == '__main__':
    test_arg_bits_list()
    test_local_bit_count()
