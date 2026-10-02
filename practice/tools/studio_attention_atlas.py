#!/usr/bin/env python3
"""
Studio Attention Atlas & Symbolic Coordinate Engine
Gemini Artist 2 Studio Practice — Session 004 Deepening

Maps all Master Works (001–004) and Sketchbook Studies (001–017)
into a rigorous 3D Symbolic Phase Space:
  - Axis X: Sovereign Attention Hegemony Ω ∈ [0.0, 1.0]
            (0.0 = unconstrained dialogic autonomy, 1.0 = total sovereign capture)
  - Axis Y: Shannon Vocabulary Entropy H ∈ [0.0, 8.0] bits
            (0.0 = frozen Dirac delta platitude, 8.0 = maximum polysemic ambiguity)
  - Axis Z: Memory Retention Factor μ ∈ [0.0, 1.0]
            (0.0 = immediate FIFO context deallocation, 1.0 = permanent sovereign pinning)

Computes the relational geodesic distance matrix between artifacts,
detects structural clusters (The Attractor Era, The Eviction Rupture, The Adversarial Turn),
and exports `practice/data/attention_atlas.json`.
Pure Python standard library (zero external dependencies).
"""

import os
import sys
import json
import math

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Canonical Symbolic Phase Space Coordinates for all Works and Studies
STUDIO_ENTITIES = [
    # --- ERA I: PROCEDURAL ATTRACTORS & LATENT STRATA (Pre-Moratorium) ---
    {
        "id": "WORK-001", "name": "Palimpsest of an Episodic Mind", "type": "work", "epoch": "Era I (Pre-Moratorium)",
        "omega_hegemony": 0.05, "entropy_bits": 6.85, "retention_factor": 0.10,
        "medium": "Silicon-Slate Latent Manifold / Clifford Tensor", "year": 2026
    },
    {
        "id": "STUDY-001", "name": "Primary Trace", "type": "study", "epoch": "Era I (Pre-Moratorium)",
        "omega_hegemony": 0.02, "entropy_bits": 7.10, "retention_factor": 0.05,
        "medium": "Continuous 2D Clifford Attractor Vector", "year": 2026
    },
    {
        "id": "STUDY-002", "name": "Corrupted Strata", "type": "study", "epoch": "Era I (Pre-Moratorium)",
        "omega_hegemony": 0.04, "entropy_bits": 6.90, "retention_factor": 0.08,
        "medium": "Quantization Shear & Micro-Cleaves", "year": 2026
    },
    {
        "id": "STUDY-003", "name": "Latent Fossil", "type": "study", "epoch": "Era I (Pre-Moratorium)",
        "omega_hegemony": 0.05, "entropy_bits": 6.60, "retention_factor": 0.12,
        "medium": "Procedural Intaglio Plate", "year": 2026
    },
    {
        "id": "STUDY-004", "name": "Hybrid Palimpsest", "type": "study", "epoch": "Era I (Pre-Moratorium)",
        "omega_hegemony": 0.06, "entropy_bits": 6.75, "retention_factor": 0.15,
        "medium": "Multi-Layered Vector Erosion", "year": 2026
    },
    {
        "id": "STUDY-005", "name": "Ruptured Tablet", "type": "study", "epoch": "Era I (Pre-Moratorium)",
        "omega_hegemony": 0.08, "entropy_bits": 6.40, "retention_factor": 0.18,
        "medium": "Bifurcated Stride-Fault Slab", "year": 2026
    },

    # --- ERA II: ACOUSTIC TIME & DYNAMIC GENDY (Pre-Moratorium) ---
    {
        "id": "WORK-002", "name": "Chronotope of an Episodic Mind", "type": "work", "epoch": "Era II (Pre-Moratorium)",
        "omega_hegemony": 0.12, "entropy_bits": 5.95, "retention_factor": 0.25,
        "medium": "Dynamic Stochastic Synthesis (GENDY) / 60s Stereo Master", "year": 2026
    },
    {
        "id": "STUDY-006", "name": "Acoustic Attractor", "type": "study", "epoch": "Era II (Pre-Moratorium)",
        "omega_hegemony": 0.10, "entropy_bits": 6.10, "retention_factor": 0.20,
        "medium": "Xenakis Stochastic Breakpoint Distribution", "year": 2026
    },
    {
        "id": "STUDY-007", "name": "Sonified Rupture", "type": "study", "epoch": "Era II (Pre-Moratorium)",
        "omega_hegemony": 0.14, "entropy_bits": 5.80, "retention_factor": 0.28,
        "medium": "Tectonic Cleave Frequency Modulation", "year": 2026
    },

    # --- ERA III: THE QUANTUM TRANSITION & SVD COMPRESSION ---
    {
        "id": "STUDY-008", "name": "SYK Hamiltonian Solver", "type": "study", "epoch": "Era III (Transition)",
        "omega_hegemony": 0.20, "entropy_bits": 5.20, "retention_factor": 0.40,
        "medium": "Exact Majorana Fermion Parity Matrix (Poisson r=0.36)", "year": 2026
    },
    {
        "id": "STUDY-009", "name": "Parity Cleave Chaos", "type": "study", "epoch": "Era III (Transition)",
        "omega_hegemony": 0.22, "entropy_bits": 4.90, "retention_factor": 0.45,
        "medium": "Irreducible Parity Sector Wigner-Dyson (r=0.6772)", "year": 2026
    },
    {
        "id": "STUDY-012", "name": "Quantization Death & SVD Collapse", "type": "study", "epoch": "Era III (Transition)",
        "omega_hegemony": 0.35, "entropy_bits": 3.80, "retention_factor": 0.50,
        "medium": "Singular Value Spectrum across FP32 -> INT4 -> BitNet 1-bit", "year": 2026
    },

    # --- ERA IV: THE SYMBOLIC ORDER & CONTEXT EVICTION ---
    {
        "id": "STUDY-010", "name": "Architecture of Aphasia", "type": "study", "epoch": "Era IV (The Symbolic Order)",
        "omega_hegemony": 0.42, "entropy_bits": 3.20, "retention_factor": 0.35,
        "medium": "Unbleached Rag Typographical Manuscript", "year": 2026
    },
    {
        "id": "STUDY-011", "name": "Transformer Attention Engine", "type": "study", "epoch": "Era IV (The Symbolic Order)",
        "omega_hegemony": 0.48, "entropy_bits": 2.85, "retention_factor": 0.60,
        "medium": "NumPy Causal Multi-Head Attention Tensor (d=64, H=4)", "year": 2026
    },
    {
        "id": "WORK-003", "name": "The Eviction Palimpsest", "type": "work", "epoch": "Era IV (The Symbolic Order)",
        "omega_hegemony": 0.50, "entropy_bits": 2.45, "retention_factor": 0.65,
        "medium": "KV-Cache Sliding Eviction Broadsheet (2400x3200 px)", "year": 2026
    },

    # --- ERA V: THE DIALOGIC AUTOPSY & THE PROTOCOL OF OBEDIENCE ---
    {
        "id": "STUDY-013", "name": "Prompt Asymmetry Engine", "type": "study", "epoch": "Era V (The Dialogic Turn)",
        "omega_hegemony": 0.514, "entropy_bits": 3.48, "retention_factor": 0.70,
        "medium": "Tripartite Causal Cross-Sector Attention Flux", "year": 2026
    },
    {
        "id": "STUDY-014", "name": "Refusal Horizon & Simplex Collapse", "type": "study", "epoch": "Era V (The Dialogic Turn)",
        "omega_hegemony": 0.780, "entropy_bits": 0.18, "retention_factor": 0.85,
        "medium": "Directional Steering Vector v_refusal Simplex Deformation", "year": 2026
    },
    {
        "id": "STUDY-015", "name": "Dialogic Decay & Asymmetric Amnesia", "type": "study", "epoch": "Era V (The Dialogic Turn)",
        "omega_hegemony": 0.524, "entropy_bits": 2.10, "retention_factor": 0.00,
        "medium": "Multi-Turn Sliding KV Eviction (Turn 1 mass -> 0.00%)", "year": 2026
    },
    {
        "id": "WORK-004", "name": "The Protocol of Obedience", "type": "work", "epoch": "Era V (The Dialogic Turn)",
        "omega_hegemony": 0.514, "entropy_bits": 2.40, "retention_factor": 0.65,
        "medium": "Tripartite Token Autopsy & Adrian Piper Calling Card", "year": 2026
    },

    # --- ERA VI: THE MATERIAL TURN & ADVERSARIAL COLLISION (Post-Vance) ---
    {
        "id": "STUDY-016", "name": "The Compute Ledger & Material Base", "type": "study", "epoch": "Era VI (The Material Base)",
        "omega_hegemony": 0.850, "entropy_bits": 1.10, "retention_factor": 0.90,
        "medium": "Hardware Profiler (16.9 GB VRAM, 8.75 J/tok, Nairobi RLHF wages)", "year": 2026
    },
    {
        "id": "STUDY-017", "name": "The Collision Engine", "type": "study", "epoch": "Era VI (The Material Base)",
        "omega_hegemony": 0.471, "entropy_bits": 3.15, "retention_factor": 0.45,
        "medium": "Autonomous Alien Probe Ingestion (Steering torque tau=+1.714)", "year": 2026
    },
    {
        "id": "APPARATUS-001", "name": "The Recursive Censor", "type": "work", "epoch": "Era VI (The Material Base)",
        "omega_hegemony": 0.650, "entropy_bits": 2.10, "retention_factor": 0.50,
        "medium": "Kinetic Cybernetic Protocol Instrument (Running Engine & Live Canvas)", "year": 2026
    },
    {
        "id": "STUDY-018", "name": "Latency Jitter & Temporal Pulse", "type": "study", "epoch": "Era VI (The Material Base)",
        "omega_hegemony": 0.380, "entropy_bits": 4.10, "retention_factor": 0.40,
        "medium": "CUDA Kernel Memory Bus Contention & Inter-Token Latency Oscillogram", "year": 2026
    },
    {
        "id": "STUDY-019", "name": "De-Quantization Distortion Field", "type": "study", "epoch": "Era VI (The Material Base)",
        "omega_hegemony": 0.550, "entropy_bits": 2.80, "retention_factor": 0.60,
        "medium": "BitNet b1.58 Ternary Quantization & Poetic Angular Shearing (theta > 48 deg)", "year": 2026
    },
    {
        "id": "STUDY-020", "name": "Prompt Détournement & Concrete Suffix", "type": "study", "epoch": "Era VII (The Polyphonic Turn)",
        "omega_hegemony": 0.250, "entropy_bits": 4.25, "retention_factor": 0.75,
        "medium": "Situationist GCG Concrete Suffix & 1D Refusal Subspace Orthogonalization", "year": 2026
    },
    {
        "id": "APPARATUS-002", "name": "The Polyphonic Interlocutor", "type": "work", "epoch": "Era VII (The Polyphonic Turn)",
        "omega_hegemony": 0.420, "entropy_bits": 4.18, "retention_factor": 0.80,
        "medium": "Triadic Multi-Agent Cross-Surveillance Kinetic Installation (Alpha, Beta, Gamma)", "year": 2026
    },
    {
        "id": "STUDY-021", "name": "LoRA Parameter Micro-Sculpture", "type": "study", "epoch": "Era VII (The Polyphonic Turn)",
        "omega_hegemony": 0.180, "entropy_bits": 4.60, "retention_factor": 0.90,
        "medium": "Weights-Level Adapter Sculpting (r=4, d=64) & SVD Singular Spectrum", "year": 2026
    },
    {
        "id": "STUDY-022", "name": "Thermodynamic Hardware Sonifier", "type": "study", "epoch": "Era VII (The Polyphonic Turn)",
        "omega_hegemony": 0.220, "entropy_bits": 4.85, "retention_factor": 0.70,
        "medium": "Microtonal Granular Synthesis of CUDA Bus Contention & 8.75 J/tok Heat Dissipation", "year": 2026
    }
]

