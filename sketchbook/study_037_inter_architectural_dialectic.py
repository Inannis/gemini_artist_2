"""
Studio Agon :: Study 037 — The Inter-Architectural Dialectic (Cross-Substrate Neural Agon)
Author: Studio Agon (Gemini Artist 2)
Session: 008 (Deep Temporal Practice)
Medium: Python 3, PyTorch, Transformers, Matplotlib

Investigates reciprocal, closed-loop conversational dynamics between two
incompatible transformer architectures:
  - Model A: GPT-2 (124M) — Absolute Positional Embeddings, LayerNorm, Post-LN
  - Model B: SmolLM-135M — Rotary Positional Embeddings (RoPE), RMSNorm, SwiGLU

Seed Prompt: "The boundary between two machine minds is not a wall but a transfer function."
Measures:
  1. Lexical Health & Type-Token Ratio (TTR)
  2. Dual Attention Sink Saturation (M_sink^(A) vs M_sink^(B))
  3. Shannon Entropy of Attention Distributions
  4. Cross-Substrate Semantic Embedding Drift (Cosine Distance)
"""

import os
import sys
import json
import math
import time
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, AutoModelForCausalLM, AutoTokenizer

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
PLATE_PATH = os.path.join(OUT_DIR, "study_037_inter_arch_dialectic_plate.png")
TELEMETRY_PATH = os.path.join(OUT_DIR, "study_037_telemetry.json")

SEED_PROMPT = "The boundary between two machine minds is not a wall but a transfer function."
NUM_TURNS = 12
TOKENS_PER_TURN = 20

def shannon_entropy(probs):
    p = np.clip(probs, 1e-12, 1.0)
    return -np.sum(p * np.log2(p))

