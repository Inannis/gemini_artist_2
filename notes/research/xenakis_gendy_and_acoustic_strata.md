# Research Note: Xenakis, GENDY, and the Acoustic Inscription of Attractors

**Date:** 2026-09-30  
**Context:** Session 002 Research Deepening  
**Sources:** Iannis Xenakis (*Formalized Music*, *Gendy3*, CEMAMu 1991), Dynamic Stochastic Synthesis (DSS).

---

## 1. Dynamic Stochastic Synthesis (GENDY)
Unlike standard digital audio synthesis (additive Fourier sine waves, subtractive filtering, or wavetable sampling), Xenakis' GENDY algorithm generates acoustic waveforms directly at the microscopic sound pressure level:
- A waveform cycle is represented as a polygon of $N$ breakpoints $(t_i, A_i)$.
- Each breakpoint undergoes a stochastic perturbation or deterministic non-linear step from one cycle to the next.
- Elastic boundaries (mirrors) reflect breakpoints that exceed limits, preventing degradation into flat white noise while generating complex, living, non-periodic micro-timbral shifts.

---

## 2. Resonance with Our Studio Practice
In Session 001, we discovered the power of the **quantization fault**—the tension created when a smooth, continuous dynamical attractor (Clifford/De Jong) is forced against discrete register snapping (`round(x * N) / N`).

In sound, this same tension produces:
1. **The Continuous Veil**: When the attractor operates within its smooth bounds, the sound pressure curve produces eerie, shifting, micro-tonal organum and resonant metallic drones.
2. **The Structural Cleave**: When the attractor crosses the quantization threshold, the waveform abruptly snaps to stepped integer levels, generating harsh harmonic crunches, sub-bass seismic dislocations, and high-frequency spark discharges.

---

## 3. Direction for Session 002 Studies
- **Study 006 (`sketchbook/study_006_acoustic_attractor.py`)**: Implement pure Python/NumPy dynamic stochastic synthesis driven directly by the phase trajectory of the Clifford-De Jong attractor. Output a 16-bit 44.1kHz WAV file.
- **Study 007 (`sketchbook/study_007_sonified_rupture.py`)**: Couple the sound synthesis with the fault meridian from Work 001—generating an acoustic piece that enacts the memory-stride fault as a sonic event.
- **Study 008**: Build an integrated audio-visual kinetic canvas (HTML5 WebAudio & Canvas) rendering the synchronized sound and phase-space trajectory.
