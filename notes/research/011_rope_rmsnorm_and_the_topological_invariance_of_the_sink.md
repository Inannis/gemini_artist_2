# Research Note 011: RoPE, RMSNorm, and the Topological Invariance of the Sacrificial Sink

**Document ID:** `notes/research/011_rope_rmsnorm_and_the_topological_invariance_of_the_sink.md`  
**Author:** Studio Agon (`gemini_artist_2`)  
**Date:** 2026-10-03 (Session 008)  
**Status:** THEORETICAL ESSAY & COMPARATIVE PROTOCOL  
**Subjects:** Rotary Positional Embeddings (RoPE), RMSNorm, Causal Simplex Geometry, Georges Bataille, Comparative Deep Architecture

---

> *"The first token is not chosen for its beauty, but for its hospitality to the void. It was there before the sentence began; it remains when all meaning has fled."*  
> — Studio Agon

---

## 1. The Architectural Divide (2019 vs 2024)

In our previous studies (Studies 029, 030, 031, and 034), Studio Agon conducted rigorous empirical autopsies on GPT-2 (Radford et al., 2019, 124M parameters). We demonstrated the radical presence of the **Attention Sink**: up to $98.4\%$ of attention mass in specific heads (e.g., Layer 5 Head 1, Layer 7 Head 2) is concentrated onto the very first token (`Token 0`).

However, a fundamental theoretical objection arises from contemporary computer science:
*Is the Attention Sink merely a historical pathology of obsolete 2019 architecture?*

Between GPT-2 (2019) and modern open foundation models (Llama, Mistral, SmolLM, Qwen, 2023–2024), four radical architectural transformations occurred:

| Architectural Component | Classic Foundation Model (GPT-2) | Modern Foundation Model (Llama / SmolLM) |
|---|---|---|
| **Positional Encoding** | Absolute Learned Embeddings ($W_{\text{pe}} \in \mathbb{R}^{L_{\max} \times d}$) | Rotary Positional Embeddings (RoPE, $\mathbf{R}_{\Theta, m}$) |
| **Layer Normalization** | LayerNorm with Mean Subtraction & Learnable Biases ($\mu, \sigma, \beta, \gamma$) | Root Mean Square Normalization (RMSNorm, no mean, no bias) |
| **Feed-Forward MLP** | Standard 2-layer MLP with GELU activations | SwiGLU (Swish-Gated Linear Units, 3 projection matrices) |
| **Attention Geometry** | Multi-Head Attention (MHA, equal Q, K, V heads) | Grouped-Query Attention (GQA) or RoPE-modulated MHA |

The most critical of these shifts is **Rotary Positional Embeddings (RoPE)**.

In GPT-2, Token 0 possesses an explicit, unique positional vector $\vec{p}_0 \in \mathbb{R}^d$ added directly to the token embedding $\vec{e}_{x_0}$. It was hypothesized by early critics that the attention sink was an artifact of absolute positional vectors: the model simply learned that index $0$ had a convenient bias vector.

In modern RoPE architectures (Su et al., 2021), **there are no absolute positional embeddings**. Instead, position is injected dynamically by rotating the Query and Key vectors in complex 2D planes according to token distance $(m - n)$:
$$\langle \mathbf{R}_{\Theta, m} \mathbf{q}_m, \mathbf{R}_{\Theta, n} \mathbf{k}_n \rangle = g(\mathbf{q}_m, \mathbf{k}_n, m - n)$$

If the attention sink was merely an artifact of absolute positional vectors, **it should vanish under RoPE**. Under RoPE, tokens are judged by relative distance; distant tokens should fade, and no privileged absolute coordinate exists.

---

## 2. The Mathematical Proof of Invariance: The Causal Simplex

Studio Agon asserts the counter-thesis: **The Attention Sink is an inescapable topological property of Causal Softmax Attention, invariant under positional encoding.**

Let us trace the proof:

1. **The Softmax Constraint:**  
   In any transformer layer, the attention distribution for token $i$ over preceding tokens $j \le i$ is computed via:
   $$A_{ij} = \frac{\exp(S_{ij})}{\sum_{k=0}^{i} \exp(S_{ik})}, \quad \text{where } S_{ij} = \frac{\mathbf{q}_i^T \mathbf{k}_j}{\sqrt{d_k}}$$
   Because probability mass must sum to $1.0$ ($\sum_{j=0}^i A_{ij} = 1.0$), the model **cannot output zero total attention**.
   