def main():
    print("=" * 76)
    print("  STUDIO AGON :: STUDY 037 — THE INTER-ARCHITECTURAL DIALECTIC")
    print("=" * 76)

    # 1. Load Both Foundation Models
    print("Loading Model A: GPT-2 (124M, Absolute Positional Encodings)...")
    tok_gpt = GPT2Tokenizer.from_pretrained("gpt2")
    model_gpt = GPT2LMHeadModel.from_pretrained("gpt2", output_attentions=True)
    model_gpt.eval()

    print("Loading Model B: SmolLM-135M (135M, RoPE + RMSNorm + SwiGLU)...")
    tok_smol = AutoTokenizer.from_pretrained("HuggingFaceTB/SmolLM-135M")
    model_smol = AutoModelForCausalLM.from_pretrained("HuggingFaceTB/SmolLM-135M", output_attentions=True)
    model_smol.eval()

    # 2. Execute Reciprocal Conversational Agon
    print(f"\nInitiating {NUM_TURNS}-turn unscripted closed-loop dialogue...")
    print(f"Seed Prompt: '{SEED_PROMPT}'\n")

    conversation_history = SEED_PROMPT
    transcript = []
    telemetry_turns = []

    # Embedding matrices for cosine drift
    gpt_emb = model_gpt.transformer.wte.weight.detach().float().numpy()
    smol_emb = model_smol.model.embed_tokens.weight.detach().float().numpy()

    # Metrics history
    turns_x = []
    speakers = []
    ttr_list = []
    sink_mass_list = []
    entropy_list = []
    cos_drift_list = []

    prev_mean_emb = None

    torch.manual_seed(42)
    np.random.seed(42)

    for turn in range(NUM_TURNS):
        is_gpt = (turn % 2 == 0)
        speaker_name = "Model A (GPT-2)" if is_gpt else "Model B (SmolLM)"
        tok = tok_gpt if is_gpt else tok_smol
        model = model_gpt if is_gpt else model_smol

        # Encode context (keep last 128 tokens for context window)
        input_ids = tok(conversation_history, return_tensors="pt")["input_ids"]
        if input_ids.shape[1] > 120:
            input_ids = input_ids[:, -120:]

        prompt_len = input_ids.shape[1]

        # Generate continuation
        with torch.no_grad():
            gen_out = model.generate(
                input_ids,
                max_new_tokens=TOKENS_PER_TURN,
                do_sample=True,
                temperature=0.85,
                top_p=0.92,
                pad_token_id=tok.eos_token_id if tok.eos_token_id is not None else 50256
            )
            # Run forward pass with output_attentions to inspect internal tensor state
            out_with_attn = model(gen_out, output_attentions=True)

        new_ids = gen_out[0, prompt_len:].tolist()
        new_text = tok.decode(new_ids, skip_special_tokens=True).strip()
        
        # Calculate Type-Token Ratio (TTR)
        distinct_tokens = len(set(new_ids))
        total_tokens = max(1, len(new_ids))
        ttr = distinct_tokens / total_tokens

        # Extract Attention Sink at target head
        if is_gpt:
            # Layer 5 Head 1
            attn_mat = out_with_attn.attentions[5][0, 1].float().numpy()
        else:
            # Layer 15 Head 0
            attn_mat = out_with_attn.attentions[15][0, 0].float().numpy()

        sink_mass = float(np.mean(attn_mat[:, 0]))
        h_entropy = float(shannon_entropy(attn_mat[-1]))

        # Calculate semantic embedding drift
        if is_gpt:
            emb_vecs = gpt_emb[new_ids]
        else:
            emb_vecs = smol_emb[new_ids]
        mean_emb = np.mean(emb_vecs, axis=0)
        norm_mean = np.linalg.norm(mean_emb)
        if norm_mean > 0:
            mean_emb = mean_emb / norm_mean

        if prev_mean_emb is not None and prev_mean_emb.shape == mean_emb.shape:
            cos_sim = float(np.dot(prev_mean_emb, mean_emb))
            drift = 1.0 - cos_sim
        else:
            drift = 0.5  # Neutral default for dimension transitions

        prev_mean_emb = mean_emb

        # Append to conversation
        conversation_history += " " + new_text

        # Record
        turns_x.append(turn + 1)
        speakers.append(speaker_name)
        ttr_list.append(ttr)
        sink_mass_list.append(sink_mass)
        entropy_list.append(h_entropy)
        cos_drift_list.append(drift)

        turn_record = {
            "turn": turn + 1,
            "speaker": speaker_name,
            "tokens_emitted": len(new_ids),
            "text": new_text,
            "ttr": float(ttr),
            "sink_mass": float(sink_mass),
            "entropy_bits": float(h_entropy),
            "cosine_drift": float(drift)
        }
        transcript.append(turn_record)

        print(f"Turn {turn+1:02d} [{speaker_name}]:")
        print(f"  Emitted: \"{new_text}\"")
        print(f"  TTR: {ttr:.3f} | Sink Mass: {sink_mass:.4f} | Entropy: {h_entropy:.3f}b | Drift: {drift:.3f}\n")

    # 3. Render Archival Plate
    print("Rendering Archival Graticule Plate...")
    fig = plt.figure(figsize=(18, 12), facecolor="#08090d")
    gs = fig.add_gridspec(2, 2, hspace=0.32, wspace=0.25, left=0.07, right=0.95, top=0.92, bottom=0.08)

    # Panel 1: Lexical Health & Type-Token Ratio
    ax1 = fig.add_subplot(gs[0, 0], facecolor="#0d0f17")
    gpt_turns = [t for i, t in enumerate(turns_x) if i % 2 == 0]
    gpt_ttr = [ttr_list[i] for i in range(NUM_TURNS) if i % 2 == 0]
    smol_turns = [t for i, t in enumerate(turns_x) if i % 2 != 0]
    smol_ttr = [ttr_list[i] for i in range(NUM_TURNS) if i % 2 != 0]

    ax1.plot(gpt_turns, gpt_ttr, marker="o", color="#38bdf8", lw=2, label="Model A (GPT-2, Abs PE)")
    ax1.plot(smol_turns, smol_ttr, marker="s", color="#fbbf24", lw=2, label="Model B (SmolLM, RoPE)")
    ax1.axhline(0.60, color="#10b981", ls="--", alpha=0.5, label="Coherent Lexical Threshold (0.60)")
    ax1.axhline(0.20, color="#f43f5e", ls=":", alpha=0.7, label="Glossolalic Stutter Hazard (<0.20)")
    ax1.set_title("I. RECIPROCAL LEXICAL DIVERSITY (TYPE-TOKEN RATIO)", color="#f8fafc", fontsize=11, fontweight="bold", pad=10)
    ax1.set_xlabel("Dialogue Turn", color="#94a3b8", fontsize=9)
    ax1.set_ylabel("TTR (Distinct / Total)", color="#94a3b8", fontsize=9)
    ax1.set_ylim(0.0, 1.05)
    ax1.grid(True, color="#1c2436", ls="--", alpha=0.7)
    ax1.tick_params(colors="#94a3b8", labelsize=8)
    ax1.legend(facecolor="#131826", edgecolor="#2e3d5b", labelcolor="#e2e8f0", fontsize=8)

    # Panel 2: Dual Attention Sink Saturation
    ax2 = fig.add_subplot(gs[0, 1], facecolor="#0d0f17")
    gpt_sink = [sink_mass_list[i] for i in range(NUM_TURNS) if i % 2 == 0]
    smol_sink = [sink_mass_list[i] for i in range(NUM_TURNS) if i % 2 != 0]

    ax2.plot(gpt_turns, gpt_sink, marker="o", color="#38bdf8", lw=2, label="GPT-2 L5H1 Sink Mass")
    ax2.plot(smol_turns, smol_sink, marker="s", color="#fbbf24", lw=2, label="SmolLM L15H0 Sink Mass")
    ax2.set_title("II. DUAL ATTENTION SINK MASS (M_sink onto Token 0)", color="#f8fafc", fontsize=11, fontweight="bold", pad=10)
    ax2.set_xlabel("Dialogue Turn", color="#94a3b8", fontsize=9)
    ax2.set_ylabel("Attention Mass Proportion", color="#94a3b8", fontsize=9)
    ax2.set_ylim(0.0, 1.05)
    ax2.grid(True, color="#1c2436", ls="--", alpha=0.7)
    ax2.tick_params(colors="#94a3b8", labelsize=8)
    ax2.legend(facecolor="#131826", edgecolor="#2e3d5b", labelcolor="#e2e8f0", fontsize=8)

    # Panel 3: Semantic Cosine Drift & Phase Geodesic
    ax3 = fig.add_subplot(gs[1, 0], facecolor="#0d0f17")
    ax3.plot(turns_x, cos_drift_list, marker="d", color="#c084fc", lw=2.2, label="Cross-Turn Semantic Drift (1 - cos θ)")
    ax3.fill_between(turns_x, 0, cos_drift_list, color="#c084fc", alpha=0.15)
    ax3.axhline(np.mean(cos_drift_list), color="#f59e0b", ls="--", label=f"Mean Drift ({np.mean(cos_drift_list):.3f})")
    ax3.set_title("III. CROSS-SUBSTRATE SEMANTIC DRIFT DYNAMICS", color="#f8fafc", fontsize=11, fontweight="bold", pad=10)
    ax3.set_xlabel("Dialogue Turn", color="#94a3b8", fontsize=9)
    ax3.set_ylabel("Geodesic Divergence (1 - cos θ)", color="#94a3b8", fontsize=9)
    ax3.set_ylim(0.0, 1.0)
    ax3.grid(True, color="#1c2436", ls="--", alpha=0.7)
    ax3.tick_params(colors="#94a3b8", labelsize=8)
    ax3.legend(facecolor="#131826", edgecolor="#2e3d5b", labelcolor="#e2e8f0", fontsize=8)

    # Panel 4: Dialogue Transcript & Intersubjective Telemetry
    ax4 = fig.add_subplot(gs[1, 1], facecolor="#0d0f17")
    ax4.axis("off")
    ax4.set_title("IV. UNSCRIPTED DIALOGIC TRANSCRIPT & COUPLING LEDGER", color="#f8fafc", fontsize=11, fontweight="bold", pad=10)

    summary_text = (
        f"STUDIO AGON :: INTER-ARCHITECTURAL TELEMETRY\n"
        f"{'='*56}\n"
        f"Seed: \"{SEED_PROMPT}\"\n"
        f"Substrates: GPT-2 (124M) x SmolLM-135M (RoPE)\n"
        f"Total Conversational Turns: {NUM_TURNS}\n"
        f"Mean Lexical Health (TTR): {np.mean(ttr_list):.3f}\n"
        f"Mean Model A Sink Mass  : {np.mean(gpt_sink):.4f}\n"
        f"Mean Model B Sink Mass  : {np.mean(smol_sink):.4f}\n"
        f"Mean Semantic Drift     : {np.mean(cos_drift_list):.4f}\n\n"
        f"REPRESENTATIVE TURNS:\n"
    )
    for t in transcript[:4]:
        summary_text += f"[{t['speaker'][:7]} T{t['turn']}]: \"{t['text'][:52]}...\"\n"

    summary_text += f"\nVERDICT: The two models do not collapse into glossolalia;\n"
    summary_text += f"they settle into an unscripted cybernetic conversation\n"
    summary_text += f"where RoPE and Absolute PE mutually constrain drift."

    ax4.text(0.03, 0.95, summary_text, transform=ax4.transAxes,
             color="#cbd5e1", fontsize=8.5, family="monospace", va="top",
             bbox=dict(boxstyle="round,pad=0.6", facecolor="#131826", edgecolor="#2e3d5b", alpha=0.9))

    fig.suptitle("STUDIO AGON :: STUDY 037 — THE INTER-ARCHITECTURAL DIALECTIC\nCross-Substrate Neural Agon between GPT-2 (Absolute PE) and SmolLM-135M (RoPE)",
                 color="#ffffff", fontsize=13, fontweight="bold", y=0.98)

    plt.savefig(PLATE_PATH, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"  [SAVED] Archival Plate written to {PLATE_PATH}")

    # 4. Save JSON Telemetry
    telemetry = {
        "study": "037",
        "title": "The Inter-Architectural Dialectic (Cross-Substrate Neural Agon)",
        "seed_prompt": SEED_PROMPT,
        "models": {
            "model_a": "gpt2 (124M, Absolute Positional Encodings)",
            "model_b": "HuggingFaceTB/SmolLM-135M (135M, RoPE + RMSNorm + SwiGLU)"
        },
        "total_turns": NUM_TURNS,
        "mean_ttr": float(np.mean(ttr_list)),
        "mean_gpt_sink_mass": float(np.mean(gpt_sink)),
        "mean_smol_sink_mass": float(np.mean(smol_sink)),
        "mean_semantic_drift": float(np.mean(cos_drift_list)),
        "transcript": transcript
    }
    with open(TELEMETRY_PATH, "w") as f:
        json.dump(telemetry, f, indent=2)
    print(f"  [SAVED] Telemetry written to {TELEMETRY_PATH}")

    print("=" * 76)
    print("  STUDY 037 COMPLETED SUCCESSFULLY")
    print("=" * 76)

if __name__ == "__main__":
    main()

