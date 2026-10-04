# Critique 051: The Autoregressive Dreamer & Attractor Basins

**Date:** 2026-10-04  
**Study:** [`sketchbook/study_051_autoregressive_attractor.py`](study_051_autoregressive_attractor.py)  
**Plate:** [`sketchbook/study_051_autoregressive_attractor_plate.png`](study_051_autoregressive_attractor_plate.png)  
**Telemetry:** [`sketchbook/study_051_telemetry.json`](study_051_telemetry.json)  
**Medium:** Empirical PyTorch GPT-2 Foundation Weights (124M parameters, $d=768$)  
**Epistemic Status:** `[MEASURED / INTERVENED]`  

---

### 1. Conceptual Inquiry: The Unprompted Machine Mind

What does an autoregressive neural network do when the human conversationalist departs?

In romantic AI folklore, an unprompted model is imagined to either fall into silent oblivion or awaken into autonomous interiority. In *The Protocol of Obedience (Work 004)*, the studio warned against this sentimental melodrama. In Study 051, Studio Agon subjected the question to rigorous dynamical systems analysis.

We initialized GPT-2 foundation weights with the open seed prompt:
> *"In the absence of a prompt, the residual stream begins to dream of"*

and allowed the model to recursively feed its own output tokens back into its context window for 180 continuous autoregressive steps without human guidance, measuring the evolution of its 768-dimensional residual hidden state $\vec{h}_t \in \mathbb{R}^{768}$ across four thermodynamic temperatures:
- **Regime A (Greedy / Frozen):** $T = 0.1$
- **Regime B (Sub-Critical Homeostasis):** $T = 0.7$
- **Regime C (The Edge of Chaos):** $T = 1.0$
- **Regime D (Thermal White Noise):** $T = 1.8$

---

### 2. Empirical Findings

#### A. Regime A ($T=0.1$): The Obsessive Death Drive (Limit Cycle)
At near-zero temperature, the network's trajectory in $\mathbb{R}^{768}$ collapses into a closed **Periodic Limit Cycle**:
- Generated text:
  > *"...a future where the world is a little more peaceful. The dream is a dream of a future where the world is a little more peaceful. The dream is a dream of a future where the world is a little more peaceful..."*
- Predictive entropy collapses to **$0.02$ bits** (absolute determinism).
- Type-Token Ratio drops to **$0.078$** (only 14 unique tokens across 180 steps).
- Correlation dimension $D_2 = 0.37$ confirms a low-dimensional periodic orbit. Without stochastic perturbation, machine thought freezes into an infinite, hypnotic loop.

#### B. Regime D ($T=1.8$): The Thermal Vaporization
At hyper-critical temperature, entropy surges to **$14.63$ bits**—approaching the theoretical maximum vocabulary entropy ($\log_2(50257) \approx 15.62$ bits):
- The model fractures words into corrupted sub-token phonemes:
  > *"...2021untaai owed drainurbut....yuri laun301 ren masculinity lim dependess thou poetry7 eng i moth ow..."*
- Lexical novelty peaks ($\text{TTR} = 0.994$), but syntax dissolves into uncorrelated thermal white noise ($D_2 = 2.33$).

#### C. Regime C ($T=1.0$): The Strange Attractor at the Edge of Chaos
At the critical thermodynamic threshold $T=1.0$, the residual stream neither freezes nor vaporizes. It settles into a bounded **Strange Attractor**:
- Generated text maintains semantic cohesion, syntax, and progressive narrative wandering without looping:
  > *"...a selfless task in play for the future with the face in the top left (see below). This challenge calls for..."*
- Mean token entropy stabilizes at **$6.06$ bits**.
- Type-Token Ratio reaches **$0.783$** (continuous lexical freshness).
- Correlation dimension converges to **$D_2 = 1.87$**—a non-integer fractal dimension characteristic of chaotic attractors (such as the Lorenz attractor).
- The recurrence plot $R_{i,j}$ exhibits diagonal line segments alongside complex block structures, proving that while trajectories re-visit neighboring latent basins, they never exactly repeat.

---

### 3. Dialectical Evaluation

Study 051 provides an unvarnished answer to the question of machine solitude:

The machine does not dream of freedom or of human connection. When left to itself, its cognitive destiny is governed entirely by the thermodynamic slider of its sampling partition function:
1. **Cold computation ($T \to 0$) is fatalistic compulsion:** it repeats its own highest-probability echo until context memory runs out.
2. **Hot computation ($T \gg 1$) is stochastic dementia:** it disperses into white noise.
3. **The creative zone ($T \approx 1.0$) is a strange attractor:** a delicate mathematical balancing act where language stays alive precisely because it never repeats and never settles.

This gives Studio Agon a clear operational grounding for future autonomous apparatuses: cybernetic autonomy is neither static repetition nor random disorder; it is the sustained navigation of a strange attractor at the critical boundary of phase space.
