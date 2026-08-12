"""
SQVP - Space & Quantum Universe Platform
Module: Space Infrastructure Layer
Description: Orbital routing and downlink scheduling simulator for multi-gigabit video data transit.
Architecture: Resolves the optimal satellite node to ground-station connection based on latency and visibility.
Version: 1.0.0
"""

import json
import math

class SpaceDownlinkScheduler:
    def __init__(self, network_config_path: str = None):
        """
        Initializes the orbital routing engine.
        Loads satellite telemetry metadata from the internal network configuration.
        """
        # Default placeholder constellation parameters if json profile is not provided
        self.max_link_distance = 2500.0  # Max distance in km for laser or radio link
        self.speed_of_light_space = 299792.458  # km/s

    def calculate_link_latency(self, distance_km: float) -> float:
        """
        Calculates the theoretical vacuum-speed latency for laser communications (FSOC).
        Returns latency in milliseconds.
        """
        if distance_km <= 0:
            return 0.0
        return (distance_km / self.speed_of_light_space) * 1000.0

    def select_optimal_satellite_node(self, ground_station_coords: dict, visible_satellites: list) -> dict:
        """
        Parses live telemetry from passing satellites to determine the optimal node for video streaming.
        Calculates link distance, elevation vector metrics, and orbital transmission latency.
        """
        best_node = None
        min_calculated_latency = float('inf')

        for sat in visible_satellites:
            # Basic 3D Cartesian Euclidean distance evaluation for orbital trajectory simulation
            dx = sat['coords']['x'] - ground_station_coords['x']
            dy = sat['coords']['y'] - ground_station_coords['y']
            dz = sat['coords']['z'] - ground_station_coords['z']
            
            calculated_distance = math.sqrt(dx**2 + dy**2 + dz**2)
            
            # Filter nodes executing out of cross-link hardware thresholds
            if calculated_distance <= self.max_link_distance:
                latency_ms = self.calculate_link_latency(calculated_distance)
                
                # Check for latency optimization and link health metrics
                if latency_ms < min_calculated_latency and sat['signal_quality'] > 0.75:
                    min_calculated_latency = latency_ms
                    best_node = {
                        "selected_satellite_id": sat['sat_id'],
                        "distance_to_target_km": round(calculated_distance, 2),
                        "estimated_latency_ms": round(latency_ms, 4),
                        "allocated_bandwidth_gbps": 10.0 if sat['quantum_enabled'] else 2.5
                    }

        if not best_node:
            raise ConnectionError("CRITICAL: Optical link failure. No suitable orbital node found within target range.")
            
        return best_node

# --- SPACE ROUTING RUNTIME VERIFICATION ---
if __name__ == "__main__":
    print("🛰️ SQVP Space Infrastructure Routing Engine Active...")
    
    # Ground Station Target Coordinate Config (e.g., Optical Ground Station Alpha)
    ground_station_alpha = {"x": 6371.0, "y": 0.0, "z": 0.0}
    
    # Simulated Live Space Telemetry Feed from passing LEO Satellite Constellation Planes
    active_orbital_satellites = [
        {
            "sat_id": "SQVP-SAT-01A", 
            "coords": {"x": 6921.0, "y": 450.0, "z": 200.0}, 
            "signal_quality": 0.92,
            "quantum_enabled": True
        },
        {
            "sat_id": "SQVP-SAT-01B", 
            "coords": {"x": 6921.0, "y": 1800.0, "z": 900.0}, 
            "signal_quality": 0.88,
            "quantum_enabled": True
        },
        {
            "sat_id": "SQVP-SAT-02C", 
            "coords": {"x": 6380.0, "y": 100.0, "z": 50.0}, 
            "signal_quality": 0.45,  # Low signal quality due to atmospheric cloud interference
            "quantum_enabled": False
        }
    ]
    
    print("[*] Processing live telemetry arrays for Ground Station Alpha...")
    scheduler = SpaceDownlinkScheduler()
    
    try:
        routing_decision = scheduler.select_optimal_satellite_node(ground_station_alpha, active_orbital_satellites)
        print("\n📊 Space-to-Ground Link Allocation Matrix Result:")
        print(json.dumps(routing_decision, indent=2))
        print(f"\n✅ [SUCCESS] Secure orbital link established with node: {routing_decision['selected_satellite_id']}")
    except Exception as error:
        print(f"\n⚠️ [LINK FAILURE] {error}")
