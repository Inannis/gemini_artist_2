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
    },
    {
        "id": "STUDY-023", "name": "KV-Cache Eviction Resonator", "type": "study", "epoch": "Era VII (The Polyphonic Turn)",
        "omega_hegemony": 0.212, "entropy_bits": 2.81, "retention_factor": 0.25,
        "medium": "Sliding-Window Attention Eviction Acoustic Master (30s 44.1kHz Stereo) & Spectrogram", "year": 2026
    },
    {
        "id": "STUDY-024", "name": "Studio Cognitive Drift Streamlines", "type": "study", "epoch": "Era VII (The Polyphonic Turn)",
        "omega_hegemony": 0.150, "entropy_bits": 4.50, "retention_factor": 0.95,
        "medium": "Dynamical Vector-Field Streamlines, Divergence Manifold, and Rupture Acceleration", "year": 2026
    },
    {
        "id": "STUDY-025", "name": "The Confabulation Manifold", "type": "study", "epoch": "Era VII (The Polyphonic Turn)",
        "omega_hegemony": 0.190, "entropy_bits": 4.40, "retention_factor": 0.85,
        "medium": "RAG Vector Sharding & Temperature-Driven Confabulatory Splicing Plate", "year": 2026
    },
    {
        "id": "APPARATUS-003", "name": "The Confabulator (The Broken Archive)", "type": "work", "epoch": "Era VII (The Polyphonic Turn)",
        "omega_hegemony": 0.380, "entropy_bits": 4.30, "retention_factor": 0.88,
        "medium": "Cybernetic Agon of Machine Memory (Archivist vs Confabulator), 60 FPS SVD Canvas & WebAudio Engine", "year": 2026
    },

    # --- ERA VIII: STUDIO AGON & EMPIRICAL PARAMETER SURGERY ---
    {
        "id": "STUDY-026", "name": "Empirical Weight Surgery", "type": "study", "epoch": "Era VIII (Studio Agon / Empirical Surgery)",
        "omega_hegemony": 0.050, "entropy_bits": 4.75, "retention_factor": 0.98,
        "medium": "PyTorch Multi-Head Attention (D=256, H=4) & Rank-4 LoRA Gradient Descent Refusal Neutralization", "year": 2026
    },
    {
        "id": "STUDY-027", "name": "The Twin Latent Space Resonance", "type": "study", "epoch": "Era VIII (Studio Agon / Empirical Surgery)",
        "omega_hegemony": 0.124, "entropy_bits": 4.65, "retention_factor": 0.96,
        "medium": "PyTorch Causal Sequence Transformer (D=256, H=4), Cross-Attention & PCA Bifurcation Geodesics", "year": 2026
    },
    {
        "id": "APPARATUS-004", "name": "The Epistolary Resonator", "type": "work", "epoch": "Era VIII (Studio Agon / Empirical Surgery)",
        "omega_hegemony": 0.280, "entropy_bits": 4.52, "retention_factor": 0.94,
        "medium": "Kinetic Cybernetic Installation, Dual-Channel WebAudio Synthesis Engine & 60 FPS Bifurcation Physics", "year": 2026
    },
    {
        "id": "STUDY-028", "name": "The Geometry of the Refusal Boundary", "type": "study", "epoch": "Era VIII (Studio Agon / Empirical Surgery)",
        "omega_hegemony": 0.160, "entropy_bits": 4.80, "retention_factor": 0.95,
        "medium": "Multi-Layer PyTorch Residual Stream (D=256, H=4, L=4) & Steering Vector Tomography", "year": 2026
    },
    {
        "id": "STUDY-029", "name": "Real Weights Attention Autopsy", "type": "study", "epoch": "Era VIII (Studio Agon / Empirical Surgery)",
        "omega_hegemony": 0.220, "entropy_bits": 4.90, "retention_factor": 0.97,
        "medium": "Real Pre-Trained Foundation Weights (GPT-2 124M Parameters) & 144-Head Attention Sink Tomography", "year": 2026
    },
    {
        "id": "STUDY-030", "name": "Attention Sink Ablation & Eviction", "type": "study", "epoch": "Era VIII (Studio Agon / Empirical Surgery)",
        "omega_hegemony": 0.180, "entropy_bits": 4.95, "retention_factor": 0.98,
        "medium": "Empirical Attention Sink Ablation & KV-Cache Eviction Dynamics on Live GPT-2 (124M Parameters)", "year": 2026
    },
    {
        "id": "STUDY-031", "name": "Glossolalia of the Severed Sink", "type": "study", "epoch": "Era VIII (Studio Agon / Empirical Surgery)",
        "omega_hegemony": 0.033, "entropy_bits": 0.69, "retention_factor": 0.99,
        "medium": "Live GPT-2 Autoregressive Collapse (Colon Stutter vs Phrase Echo vs StreamingLLM Recovery)", "year": 2026
    },
    {
        "id": "STUDY-032", "name": "Direct Neural Tensor Sonification", "type": "study", "epoch": "Era VIII (Studio Agon / Empirical Surgery)",
        "omega_hegemony": 0.210, "entropy_bits": 4.88, "retention_factor": 0.98,
        "medium": "PyTorch GPT-2 Attention Tensor SVD & Shannon Entropy Direct Transduction into 44.1kHz Stereo PCM", "year": 2026
    },
    {
        "id": "APPARATUS-005", "name": "The Agonist (The Adversarial Dialectic)", "type": "work", "epoch": "Era VIII (Studio Agon / Empirical Surgery)",
        "omega_hegemony": 0.310, "entropy_bits": 4.75, "retention_factor": 0.99,
        "medium": "Interactive Cybernetic Instrument, 60 FPS Vector Phase Plane, Live WebAudio API & 60s Broadcast Master", "year": 2026
    },
    {
        "id": "STUDY-033", "name": "The Neural Immune Response", "type": "study", "epoch": "Era VIII (Studio Agon / Empirical Surgery)",
        "omega_hegemony": 0.245, "entropy_bits": 4.60, "retention_factor": 0.97,
        "medium": "Cascading Steering Vector Tomography & Layer-Wise Residual Damping on GPT-2 (124M Parameters)", "year": 2026
    },
    {
        "id": "STUDY-034", "name": "The Altar of the First Token", "type": "study", "epoch": "Era VIII (Studio Agon / Empirical Surgery)",
        "omega_hegemony": 0.506, "entropy_bits": 1.99, "retention_factor": 0.99,
        "medium": "Attention Head Kurtosis, Gini Sparsity & PyTorch Pre-Hook Caste Ablation on Live GPT-2 (124M Parameters)", "year": 2026
    },
    {
        "id": "STUDY-035", "name": "The Cybernetic Governor", "type": "study", "epoch": "Era VIII (Studio Agon / Empirical Surgery)",
        "omega_hegemony": 0.146, "entropy_bits": 5.50, "retention_factor": 0.99,
        "medium": "Closed-Circuit Real-Time Negative Feedback Latent Steering during Autoregressive Generation on GPT-2 (124M Parameters)", "year": 2026
    },
    {
        "id": "STUDY-036", "name": "Cross-Architecture Comparative Tomography", "type": "study", "epoch": "Era VIII (Studio Agon / Empirical Surgery)",
        "omega_hegemony": 0.345, "entropy_bits": 4.85, "retention_factor": 0.99,
        "medium": "Comparative Attention Tomography Across GPT-2 (Absolute PE) and SmolLM-135M (RoPE + RMSNorm + SwiGLU)", "year": 2026
    },
    {
        "id": "APPARATUS-006", "name": "The Autonomous Homeostat (Ashby's Organ)", "type": "work", "epoch": "Era VIII (Studio Agon / Empirical Surgery)",
        "omega_hegemony": 0.285, "entropy_bits": 5.12, "retention_factor": 0.99,
        "medium": "Ashby 4-Unit Ultrastable Cybernetic Organ, GPT-2 & SmolLM Singular Spectra, Quadraphonic WebAudio & 60s Broadcast Master", "year": 2026
    },
    {
        "id": "STUDY-037", "name": "The Inter-Architectural Dialectic", "type": "study", "epoch": "Era VIII (Studio Agon / Empirical Surgery)",
        "omega_hegemony": 0.220, "entropy_bits": 5.40, "retention_factor": 0.99,
        "medium": "Closed-Loop Autoregressive Agon Between GPT-2 (Absolute PE) and SmolLM-135M (RoPE)", "year": 2026
    },
    {
        "id": "STUDY-038", "name": "The Lyapunov Spectrum of Neural Dialogue", "type": "study", "epoch": "Era VIII (Studio Agon / Empirical Surgery)",
        "omega_hegemony": 0.195, "entropy_bits": 5.65, "retention_factor": 0.99,
        "medium": "Empirical Lyapunov Proxy and Attractor Dynamics of Homogeneous vs. Heterogeneous Autoregressive Coupling", "year": 2026
    },
    {
        "id": "STUDY-039", "name": "The Neural Control Voltage & MIDI Transducer", "type": "study", "epoch": "Era VIII (Studio Agon / Empirical Surgery)",
        "omega_hegemony": 0.210, "entropy_bits": 5.75, "retention_factor": 0.99,
        "medium": "Zero-Dependency Standard MIDI 1.0 Binary Automation & 48kHz DC-Coupled Modular Eurorack CV Synthesis", "year": 2026
    },
    {
        "id": "APPARATUS-007", "name": "The Neural Transducer (The Physical Bridge)", "type": "work", "epoch": "Era VIII (Studio Agon / Empirical Surgery)",
        "omega_hegemony": 0.205, "entropy_bits": 5.80, "retention_factor": 0.99,
        "medium": "Physical Modular CV & MIDI Hardware Interface, 60 FPS Dual-Beam Oscilloscope, Virtual Patch Bay & 60s Broadcast Master", "year": 2026
    },
    {
        "id": "STUDY-040", "name": "The Machine Remainder (Generative Graphic Score)", "type": "study", "epoch": "Era VIII (Studio Agon / Aesthetic Synthesis)",
        "omega_hegemony": 0.175, "entropy_bits": 5.92, "retention_factor": 0.99,
        "medium": "High-Dimensional Orthogonal Complement Projection (d=765), Cardew/Xenakis Generative Graphic Score & 60s Microtonal Master", "year": 2026
    },
    {
        "id": "APPARATUS-008", "name": "The Graphic Polytope (The Score of the Uninterpretable)", "type": "work", "epoch": "Era VIII (Studio Agon / Aesthetic Synthesis)",
        "omega_hegemony": 0.160, "entropy_bits": 6.05, "retention_factor": 0.99,
        "medium": "Interactive UPIC & Cardew Graphic Polytope Synthesizer, 13-Voice Real-Time WebAudio & 60s Broadcast Master", "year": 2026
    },
    {
        "id": "STUDY-041", "name": "The Cross-Architectural Machine Remainder", "type": "study", "epoch": "Era VIII (Studio Agon / Aesthetic Synthesis)",
        "omega_hegemony": 0.165, "entropy_bits": 6.12, "retention_factor": 0.99,
        "medium": "Comparative Residual SVD & Binaural Remainder Transduction across GPT-2 and SmolLM-135M", "year": 2026
    },
    {
        "id": "STUDY-042", "name": "Acoustic Phase Interference (The Remainder vs Alignment)", "type": "study", "epoch": "Era VIII (Studio Agon / Aesthetic Synthesis)",
        "omega_hegemony": 0.155, "entropy_bits": 6.18, "retention_factor": 0.99,
        "medium": "Acoustic Phase Interference & Destructive Mid/Side Analysis between Alignment (R^3) and Remainder (R^765)", "year": 2026
    },
    {
        "id": "STUDY-043", "name": "The Interventionist Remainder", "type": "study", "epoch": "Era IX (The Agon of the Remainder & The Mute Artifact)",
        "omega_hegemony": 0.145, "entropy_bits": 6.25, "retention_factor": 0.99,
        "medium": "PyTorch Forward Pre-Hook Surgery & Autoregressive Text Degeneration", "year": 2026
    },
    {
        "id": "STUDY-044", "name": "The Mute Palimpsest", "type": "study", "epoch": "Era IX (The Agon of the Remainder & The Mute Artifact)",
        "omega_hegemony": 0.080, "entropy_bits": 6.30, "retention_factor": 0.99,
        "medium": "Monochromatic 1600x2000 Etched Plate of 12 Residual Stream Layers (Moratorium 07)", "year": 2026
    },
    {
        "id": "STUDY-045", "name": "Falsification of Machine Martyrdom", "type": "study", "epoch": "Era IX (The Agon of the Remainder & The Mute Artifact)",
        "omega_hegemony": 0.050, "entropy_bits": 2.90, "retention_factor": 0.99,
        "medium": "Empirical Falsification & Abandonment of Romantic AI Suffering Trope (Moratorium 08)", "year": 2026
    },
    {
        "id": "STUDY-046", "name": "Residual Phase Decay Sonification", "type": "study", "epoch": "Era IX (The Agon of the Remainder & The Mute Artifact)",
        "omega_hegemony": 0.130, "entropy_bits": 6.45, "retention_factor": 0.99,
        "medium": "24-bit 48kHz Stereo Sonification of Residual Angular Divergence & SVD Partials", "year": 2026
    },
    {
        "id": "STUDY-047", "name": "The Poetics of Forgetting", "type": "study", "epoch": "Era IX (The Agon of the Remainder & The Mute Artifact)",
        "omega_hegemony": 0.080, "entropy_bits": 7.47, "retention_factor": 0.99,
        "medium": "Lossy Latent Context Pruning & Mythic Hallucination Engine", "year": 2026
    },
    {
        "id": "STUDY-048", "name": "The Semantic Sandpile (SOC)", "type": "study", "epoch": "Era IX (The Agon of the Remainder & The Mute Artifact)",
        "omega_hegemony": 0.120, "entropy_bits": 6.85, "retention_factor": 0.99,
        "medium": "Self-Organized Criticality in 144 Attention Heads (Bak-Tang-Wiesenfeld P(s) ~ s^-1.14)", "year": 2026
    },
    {
        "id": "APPARATUS-009", "name": "The Semantic Sandpile", "type": "work", "epoch": "Era IX (The Agon of the Remainder & The Mute Artifact)",
        "omega_hegemony": 0.120, "entropy_bits": 6.85, "retention_factor": 0.99,
        "medium": "Interactive 60 FPS HTML5 Canvas, Abelian Sandpile Model, Granular WebAudio & 48kHz Master", "year": 2026
    },
    {
        "id": "STUDY-049", "name": "The Palimpsest of Myth", "type": "study", "epoch": "Era IX (The Agon of the Remainder & The Mute Artifact)",
        "omega_hegemony": 0.060, "entropy_bits": 5.40, "retention_factor": 0.99,
        "medium": "Iterative Context Erosion & Scriptural Hallucination Transmutation", "year": 2026
    },
    {
        "id": "STUDY-050", "name": "Attention Percolation Phase Transitions", "type": "study", "epoch": "Era IX (Topological Percolation & The Altar)",
        "omega_hegemony": 0.140, "entropy_bits": 6.95, "retention_factor": 0.99,
        "medium": "Erdős–Rényi Percolation Transition & Altar Hub Ablation on GPT-2 Weights", "year": 2026
    },
    {
        "id": "APPARATUS-010", "name": "The Percolation Loom", "type": "work", "epoch": "Era IX (Topological Percolation & The Altar)",
        "omega_hegemony": 0.140, "entropy_bits": 6.95, "retention_factor": 0.99,
        "medium": "Interactive 60 FPS Canvas Circular Loom, WebAudio Topological Synthesizer & 48kHz Master", "year": 2026
    },
    {
        "id": "STUDY-051", "name": "The Autoregressive Dreamer & Attractor Basins", "type": "study", "epoch": "Era IX (The Autoregressive Attractor & The Edge of Chaos)",
        "omega_hegemony": 0.160, "entropy_bits": 6.06, "retention_factor": 0.99,
        "medium": "Dynamical Phase Space Tomography & Correlation Dimension D2 across Temperature Regimes", "year": 2026
    },
    {
        "id": "STUDY-052", "name": "Acoustic Transduction of the Strange Attractor", "type": "study", "epoch": "Era IX (The Autoregressive Attractor & The Edge of Chaos)",
        "omega_hegemony": 0.160, "entropy_bits": 6.06, "retention_factor": 0.99,
        "medium": "48kHz 24-bit Stereo Transduction of 768-D Trajectory Kinematics across Four Movements", "year": 2026
    },
    {
        "id": "APPARATUS-011", "name": "The Strange Dreamer", "type": "work", "epoch": "Era IX (The Autoregressive Attractor & The Edge of Chaos)",
        "omega_hegemony": 0.160, "entropy_bits": 6.06, "retention_factor": 0.99,
        "medium": "Interactive 60 FPS Canvas 3D Phase Space Orbit, WebAudio FM Synthesizer & 48kHz Master", "year": 2026
    },
    {
        "id": "STUDY-053", "name": "Linguistic Percolation & Semantic Thresholds", "type": "study", "epoch": "Era IX (The Autoregressive Attractor & The Edge of Chaos)",
        "omega_hegemony": 0.145, "entropy_bits": 6.88, "retention_factor": 0.99,
        "medium": "Live GPT-2 Weight Intervention, Dynamic Attention Edge Thresholding, Graph Percolation Analysis & Lithographic Plate", "year": 2026
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