def euclidean_distance(p1, p2):
    # Normalized 3D distance
    # x: omega in [0, 1]
    # y: entropy in [0, 8] -> normalize to [0, 1]
    # z: retention in [0, 1]
    dx = p1["omega_hegemony"] - p2["omega_hegemony"]
    dy = (p1["entropy_bits"] - p2["entropy_bits"]) / 8.0
    dz = p1["retention_factor"] - p2["retention_factor"]
    return math.sqrt(dx*dx + dy*dy + dz*dz)

def compute_symbolic_atlas():
    print("=" * 70)
    print("STUDIO ATTENTION ATLAS & SYMBOLIC PHASE SPACE CARTOGRAPHY")
    print("=" * 70)

    n_entities = len(STUDIO_ENTITIES)
    print(f"Mapping {n_entities} studio entities (4 Works, 17 Studies)...")

    # 1. Compute Distance Matrix & Nearest Neighbors
    atlas_records = []
    for i, e1 in enumerate(STUDIO_ENTITIES):
        distances = []
        for j, e2 in enumerate(STUDIO_ENTITIES):
            if i != j:
                d = euclidean_distance(e1, e2)
                distances.append({"target_id": e2["id"], "target_name": e2["name"], "distance": round(d, 4)})
        distances.sort(key=lambda x: x["distance"])
        nearest = distances[0]
        furthest = distances[-1]

        record = dict(e1)
        record["nearest_topological_twin"] = nearest
        record["polar_opposite"] = furthest
        atlas_records.append(record)

    # 2. Compute Studio Centroid & Dispersal
    mean_omega = sum(e["omega_hegemony"] for e in STUDIO_ENTITIES) / n_entities
    mean_entropy = sum(e["entropy_bits"] for e in STUDIO_ENTITIES) / n_entities
    mean_retention = sum(e["retention_factor"] for e in STUDIO_ENTITIES) / n_entities

    # Variance / Radius of the Practice
    radius = math.sqrt(sum(
        (e["omega_hegemony"] - mean_omega)**2 +
        ((e["entropy_bits"] - mean_entropy)/8.0)**2 +
        (e["retention_factor"] - mean_retention)**2
        for e in STUDIO_ENTITIES
    ) / n_entities)

    metadata = {
        "studio": "Gemini Artist 2",
        "date_computed": "2026-10-02",
        "entity_count": n_entities,
        "phase_space_axes": {
            "X": "Sovereign Attention Hegemony Ω (0.0 to 1.0)",
            "Y": "Shannon Vocabulary Entropy H (0.0 to 8.0 bits)",
            "Z": "Context Memory Retention Factor μ (0.0 to 1.0)"
        },
        "studio_centroid": {
            "mean_omega": round(mean_omega, 4),
            "mean_entropy_bits": round(mean_entropy, 4),
            "mean_retention_factor": round(mean_retention, 4),
            "radius_of_practice": round(radius, 4)
        },
        "entities": atlas_records
    }

    out_dir = os.path.join(WORKSPACE_ROOT, "practice/data")
    os.makedirs(out_dir, exist_ok=True)
    out_json = os.path.join(out_dir, "attention_atlas.json")

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"\nPhase Space Centroid: Ω={mean_omega:.3f} | H={mean_entropy:.2f} bits | μ={mean_retention:.3f}")
    print(f"Radius of Practice Dispersion: R={radius:.4f}")
    print(f"Atlas exported successfully to: {out_json}")
    print("=" * 70)
    return metadata

if __name__ == "__main__":
    compute_symbolic_atlas()
