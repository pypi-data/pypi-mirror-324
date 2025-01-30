import numpy as np
from qiskit import QuantumCircuit, transpile

from qiskit_alice_bob_provider import (
    AliceBobLocalProvider,
    AliceBobRemoteProvider,
)

remote_provider = AliceBobRemoteProvider(
    'YS0yeWFwOnVwZkZwc1pBaG1JdU5sR1ptWTBrVWFKNDIwUHlyaTBa',
    url='http://localhost:8320/external/',
)

local_provider = AliceBobLocalProvider()


def build_bit_flip_circuit(delay_duration_us: float) -> QuantumCircuit:
    circuit = QuantumCircuit(2, 2)
    circuit.initialize('0', 0)
    circuit.initialize('1', 1)
    circuit.cx(0, 1)
    circuit.measure(0, 0)
    circuit.measure(1, 1)
    circuit.draw()
    return circuit


if __name__ == '__main__':
    provider = remote_provider
    backend = provider.get_backend(
        "EMU:40Q:LOGICAL_TARGET", kappa_1=1000, average_nb_photons=8.5
    )

    circ = build_bit_flip_circuit(delay_duration_us=1000)

    trans = transpile(circ, backend)

    job = backend.run(trans, shots=10000, memory=False)
    result = job.result()

    print(backend.target)
    print(result.get_memory())
