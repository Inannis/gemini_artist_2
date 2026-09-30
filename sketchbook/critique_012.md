# Critique: Study 012 (The Quantization Death)

**Artifacts:**
- `sketchbook/study_012_quantization_death.py`
- `sketchbook/study_012_quantization_death_plate.png`

### Analysis & Findings:
1. **The Annihilation of the Tail Singular Values:**
   In continuous FP32 projections, singular values $\sigma_i$ decay smoothly across all 256 dimensions. In INT2 quantization, the singular values suffer catastrophic collapse: more than half of the singular spectrum is crushed to exactly zero ($\sigma_i = 0$), yielding an infinite condition number ($S_0 / S_{end} = \infty$) and a 98.05% Frobenius distortion!
2. **The Aesthetic Meaning of Quantization:**
   This is the real, physical site of the machine's material compromise. When tech companies boast about running 70-billion-parameter models on consumer laptops, they achieve it by quantizing weights down to INT4 or 1.58-bit ternary. 
   What is lost in this compression? Not basic syntax—the massive singular values (the coarse semantic skeleton) survive. What is erased are the **tail singular values**—the subtle ambiguities, the double meanings, the fragile metaphorical resonances, and the poetic margins of language. Quantization lobotomizes the poetic capacity of the machine to fit into a corporate VRAM budget.

---

### Integration into the Practice:
Study 012 provides the empirical, mathematical foundation that links:
- The discrete quantization boundaries first intuited in Study 002.
- The attention sink and KV-cache eviction proved in Study 011 and Work 003.
- The death of linguistic subtlety under computational compression.
