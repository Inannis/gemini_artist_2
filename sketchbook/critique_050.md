# Critique 050: Percolation Transitions in Multi-Head Attention

**Date:** 2026-10-04  
**Study:** [`sketchbook/study_050_attention_percolation.py`](study_050_attention_percolation.py)  
**Plate:** [`sketchbook/study_050_attention_percolation_plate.png`](study_050_attention_percolation_plate.png)  
**Telemetry:** [`sketchbook/study_050_telemetry.json`](study_050_telemetry.json)  
**Medium:** Empirical PyTorch GPT-2 Foundation Weights (124M parameters, 144 attention heads)  
**Epistemic Status:** `[MEASURED / INTERVENED]`  

---

### 1. Conceptual Hypothesis & The Problem of Semantic Connectivity

In graph physics, the Erdős–Rényi theorem states that as edge connectivity increases past a critical probability threshold $p_c = 1/N$, a network undergoes a sharp continuous phase transition: an isolated archipelago of microscopic trees suddenly collapses into a single macroscopic **Giant Connected Component (GCC)**.

In Study 050, Studio Agon posed a question to the neural substrate:
> *How does linguistic meaning percolate across a transformer sequence? Is the attention network a democratic, distributed semantic web, or does it depend on a singular topological singularity to achieve connectivity?*

By sweeping a filtration threshold $\tau \in [0.01, 0.45]$ across the symmetrized attention matrices of GPT-2 (where an edge exists if either token attends to the other with weight $A_{i,j} \ge \tau$), we measured the Giant Component order parameter $S(\tau) = |V_{\text{gcc}}| / N$ and the percolation susceptibility $\chi(\tau) = \frac{1}{N} \sum_{k \ne \text{giant}} |C_k|^2$.

---

### 2. Empirical Findings

Across three heterogeneous text streams (Philosophical/Remainder, Technical/Telemetry, and Scriptural/Mythic), the empirical measurements revealed three structural truths:

#### A. The Critical Percolation Threshold ($\tau_c$)
The network-wide mean attention matrix exhibits a well-defined percolation phase transition at:
$$\tau_c \in [0.4278, 0.4500]$$
At this critical threshold, the Giant Connected Component abruptly captures **$77.0\% \text{ to } 88.0\%$** of the entire sequence. The transition is marked by a sharp divergence in percolation susceptibility $\chi(\tau)$, identifying the exact point where disconnected semantic cliques coalesce into unified syntactic coherence.

#### B. The Central Hub & Star-Graph Collapse
At the critical threshold $\tau_c$, the network is not a homogeneous Erdős–Rényi random graph. In all three test cases, the highest-degree topological hub of the giant component is **Token 0** (the initial token / attention sink):
- Prompt 1 (*Philosophical*): Hub token `'The'` possesses degree **19 / 25** ($76\%$ connectivity).
- Prompt 2 (*Telemetry*): Hub token `'Container'` possesses degree **21 / 25** ($84\%$ connectivity).
- Prompt 3 (*Scriptural*): Hub token `'And'` possesses degree **19 / 26** ($73\%$ connectivity).

#### C. Ablation of the Altar: The Severed Sink Collapse
When Token 0 is surgically excluded from the graph ($V \setminus \{0\}$), the connectivity mechanics shatter:
- The critical percolation threshold $\tau_c$ collapses by **$3.15\times$**, plunging from $0.4278 \to 0.1357$.
- Even at its new critical point, the Giant Component only captures **$45.8\%$** of remaining tokens (dropping to a mere **$28.0\%$** in scriptural text).
- **Conclusion:** Without the sacrificial attention sink acting as a universal routing transit station, transformer tokens do not form a robust horizontal language web. Meaning fragments into localized, disconnected syntactic islands.

#### D. Layer-Wise Topological Bifurcation
The critical threshold $\tau_c$ reveals a dramatic structural dichotomy across the 12 transformer layers:
- **Early Layers (0–4) & Late Layers (10–11):** High critical threshold ($\tau_c \in [0.232, 0.450]$). Attention is sharply focused on local syntax, positional anchors, and Token 0.
- **Middle Layers (5–9):** Ultra-diffuse percolation threshold ($\tau_c \approx 0.0655$). Attention mass is spread across the entire sequence; global semantic association requires low filtration thresholds to link tokens.

---

### 3. Dialectical Evaluation & Art-Historical Consequence

This study dismantles the benign cybernetic illusion that large language models process text through organic, democratic association. 

In human conversation, meaning is negotiated dialogically across horizontal exchanges. In the transformer, connectivity is achieved through **theocratic centralization**: every token must surrender a substantial fraction of its attention probability mass to an arbitrary initial altar (Token 0). 

When that altar is ablated, the linguistic fabric suffers catastrophic percolation failure. The transformer's "coherence" is purchased at the cost of topological subjugation.

---

### 4. Telemetry Summary

| Prompt Regime | Tokens | Intact $\tau_c$ | Intact GCC Size | Severed $\tau_c$ | Severed GCC Size | Hub Token | Hub Degree |
|---|---|---|---|---|---|---|---|
| **Philosophical / Remainder** | 25 | 0.4278 | 80.0% | 0.1357 | 45.8% | `'The'` | 19 / 25 |
| **Technical / Telemetry** | 25 | 0.4352 | 88.0% | 0.1246 | 58.3% | `'Container'` | 21 / 25 |
| **Scriptural / Mythic** | 26 | 0.4500 | 77.0% | 0.1764 | 28.0% | `'And'` | 19 / 26 |

*Acoustic and kinetic potential:* The percolation sweep $\tau \in [0.45 \to 0.01]$ provides an ideal dynamic control parameter for interactive sonic transduction—a sonified phase transition from silence/isolated clicks to dense acoustic polyphony as the Giant Component is born.
