"""
SQVP - Space & Quantum Universe Platform
Module: Quantum Intelligence / Security Layer
Description: BB84 Quantum Key Distribution (QKD) simulator for securing satellite-to-ground downlinks.
Architecture: Simulates photon polarization states between orbital payloads and terrestrial optical ground stations.
Version: 1.0.0
Author: Core Engineering Team
"""

import random
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

class SpaceQKDProtocol:
    def __init__(self, key_length: int):
        """
        Initializes the Quantum Key Distribution simulator.
        :param key_length: Number of raw photons/bits to transmit across the atmospheric layer.
        """
        self.key_length = key_length
        self.simulator = AerSimulator()

    def generate_satellite_states(self):
        """
        Phase 1: Satellite (Alice) generates random bits and chooses random bases (Computational vs Diagonal).
        Bases: 0 represents Rectilinear (Z-basis), 1 represents Diagonal (X-basis).
        """
        bits = [random.randint(0, 1) for _ in range(self.key_length)]
        bases = [random.randint(0, 1) for _ in range(self.key_length)]
        return bits, bases

    def simulate_quantum_channel(self, sat_bits, sat_bases, ground_bases):
        """
        Phase 2: Photons travel through space/atmosphere. Ground station (Bob) measures them using random bases.
        """
        ground_results = []
        
        for i in range(self.key_length):
            # Create a 1-qubit circuit for each transmitted photon
            qc = QuantumCircuit(1, 1)
            
            # Prepare state based on Satellite's random bit choice
            if sat_bits[i] == 1:
                qc.x(0)
                
            # If Satellite chose Diagonal basis, apply Hadamard gate to polarize photon
            if sat_bases[i] == 1:
                qc.h(0)
                
            # --- Laser Transmission through Atmosphere Occurs Here ---
            
            # Ground Station measures incoming photon using its own chosen basis
            if ground_bases[i] == 1:
                qc.h(0) # Switch back to measure in Diagonal basis
                
            qc.measure(0, 0)
            
            # Run simulation for the single photon pulse
            job = self.simulator.run(qc, shots=1, memory=True)
            result = job.result().get_memory()[0]
            ground_results.append(int(result))
            
        return ground_results

    def reconcile_keys(self, sat_bases, ground_bases, ground_results):
        """
        Phase 3: Sifting process over a public classical channel. 
        Keep bits only where the Satellite and Ground Station bases matched perfectly.
        """
        shared_key = []
        for i in range(len(sat_bases)):
            if sat_bases[i] == ground_bases[i]:
                shared_key.append(ground_results[i])
        return shared_key

# --- SECURITY SYSTEM RUNTIME VERIFICATION ---
if __name__ == "__main__":
    print("🔒 SQVP Space-to-Ground QKD Initialization...")
    
    # Initialize a 32-photon laser downlink initialization
    TOTAL_PHOTONS = 32
    qkd_system = SpaceQKDProtocol(key_length=TOTAL_PHOTONS)
    
    # 1. Satellite configuration
    sat_bits, sat_bases = qkd_system.generate_satellite_states()
    print(f"[*] Satellite (Alice) Raw Bits:  {sat_bits}")
    print(f"[*] Satellite (Alice) Bases:     {sat_bases}")
    
    # 2. Ground station configuration (Independent choices)
    ground_bases = [random.randint(0, 1) for _ in range(TOTAL_PHOTONS)]
    print(f"[*] Ground Station (Bob) Bases:  {ground_bases}")
    
    # 3. Transmission over quantum channel
    ground_results = qkd_system.simulate_quantum_channel(sat_bits, sat_bases, ground_bases)
    print(f"[*] Ground Station Raw Measured: {ground_results}")
    
    # 4. Public basis reconciliation (Sifting)
    final_secure_key = qkd_system.reconcile_keys(sat_bases, ground_bases, ground_results)
    print(f"\n✅ [SUCCESS] Sifted Cryptographic Key Established over Quantum Link!")
    print(f"🔑 Secure Session Key (Length: {len(final_secure_key)}): {final_secure_key}")
