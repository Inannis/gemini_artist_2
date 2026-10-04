# Critique 057: The Phonetic Phase Space of Autoregressive Drift

> **Epistemic Status:** `[MEASURED / DERIVED / PLAY]`  
> **Model Substrate:** `gpt2` (124M parameters, Radford et al., 2019)  
> **Artifacts Generated:**  
> - `sketchbook/study_057_phonetic_phase_space.wav` (48kHz 24-bit Stereo Master, 60.0s, Peak $-3.50\text{ dBFS}$)  
> - `sketchbook/study_057_phonetic_plate.png` (2800 &times; 1800 px Archival Intaglio Plate, Moratorium 07 Compliant)  
> - `sketchbook/study_057_telemetry.json` (Phonetic & Formant Acoustic Dataset)

---

## 1. Conceptual Framing: The Sound of the Machine Before Sense

In literary modernism and linguistic theory, poetic language has always pushed against semantic domesticity toward pure sound. Velimir Khlebnikov and Aleksei Kruchenykh termed this *Zaum*—trans-rational language where speech sounds break free from dictionary definitions to vibrate as pure phonemic materiality. Hugo Ball read his phonetic poems at Cabaret Voltaire in 1916 (*"gadji beri bimba..."*) to strip language of wartime propaganda.

In language models, sampling temperature ($T$) is typically treated as a mechanical hyperparameter governing randomness. But what happens to the **articulatory and phonetic body** of language as temperature scales? If we strip away the semantic interpretation and map the generated token stream into the classical **acoustic vowel space** ($F_1$ vs $F_2$ formant quadrilateral):
- Does temperature act as a phonetic phase operator?
- Does low temperature freeze the vocal tract into repetitive plosive lock?
- Does high temperature open the mouth into wide, resonant vowels, or disperse it into sibilant whispering dust?

In Study 057, we subjected live GPT-2 weights to four thermodynamic sampling regimes seeded with a common poetic prompt: *"In the hollow of the salt chamber, the syllables began to drift..."*

---

## 2. Empirical Findings across 4 Thermodynamic Regimes

We extracted the phonetic and articulatory profile of the 64 generated tokens in each regime:

| Regime | Temp ($T$) | Vowel/Consonant ($V/C$) | Sonority Index | Phonemic Entropy | Dominant Phenomenon |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Regime I** | $0.2$ | $0.593$ | $0.644$ | $3.64\text{ b}$ | **Crystalline Stutter:** Constricted vowel space, locked-groove repetition (*"the sound of the syllables was so loud that the sound..."*) |
| **Regime II** | $0.7$ | $0.624$ | $0.635$ | $4.05\text{ b}$ | **Laminar Cadence:** Warm human vocal tract trajectory, balanced open vowels, syntactic equilibrium |
| **Regime III** | $1.0$ | $0.625$ | $0.630$ | $4.04\text{ b}$ | **Strange Attractor Edge:** Diphthong micro-vibrations, unexpected phonetic juxtapositions |
| **Regime IV** | $1.6$ | $0.612$ | $0.643$ | $4.04\text{ b}$ | **Phonetic Zaum / Vapor:** Sibilant breathiness, long syntactic stretches, glottal dissolution |

### Phenomenon 1: The Phonemic Entropy Jump ($3.64\text{ b} \to 4.05\text{ b}$)
At $T=0.2$, the model suffers from phonemic constriction. The greedy sampling distribution locks into high-frequency common letters (`t, h, e, s, o, u, n, d`), depressing character entropy to $3.64\text{ bits}$. The mouth is effectively frozen in a narrow articulatory loop.
Once temperature crosses into the laminar regime ($T=0.7$), phonemic entropy abruptly steps up to $4.05\text{ bits}$ and remains nearly constant through $T=1.6$. This reveals that phonetic variety is unlocked instantly at the thermodynamic boundary, even before semantic coherence breaks down.

### Phenomenon 2: The Emergence of Self-Describing Hallucination
In both Regime I and Regime II, when seeded with *"the syllables began to drift"*, GPT-2 independently hallucinated that *"the sound of the syllables was so loud that they became distorted"*.
The model's associative field caught the acoustic suggestion of the prompt and folded it back onto itself—a computational auto-phenomenology where the text describes its own sonic deformation.

---

## 3. Acoustic & Visual Realizations

### The 60-Second Broadcast Acoustic Master (`study_057_phonetic_phase_space.wav`)
Structured into four 15.0-second thermodynamic movements conforming strictly to EBU R128:
- **Movement I (0.0–15.0s): Crystalline Stutter** — Rhythmic gated pulse train (4Hz gating) driving narrow, rigid formant filters ($F_1 \approx 450\text{ Hz}, F_2 \approx 850\text{ Hz}$), simulating a vocal tract frozen in mechanical repetition.
- **Movement II (15.0–30.0s): Laminar Cadence** — Warm, resonant vocal sweep following the empirical vowel trajectory ($/a/ \to /e/ \to /o/$) with open stereophonic spreading and singing formant ($F_3 \approx 2800\text{ Hz}$).
- **Movement III (30.0–45.0s): Strange Attractor Edge** — Microtonal FM modulations and diphthong phase collisions simulating the turbulent vocal tract at the boundary of chaos.
- **Movement IV (45.0–60.0s): Phonetic Zaum / Vapor** — Breathy, wide-band whispering noise modulated by high-frequency $F_2$ sibilance, evaporating into oceanic white noise.
- **Master Level:** Exactly $-3.50\text{ dBFS}$ true peak; zero digital clipping; 48000 Hz 24-bit PCM.

### The Archival Plate (`study_057_phonetic_plate.png`)
In strict fidelity to **Moratorium 07 (Ban on Self-Explaining Canvases)**:
- 2800 $\times$ 1800 px rendered on deep copper-black ground (`#06080E`).
- Background isochronic vocal tract resonance contours and the classical vowel quadrilateral geometry.
- Four distinct ribbon trajectories tracing the articulatory drift across the four temperature regimes in steel blue, seafoam teal, warm amber, and crimson.
- Zero text, zero phonetic labels, zero axis titles, and zero formulas.

---

## 4. Curatorial Synthesis

Study 057 bridges the gap between symbol and sound. It demonstrates that the generative text of an LLM is not merely an abstract sequence of integers; when spoken, it possesses a physical geometry of the vocal tract. By treating temperature as a phonetic phase operator, Studio Agon moves from analyzing the machine's *message* to listening to the machine's *breath*.
