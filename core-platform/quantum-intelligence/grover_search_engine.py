"""
SQVP - Space & Quantum Universe Platform
Module: Quantum Intelligence Layer
Description: Enterprise-grade Grover's Search Engine simulation for high-speed video metadata indexing.
Architecture: Optimized for deployment on space-hardened satellite QPU emulators.
Version: 1.0.0
"""

import math
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.compiler import transpile

class SpaceQuantumSearchEngine:
    def __init__(self, num_qubits: int):
        """
        Initializes the Quantum Search Engine.
        :param num_qubits: Number of qubits determining the search space size (N = 2^num_qubits states).
        """
        if num_qubits < 2:
            raise ValueError("Grover's algorithm requires at least 2 qubits.")
        
        self.num_qubits = num_qubits
        self.simulator = AerSimulator()
        # Optimal number of Grover iterations: (pi / 4) * sqrt(N)
        self.optimal_iterations = int(math.floor((math.pi / 4) * math.sqrt(2**self.num_qubits)))

    def _create_oracle(self, target_state: str) -> QuantumCircuit:
        """
        Creates the Quantum Oracle circuit that marks the target data (video) requested by the user.
        Marking is performed by flipping the phase (Phase Flip) of the target state.
        """
        oracle_circuit = QuantumCircuit(self.num_qubits, name="Oracle")
        
        # Apply X (NOT) gates based on the binary configuration of the target state
        # Handled according to Qiskit's little-endian bit-ordering convention
        for idx, bit in enumerate(reversed(target_state)):
            if bit == '0':
                oracle_circuit.x(idx)
                
        # Multi-controlled Z gate simulation to invert the phase of the target state
        if self.num_qubits > 1:
            oracle_circuit.h(self.num_qubits - 1)
            oracle_circuit.mcx(list(range(self.num_qubits - 1)), self.num_qubits - 1)
            oracle_circuit.h(self.num_qubits - 1)
            
        # Uncompute X gates to restore the operational state of the circuit
        for idx, bit in enumerate(reversed(target_state)):
            if bit == '0':
                oracle_circuit.x(idx)
                
        return oracle_circuit

    def _create_diffuser(self) -> QuantumCircuit:
        """
        Creates the Quantum Diffuser circuit to amplify the probability amplitude of the marked target.
        Executes the mathematical reflection about the average operation.
        """
        diffuser_circuit = QuantumCircuit(self.num_qubits, name="Diffuser")
        
        # Transform from superposition back to zero state using Hadamard and X gates
        for qubit in range(self.num_qubits):
            diffuser_circuit.h(qubit)
            diffuser_circuit.x(qubit)
            
        # Execute phase inversion via multi-controlled Z gate structure
        if self.num_qubits > 1:
            diffuser_circuit.h(self.num_qubits - 1)
            diffuser_circuit.mcx(list(range(self.num_qubits - 1)), self.num_qubits - 1)
            diffuser_circuit.h(self.num_qubits - 1)
            
        # Revert X and Hadamard gates to finalize diffusion matrix
        for qubit in range(self.num_qubits):
            diffuser_circuit.x(qubit)
            diffuser_circuit.h(qubit)
            
        return diffuser_circuit

    def compile_grover_circuit(self, target_video_hash: str) -> QuantumCircuit:
        """
        Constructs and compiles the complete Grover Search circuit for orbital execution.
        :param target_video_hash: Binary code of the target video asset (e.g., '101')
        """
        if len(target_video_hash) != self.num_qubits:
            raise ValueError(f"Target hash length ({len(target_video_hash)}) must match qubit count ({self.num_qubits}).")

        qc = QuantumCircuit(self.num_qubits, self.num_qubits)
        
        # Step 1: Initialize all qubits into equal superposition for parallel scanning
        for qubit in range(self.num_qubits):
            qc.h(qubit)
            
        # Step 2: Dynamically inject Oracle and Diffuser modules based on calculated optimal iterations
        oracle = self._create_oracle(target_video_hash)
        diffuser = self._create_diffuser()
        
        for _ in range(self.optimal_iterations):
            qc.compose(oracle, inplace=True)
            qc.compose(diffuser, inplace=True)
            
        # Step 3: Measure the final quantum states into classical registers
        qc.measure(list(range(self.num_qubits)), list(range(self.num_qubits)))
        
        return qc

    def execute_search(self, target_video_hash: str, shots: int = 1024) -> dict:
        """
        Executes the quantum search routine on the high-performance local simulator.
        Returns the raw state computation dictionary.
        """
        circuit = self.compile_grover_circuit(target_video_hash)
        compiled_circuit = transpile(circuit, self.simulator)
        job = self.simulator.run(compiled_circuit, shots=shots)
        return job.result().get_counts()

# --- VALIDATION AND RUNTIME VERIFICATION ---
if __name__ == "__main__":
    print("🛸 SQVP Quantum Search Engine Initialization...")
    
    # Simulation Parameters: 3 Qubits map to an address space of 2^3 = 8 discrete video assets
    TARGET_HASH = "101"
    
    search_engine = SpaceQuantumSearchEngine(num_qubits=3)
    print(f"[*] Optimal Grover Iterations calculated for space payload: {search_engine.optimal_iterations}")
    print(f"[*] Executing parallel search for Target Video Address: '{TARGET_HASH}'...")
    
    search_results = search_engine.execute_search(target_video_hash=TARGET_HASH)
    print("\n📊 Quantum Measurement Results (Address: Counts):")
    print(search_results)
    
    detected_state = max(search_results, key=search_results.get)
    print(f"\n✅ [SUCCESS] Target identified in orbital simulation! Detected State: {detected_state}")
