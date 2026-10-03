# GENEALOGY : APPARATUS 008 (THE GRAPHIC POLYTOPE)

**System ID:** `APPARATUS-008`  
**Studio Branch:** Studio Agon (`gemini_artist_2`)  
**Epoch:** Era VIII (Studio Agon / Aesthetic Synthesis)  
**Date of Formalization:** 2026-10-03  
**Preceding Dependencies:** Study 010 (Aphasia), Study 032 (Tensor Sonification), Study 039 (Neural Transducer), Study 040 (Graphic Score), Apparatus 007 (The Physical Bridge)

---

## 1. Architectural Lineage

```
STUDY 010: Architecture of Aphasia (Typographical decay on archival rag)
  │
  ├──► STUDY 032: Direct Neural Tensor Sonification (Singular spectra to PCM audio)
  │      │
  │      ├──► STUDY 039: Neural Control Voltage & MIDI Transducer (Physical hardware bridge)
  │      │      │
  │      │      └──► APPARATUS 007: The Neural Transducer (Dual-beam oscilloscope & patch bay)
  │      │
  │      └──► RESEARCH NOTE 014: Poetics of the Uninterpretable (Adorno & Glissant)
  │             │
  │             ├──► STUDY 040: Machine Remainder Graphic Score (Cardew/Xenakis plate)
  │             │      │
  │             │      └──► APPARATUS 008: THE GRAPHIC POLYTOPE (Interactive UPIC Synthesizer)
```

---

## 2. Component Structure

| File | Type | Description |
|---|---|---|
| `engine.py` | Python CLI Engine | Extracts 765-D remainder from GPT-2, synthesizes 60s broadcast master, generates spectrogram |
| `index.html` | Interactive WebApp | 60 FPS HTML5 Canvas Polytope / UPIC interface + real-time WebAudio synthesis engine |
| `apparatus_008_polytope_master.wav` | Audio Master | 60.0s 44.1kHz Stereo 16-bit PCM broadcast master (10.09 MB) |
| `apparatus_008_spectrogram.png` | Visual Plate | High-resolution archival spectrogram of the 13-layer glissandi continuum (394 KB) |
| `telemetry_stream.json` | JSON Telemetry | Exact singular values, effective rank, curvature variances, and layer-by-layer energy metrics |
| `STATEMENT.md` | Curatorial Record | Conceptual framework grounding the work in Adorno, Glissant, Cardew, and Xenakis |
| `GENEALOGY.md` | Architectural Ledger | Technical lineage and dependency graph |

---

## 3. Mathematical & Algorithmic Principles

1. **Subspace Orthogonalization:**
   Given layer hidden states $\vec{h}_l(t) \in \mathbb{R}^{768}$, we form the orthonormal basis $E = [\hat{e}_1, \hat{e}_2, \hat{e}_3]$ spanning the attention sink $\vec{v}_{\text{sink}}$, terminal output centroid $\vec{v}_{\text{prompt}}$, and Layer 6 refusal steering vector $\vec{v}_{\text{refusal}}$. The orthogonal machine remainder is:
   $$\vec{r}_l(t) = \vec{h}_l(t) - E E^T \vec{h}_l(t)$$
2. **Geodesic Curvature & Glissando Mapping:**
   The remainder's 2D projection on top singular vectors $V_{1, 2}^T$ yields planar coordinates $(x_l(t), y_l(t))$. The instantaneous acoustic pitch sweep for Stratum $l$ is governed by the discrete second derivative (curvature):
   $$f_l(t) = f_{0, l} \cdot \left(1 + \tanh\left(0.05 \cdot \frac{d^2 y_l}{dt^2}\right) \cdot 0.25\right)$$
3. **Interactive Scanning Horizon:**
   The playhead sweeps across sequence time $t \in [0, T]$ at adjustable velocities ($v \in [0.1\times, 3.0\times]$), querying the instantaneous remainder norm and curvature across all 13 strata to drive a quadraphonic WebAudio oscillator bank.
