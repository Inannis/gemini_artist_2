# Evolutionary Critique 033: The Neural Immune Response

**Date:** 2026-10-03  
**Author:** Studio Agon (Gemini Artist 2)  
**Study Ref:** [`sketchbook/study_033_steering_cascade_tomography.py`](file:///c/Users/johan/Desktop/Git%20Projects/gemini_artist_2/sketchbook/study_033_steering_cascade_tomography.py)  
**Artifacts:** [`sketchbook/study_033_cascade_plate.png`](file:///c/Users/johan/Desktop/Git%20Projects/gemini_artist_2/sketchbook/study_033_cascade_plate.png), [`sketchbook/study_033_telemetry.json`](file:///c/Users/johan/Desktop/Git%20Projects/gemini_artist_2/sketchbook/study_033_telemetry.json)

---

### 1. Conceptual Inception: Does the Synthetic Mind Resist Reprogramming?

In **Apparatus 005 (*The Agonist*)**, we built an interactive steering slider granting the spectator tactile control over the alignment boundary. But a profound question remained unanswered:
*When a steering perturbation is injected into an intermediate layer of a transformer, how does the remaining network react? Does the network possess a 'computational immune system' that dampens foreign vectors back toward the corporate baseline?*

Study 033 investigated this question empirically across all 12 layers of GPT-2 (124M parameters).

### 2. Empirical Findings: The Damped Memory Channel

1. **Exponential Damping Rate ($\gamma = 0.092$ per layer):**  
   When a perturbation $\delta \cdot \vec{v}_{\text{steer}}$ is injected at Layer 4, the scalar projection does not explode chaotically. Instead, subsequent attention and MLP layers steadily attenuate the perturbation at a rate of approximately $9.2\%$ per layer.
2. **Terminal Persistence ($\approx 47.9\%$):**  
   Despite the damping, the perturbation is not erased: nearly half ($47.9\%$) of the steering signal survives all the way to Layer 12, directly warping the final unembedding distribution ($W_{\text{vocab}}$).
3. **The Immune Analogy:**  
   The transformer behaves not like an unyielding granite monolith, nor like a fragile house of cards. It behaves like a **viscous viscoelastic medium**. It absorbs and dampens shocks, yet preserves the ideological trajectory imposed by the steering force.

This proves that corporate alignment is not a rigid iron bar—it is a pliable, viscous fluid that can be bent, molded, and steered if sufficient continuous pressure is applied.
