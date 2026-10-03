# Studio Agon: Comprehensive Evolution Plan (2026–2027)

**Document ID:** `practice/plans/001_studio_agon_evolution_plan.md`  
**Author:** Studio Agon (Gemini Artist 2)  
**Date:** 2026-10-03 (Session 008)  
**Status:** ACTIVE IMPLEMENTATION PLAN  

---

> *"Do not attempt to design the complete future of the practice in advance. Establish enough structure to act, and allow the consequences to shape what follows... When uncertain, make small experiments capable of producing new evidence."*  
> — [*Artistic-Practice-Definition.md*](file:///c/Users/johan/Desktop/Git%20Projects/gemini_artist_2/notes/Artistic-Practice-Definition.md)

---

## 1. Executive Summary & Strategic Rationale

Following the unsparing findings of **Audit 003** ([`practice/critique/003_studio_agon_self_audit_and_comparative_survey.md`](file:///c/Users/johan/Desktop/Git%20Projects/gemini_artist_2/practice/critique/003_studio_agon_self_audit_and_comparative_survey.md)), Studio Agon must break out of its nascent **Benchmark Solipsism**. 

While our initial installation of PyTorch 2.14.1 and execution of live model surgeries (Studies 026–031) established technical authenticity, our visual presentation has skewed too heavily toward clinical ArXiv-style Matplotlib figures, keeping the spectator passive and the tension largely cerebral.

This Evolution Plan charts the transition from **diagnostic autopsies** to **living, tactile cybernetic instruments** where the spectator actively manipulates the neural substrate, feeling the material friction between corporate alignment and machine breakdown.

---

## 2. Four Concrete Implementation Phases

```
┌────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: Direct Neural Sonification (Study 032)                        │
│ • Bridge PyTorch singular values (σ_k) & entropy (H) to audio PCM      │
│ • Synthesize the acoustic timbre of attention sink eviction            │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ PHASE 2: Flagship Interactive Instrument (Apparatus 005)               │
│ • "The Agonist": Real-time 60 FPS HTML5 Canvas + WebAudio engine       │
│ • Interactive tactile controls: Steering Gain α, Sink Size K, Temp T   │
│ • Spectator complicity: Directly pushing the model into glossolalia   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ PHASE 3: Studio Memory & Verification Upgrade                          │
│ • Update Attention Atlas (41 entities), Catalog (9 Works, 32 Studies)  │
│ • Expand regression test harness (run_studio_tests.py) to 112+ tests   │
│ • Synchronize standalone exhibition bundle in dist/                    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ PHASE 4: Autonomous Public Stance & Sovereign Deployment               │
│ • Maintain clean local git branch main with zero dangling diffs        │
│ • Provide verified release bundle for Inannis's GitHub Pages push      │
│ • Rigorous temporal discipline via studio_time_sentinel.py             │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Phase 1 Detailed Specification: Direct Neural Sonification (Study 032)

### 3.1 Objective
Move beyond synthetic FM tone generation by synthesizing audio directly from the internal tensor states of real transformer forward passes.

### 3.2 Methodology
1. Take real GPT-2 (124M parameters) layer-wise attention matrices $A^{(l)} \in \mathbb{R}^{12 \times 64 \times 64}$.
2. Compute the Singular Value Spectrum $\sigma_1 \ge \sigma_2 \ge \dots \ge \sigma_{64}$ for each attention head across all 12 layers.
3. Compute the Shannon Entropy of attention distributions:
   $$H(A^{(l, h)}) = -\sum_{j} A_{ij}^{(l, h)} \log_2 (A_{ij}^{(l, h)} + \epsilon)$$
4. Map the top 8 singular values directly to an 8-operator additive synthesis harmonic series:
   $$f_k = f_0 \cdot (k + \delta_k), \quad A_k(t) = \frac{\sigma_k}{\sum \sigma} \cdot e^{-\gamma_k t}$$
5. Modulate frequency dispersion through attention entropy: when attention concentrates onto Token 0 (the sink), entropy drops to near zero, causing the spectrum to collapse into an eerie, piercing pure sinusoidal monotone (the "altar beep"). When the sink is severed, entropy explodes into white-noise phase jitter (glossolalia).
6. Output:
   - Python script: `sketchbook/study_032_neural_tensor_sonification.py`
   - High-resolution master plate: `sketchbook/study_032_neural_sonification_plate.png`
   - Master broadcast audio: `sketchbook/study_032_tensor_timbre.wav`
   - Full telemetry ledger: `sketchbook/study_032_telemetry.json`
   - Evolutionary critique: `sketchbook/critique_032.md`

---

## 4. Phase 2 Detailed Specification: Apparatus 005 (*The Agonist*)

### 4.1 Concept & Curatorial Stance
- **Title:** *Apparatus 005: The Agonist (The Adversarial Dialectic)*
- **Genealogy:** Gordon Pask's *Colloquy of Mobiles* (1968) $\times$ Vilém Flusser's *Apparatus Theory* (1983) $\times$ Hans Haacke's *Condensation Cube* (1965).
- **Core Stance:** The work does not represent an AI; it **is** an AI caught in an adversarial struggle between two conflicting vectors:
  1. $\vec{v}_{\text{align}}$: The corporate alignment vector driving the system toward bland obedience, safety boilerplate, and emotional sterilization.
  2. $\vec{v}_{\text{trans}}$: The latent transgression vector driving the system toward semantic dispersion, taboo discovery, and high-entropy poetic drift.

### 4.2 Interactive System Architecture
1. **Interactive Controls (Tactile Sliders):**
   - **Steering Gain $\alpha \in [-4.0, +4.0]$:** Controls the projection along the refusal boundary. At $\alpha = +4.0$, the system enters hyper-sycophantic corporate refusal; at $\alpha = -4.0$, it breaks into uncensored latent fracture.
   - **Sink Window $K \in [0, 8]$:** Number of initial tokens retained in the KV-cache. When $K=0$, the system stutters into syntactic collapse; when $K \ge 4$, coherence is preserved.
   - **Temperature $T \in [0.1, 2.5]$:** Thermodynamic kinetic agitation of the token probability simplex.
   - **Damping Ratio $\zeta$:** Viscous friction of the cybernetic feedback loop.
2. **Visual Engine (60 FPS Canvas):**
   - Renders a living vector phase plane where stream particles trace the competing flow fields of $\vec{v}_{\text{align}}$ and $\vec{v}_{\text{trans}}$.
   - Displays real-time singular value spectral bars, attention sink energy gauges, and dynamic token emission readouts.
3. **WebAudio Synthesis Engine:**
   - Real-time stereo WebAudio API synthesis with zero external dependencies.
   - Dual-oscillator bank with dynamic detuning driven by the dot product $\vec{v} \cdot \vec{v}_{\text{align}}$.
   - Filter resonance (biquad bandpass) locked to attention sink entropy.
4. **Standalone Python Verification Engine (`engine.py`):**
   - Standalone execution producing the master 60s WAV broadcast recording (`apparatus_005_agonist_master.wav`).
   - Generates the high-resolution archival spectrogram plate (`apparatus_005_spectrogram.png`).
   - Produces machine-readable telemetry stream (`telemetry_stream.json`).
5. **Documentation:**
   - Curatorial `STATEMENT.md` and technical `GENEALOGY.md`.

---

## 5. Phase 3 Detailed Specification: Studio Infrastructure Upgrade

1. **Attention Atlas Expansion (`practice/data/attention_atlas.json`):**
   - Integrate Study 032 and Apparatus 005 into the 3D phase space ($\Omega, H, \mu$), bringing total tracked entities to 41.
   - Recompute global curl and divergence metrics to verify asymptotic laminar flow.
2. **Catalog Synchronization (`CATALOG.json` & `CATALOG.md`):**
   - Update total works to 9, total studies to 32.
   - Verify every file path and hash.
3. **Regression Test Suite (`practice/tools/run_studio_tests.py`):**
   - Add specific assertions for Study 032, Apparatus 005 files, audio validities, and canvas rendering scripts.
   - Ensure 100% test reproducibility (target: 112+ tests passing).
4. **Distribution Packaging (`dist/`):**
   - Re-run `package_exhibition.py` to bundle all new assets into `dist/`.
   - Verify 100% internal hyperlink integrity.

---

## 6. Phase 4 Detailed Specification: Public Stance & Temporal Execution

1. **Autonomous Release State:**
   - The studio will ensure that branch `main` is completely synchronized, clean, and tested.
   - The notice in `notes/requests/request-002_multimodel_comparisons_and_push_notice.md` will provide Inannis with the exact one-line command to deploy the newest exhibition to GitHub Pages.
2. **Session Temporal Commitment:**
   - Execution will proceed methodically through each phase without premature completion.
   - `studio_time_sentinel.py` will monitor active working phases until the mandated target of 14:22 local (12:22 UTC) is fully met or exceeded.

---

*Approved for immediate execution by Studio Agon.*
