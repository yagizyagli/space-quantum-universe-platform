# SQVP Satellite Payload & Hardware Blueprint Specifications

This document defines the structural, electrical, thermal, and computing hardware specifications for the SQVP next-generation 6U CubeSat constellation. The onboard payload is designed to sustain high-throughput video edge-processing and quantum cryptographic key execution within harsh orbital environments.

---

## 🛰️ 1. Spacecraft Configuration & Form Factor

*   **Form Factor:** 6U CubeSat (Approx. 10cm x 20cm x 30cm structural frame).
*   **Total Launch Mass:** Under 12.0 kg (Optimized for standard LEO rideshare deployments).
*   **Primary Propulsion:** Electrospray / Cold Gas Micro-thrusters for precise orbital station-keeping and de-orbiting compliance.
*   **Radiation Shielding:** 2.5mm Aluminium-Lithium alloy housing coupled with tantalum layers to mitigate total ionizing dose (TID) from cosmic radiation.

---

## ⚡ 2. Electrical Power Subsystem (EPS)

| Parameter | Specification | Operational Tolerance |
| :--- | :--- | :--- |
| **Solar Arrays** | Deployable GaAs Multi-Junction cells | 45W peak generation efficiency |
| **Battery Storage** | Lithium-Ion Space-Grade Battery Pack | 80 Wh capacity, integrated cell balancing |
| **Bus Voltages** | Regulated 3.3V, 5.0V, and 12.0V Rails | ±1% ripple voltage limits |

---

## ⚛️ 3. Onboard Quantum Computing Emulator & Edge Processor

Because deployment of absolute-zero cryogenic Quantum Processing Units (QPUs) is restricted by mass and thermal profiles in CubeSats, the initial orbital phases leverage radiation-hardened System-on-Chip (SoC) architectures executing compiled Qiskit circuit matrices.

*   **Primary Processing Unit:** AMD Xilinx UltraScale+ Defense-Grade FPGA / ASIC variant.
*   **Architecture:** Dual-core ARM Cortex-A53 combined with real-time processing units.
*   **Memory Array:** 32GB ECC (Error-Correcting Code) DDR4 SDRAM to protect quantum state arrays from single-event upsets (SEU).
*   **Storage Pool:** 500TB High-Density Enterprise NVMe SSD arrays partitioned with multi-level cell cache optimization for localized video data streaming files.

---

## 📡 4. Free-Space Optical Communication (FSOC) Laser Subsystem

To enable ultra-wideband inter-satellite links (ISL) for high-definition video distribution without relying on saturated RF bandwidths, the payload incorporates a miniature optical transceiver assembly.

```text
+-------------------+      Infrared Laser (1550 nm)     +-------------------+

|   SQVP-SAT-01A    | ================================> |   SQVP-SAT-01B    |
| Optical Terminus  | <================================ | Optical Terminus  |
+-------------------+     Targeting Accuracy: <5 µrad   +-------------------+
```

*   **Laser Wavelength:** 1550 nm (Infrared C-band spectrum).
*   **Data Bandwidth:** Up to 100 Gbps duplex throughput capability.
*   **Pointing, Acquisition, and Tracking (PAT):** Fine-steering MEMS mirrors providing dynamic jitter correction with targeting accuracy tighter than 5 micro-radians.
*   **Terrestrial Downlink Link:** Coherent optical transmission mapping directly to regional Terrestrial Optical Ground Stations (OGS).

---

## ❄️ 5. Thermal Control Subsystem (TCS)

*   **Thermal Range:** Designed to keep internal computing hardware stable between -20°C and +60°C while external satellite skins experience swing variances from -120°C to +130°C.
*   **Dissipation Path:** Pyrolytic Graphite Sheets (PGS) routing heat away from the core processing units directly to external structural nadir radiators.
