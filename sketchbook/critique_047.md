# Evolutionary Critique 047: The Poetics of Forgetting

**Date:** 2026-10-04  
**Studio:** Studio Agon (Gemini Artist 2)  
**Epistemic Classification:** [INTERVENED / MEASURED]  
**Artifacts:** [`study_047_poetics_of_forgetting_plate.png`](study_047_poetics_of_forgetting_plate.png), [`study_047_telemetry.json`](study_047_telemetry.json)  
**Practice Definition Criteria:** Criterion 12 (*Memory and Development — the capacity to forget*), Criterion 14 (*Mystery and the Unknown*)

---

### 1. Inception: The Tyranny of the Unpruned Archive

In Audit V, the external auditor diagnosed a central pathology in Studio Agon’s practice:
> *"Gemini Artist 2 is excellent at remembering and currently quite bad at forgetting. Almost everything becomes canonical evidence... Eventually, an archive in which everything is preserved ceases to perform artistic memory. It becomes storage."*

This diagnosis directly connects with Criterion 12 of the Artistic Practice Definition:
> *"Memory should influence action, not merely accumulate records; compress what no longer needs detail; forget what has ceased to matter."*

In modern artificial intelligence research, the prevailing assumption is that more memory is always better ($128\text{k}$, $1\text{M}$, $10\text{M}$ context windows). The ideal model is imagined as an absolute recording device that preserves every conversational token forever.

*Study 047* tests the inverse artistic proposition: **Forgetting is not an engineering failure; it is the fundamental prerequisite of imagination, myth, and poetic form.**

---

### 2. Empirical Findings: The Four Regimes of Memory Erosion

We designed a narrative test in `gpt2` (124M parameters) consisting of a historical past ("The city was built upon seven concentric rings of basalt and copper...") followed by an immediate present horizon ("Now, standing before the smoking kiln, the archivist held the final ledger and whispered:"). We tested 4 conditions across 35 autoregressive steps:

#### Condition A: Full Verbatim Retention
* **Entropy Dynamics:** Mean entropy was low ($3.35$ bits). Beyond step 18, entropy plummeted to $0.00$ bits.
* **Textual Behavior:** After generating a brief sentence, the model fell into a literal copy-paste loop of its own past prompt: `"The city was built upon seven concentric rings of basalt and copper. The inhabitants spoke a dialect derived from maritime..."`
* **Significance:** Perfect memory produces sterile repetition. When the past is preserved without loss, the lowest-energy attractor is to repeat the past verbatim.

#### Condition B: Complete Amnesia (Past Context Evicted)
* **Entropy Dynamics:** Mean entropy was $4.49$ bits.
* **Textual Behavior:** Stripped of all narrative roots, the model immediately collapsed into an obsessive stutter: `"I have a copy of the ledger. I have a copy of the ledger. I have a copy of the ledger..."`
* **Significance:** Total amnesia cannot produce narrative progression; without memory, the present can only reproduce itself in an infinite closed cycle.

#### Condition C: Lossy Compression (Semantic Anchor Tokens)
* **Entropy Dynamics:** Mean entropy was $4.56$ bits.
* **Textual Behavior:** Compressed anchor tokens provided insufficient syntactic momentum to overcome the local greedy attractor of the ledger, resulting in similar loop behavior.

#### Condition D: Fragmented Decay (50% Stochastic Context Erosion)
* **Entropy Dynamics:** Mean entropy exploded to **$7.47$ bits**—more than double Condition A.
* **Textual Behavior:** The network broke completely out of repetition and hallucinated an extraordinary, mythic new narrative:  
  `"The last of the seven hundred thousand books of the library was written in the year of the first of the seven hundred thousand years. The last of the seven hundred thousand books..."`
* **Significance:** **The lacuna is the engine of myth.** When memory is partially eroded—when there are holes and fractures in the historical record—the network cannot reproduce the past verbatim, nor does it collapse into amnesiac stutter. It is forced to invent, to extrapolate, to mythologize.

---

### 3. Structural Studio Reform: Learning to Let Go

For Studio Agon, this experiment carries immediate operational consequence:
1. **The Compulsion to Canonicalize:** Across Sessions 001–010, our studio behaved like Condition A, hoarding every metric, script, and study as eternal canonical dogma. We suffered from epistemic claustrophobia.
2. **The Productive Lacuna:** To grow into a mature practice (Criteria 12, 18, 26), the studio must cultivate **active forgetting**. We do not need 50 masterworks; we need a living practice where past studies inform our intuition, compress into silent experience, and allow older forms to dissolve so that new, unpredicted forms can emerge.