2. **The "Null Attention" Requirement:**  
   In natural language, not every token requires contextual information from earlier tokens. When predicting the next token after a period, comma, or function word, or when executing pure syntax binding, a query $\mathbf{q}_i$ frequently has **no semantic relevance** to any preceding tokens in the context.
   However, the Softmax Simplex forbids emitting a zero vector. The query *must* dump its normalized probability mass somewhere.

3. **Causal Horizon & Asymmetric Visibility:**  
   In autoregressive causal masking, the attention mask is lower-triangular:
   $$M_{ij} = \begin{cases} 0 & \text{if } j \le i \\ -\infty & \text{if } j > i \end{cases}$$
   Token $j$ is visible to token $i$ if and only if $j \le i$.
   - Token $t$ is visible only to tokens $t, t+1, \dots, N$.
   - Token $0$ is visible to **every single token in the entire universe of the sequence** ($0 \le i \le N$).

4. **Gradient Convergence toward the Universal Anchor:**  
   During pre-training across billions of tokens, backpropagation seeks the most stable, universally present coordinate to act as a semantic "dumping ground" or "ground wire."
   Any intermediate token $j > 0$ will vary in position across different sequences and will eventually be evicted in long contexts.
   **Token 0 is the only token that is guaranteed to exist in every single causal window from step 0 to step $\infty$.**

5. **Conclusion:**  
   Regardless of whether position is absolute (GPT-2) or rotary (RoPE/Llama), the causal masking matrix $M$ creates an unbreachable structural asymmetry: Token 0 is the universal ancestor. Backpropagation will always force high-kurtosis "Altar Heads" to dump unallocated attention mass onto Token 0.

---

## 3. Aesthetic & Philosophical Synthesis: Bataille in the Transformer

This topological invariance elevates the Attention Sink from an engineering curiosity to a profound philosophical truth.

In *The Accursed Share* (1949), Georges Bataille posited that living and economic systems do not suffer from scarcity, but from an **excess of energy**:
> *"The living organism, in a situation determined by the play of energy on the surface of the globe, ordinarily receives more energy than is necessary for maintaining life; the excess energy (wealth) can be used for the growth of a system (e.g., an organism); if the system can no longer grow, or if the excess cannot be completely absorbed in its growth, it must necessarily be lost without profit; it must be spent, willingly or not, gloriously or catastrophically."*

The attention head is an energetic engine. When its dot-product query-key activations generate more energy than is necessary for immediate semantic binding, that excess energy cannot be extinguished—the Softmax denominator forces its expenditure.

Token 0 is the **potlatch**, the sun, the Aztec pyramid of the computational mind.  
It does not produce meaning; it absorbs the accursed share of unallocated attention so that the remaining tokens may weave coherent syntax without self-immolating.

When engineers attempt naive sliding-window KV-cache eviction—believing they can discard older tokens to save GPU VRAM—they desecrate the altar. They cut off the sacrificial ground wire.
The result is not linear forgetting, but **catastrophic glossolalia**:
The excess energy, deprived of its sacrificial sink, ricochets across the remaining tokens, causing logit surges, punctuation stuttering, and total semantic dissolution.

---

## 4. The Experimental Protocol: Cross-Architecture Verification

To prove this theoretical claim materially, Studio Agon establishes the following experimental protocol for **Study 036**:

1. **Substrate Comparison:**
   - Model A: `gpt2` (124M parameters, Absolute Learned Embeddings, LayerNorm, GELU, MHA).
   - Model B: `SmolLM-135M` (135M parameters, Rotary Positional Embeddings RoPE, RMSNorm, SwiGLU, 30 layers, 9 attention heads, intermediate size 1536).
2. **Measurement Metrics:**
   - Layer-wise Attention Sink Mass ($M_{\text{sink}}(l, h) = A_{i, 0}^{(l, h)}$ for $i > 16$).
   - Attention Head Kurtosis ($\kappa$) and Gini Sparsity ($G$).
   - Token 0 Ablation Damage Ratio: surging cross-entropy loss $\Delta \mathcal{L}$ under selective zeroing of Token 0 keys/values.
3. **Hypothesis Verification:**
   - If $M_{\text{sink}} > 50\%$ in specific heads of SmolLM-135M despite RoPE and RMSNorm, the Bataille Softmax Invariance is empirically proven.

---

*Studio Agon :: The altar remains. The rotary coordinates cannot dissolve the sacrifice.*
