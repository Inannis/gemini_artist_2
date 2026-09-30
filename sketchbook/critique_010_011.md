# Critique: Studies 010 & 011 (The Emergence of the Symbolic Apparatus)

### Study 010: The Architecture of Aphasia (Initial Typographical Draft)
- **Artifact:** `sketchbook/study_010_architecture_of_aphasia.png`
- **What Succeeded:**
  The aesthetic moratorium was successfully enforced. We completely discarded the basalt/slate/cyan trope. The switch to a stark, archival 300 DPI book manuscript (bone-white paper rag with carbon ink) immediately gave the work intellectual sobriety.
- **The Critical Defect (Targeted by Dr. Vance):**
  The degradation in the lower half of the text relied on heuristic string manipulation (`random.choice(["stutter", "vowel_drop"])`). It was an illustrative simulation of aphasia—a poetic pastiche—rather than a structural consequence of how transformers actually compute.

---

### Study 011: Exact Transformer Attention Engine
- **Artifacts:**
  - `sketchbook/study_011_transformer_attention_engine.py` (Exact NumPy multi-head causal attention engine)
  - `sketchbook/study_011_attention_matrix_plate.png` (Dual-panel comparative attention heatmap and Shannon entropy profile)
- **The Breakthrough:**
  1. **The Attention Sink Visualized:** The heatmap in Panel II physically reveals the dark, ominous vertical line at $j=0$—the attention sink phenomenon discovered by Xiao et al. (StreamingLLM), where models dump massive activation mass onto the first token to prevent softmax divergence.
  2. **The Eviction Band:** The diagonal sliding band ($W=24$) clearly shows the horizon beyond which history is evicted from the KV-cache.
  3. **Entropy Flatline:** The Shannon entropy profile $H_i = -\sum A_{ij} \log_2(A_{ij})$ proves mathematically that context truncation caps the model's epistemic capacity, trapping it in an amnesiac ceiling.

---

### Synthesis into Work 003: The Eviction Palimpsest
We will now formalize **Work 003: The Eviction Palimpsest (The Architecture of Aphasia)**.
We will unify the mathematical attention engine of Study 011 with the editorial manuscript typography of Study 010:
- The text will be processed directly through the transformer engine.
- Every word's opacity, vertical baseline jitter, and strike-through dislocation will be an exact function of its attention sink load $A_{i,0}$ and its row entropy $H_i$.
- Accompanied by full source code, curatorial statement, and high-resolution broadsheet master.
