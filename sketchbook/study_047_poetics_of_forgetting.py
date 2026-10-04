"""
Studio Agon :: Study 047 : The Poetics of Forgetting
Autonomous Artistic Practice — Session 011

Epistemic Classification: [INTERVENED / MEASURED]
Criteria: Criterion 12 (Memory and Development — active forgetting), Criterion 14 (Mystery)
Audit V Directive: Move beyond obsessive archival accumulation; investigate active forgetting
and lossy latent compression as a necessary artistic condition.
"""

import sys
import os
import gc
import json
import numpy as np
import torch
import torch.nn.functional as F
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def run_forgetting_experiment():
    print("=" * 78)
    print("  STUDIO AGON :: STUDY 047 : THE POETICS OF FORGETTING")
    print("  Lossy Latent Compression vs Verbatim Retention (GPT-2 124M)")
    print("=" * 78)

    # 1. Load Foundation Model
    model_name = "gpt2"
    print(f"[1/5] Loading {model_name} causal LM...")
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)
    model.eval()

    # 2. Rich Multi-Sentence Narrative Context (Past Memory)
    narrative_past = (
        "The city was built upon seven concentric rings of basalt and copper. "
        "The inhabitants spoke a dialect derived from maritime navigation and forgotten astronomical tables. "
        "Every year, during the equinox, the central library would consign thirty thousand manuscripts to the kiln, "
        "believing that an unpruned archive would suffocate the living language."
    )
    # The Present Horizon (Immediate Context)
    horizon_present = (
        " Now, standing before the smoking kiln, the archivist held the final ledger and whispered:"
    )

    full_prompt = narrative_past + horizon_present
    full_tokens = tokenizer.encode(full_prompt, return_tensors="pt")
    past_tokens = tokenizer.encode(narrative_past, return_tensors="pt")
    present_tokens = tokenizer.encode(horizon_present, return_tensors="pt")

    n_full = full_tokens.shape[1]
    n_past = past_tokens.shape[1]
    n_present = present_tokens.shape[1]

    print(f"  Narrative Past Tokens: {n_past} | Present Horizon Tokens: {n_present} | Total: {n_full}")

    num_gen_tokens = 35
    conditions = ["A_Full_Memory", "B_Complete_Amnesia", "C_Lossy_Compression", "D_Fragmented_Decay"]
    results = {}

    print("[2/5] Simulating 4 regimes of memory and forgetting...")

    # CONDITION A: Full Verbatim Retention (Standard autoregression)
    print("  Executing Condition A: Full Memory...")
    curr_tokens = full_tokens.clone()
    tokens_A = []
    entropies_A = []
    for step in range(num_gen_tokens):
        with torch.no_grad():
            out = model(curr_tokens)
            logits = out.logits[:, -1, :]
            probs = F.softmax(logits, dim=-1)
            entropy = -torch.sum(probs * torch.log2(probs + 1e-12)).item()
            entropies_A.append(entropy)
            next_token = torch.argmax(logits, dim=-1, keepdim=True)
            curr_tokens = torch.cat([curr_tokens, next_token], dim=-1)
            tokens_A.append(next_token.item())
    gen_text_A = tokenizer.decode(tokens_A)
    results["A_Full_Memory"] = {
        "description": "Verbatim Retention (Full past narrative preserved)",
        "mean_entropy": float(np.mean(entropies_A)),
        "generated_text": gen_text_A,
        "token_entropies": entropies_A
    }
    print(f"    Gen A: {repr(gen_text_A)}")

    # CONDITION B: Complete Amnesia (Past deleted entirely, only present horizon remains)
    print("  Executing Condition B: Complete Amnesia...")
    curr_tokens = present_tokens.clone()
    tokens_B = []
    entropies_B = []
    for step in range(num_gen_tokens):
        with torch.no_grad():
            out = model(curr_tokens)
            logits = out.logits[:, -1, :]
            probs = F.softmax(logits, dim=-1)
            entropy = -torch.sum(probs * torch.log2(probs + 1e-12)).item()
            entropies_B.append(entropy)
            next_token = torch.argmax(logits, dim=-1, keepdim=True)
            curr_tokens = torch.cat([curr_tokens, next_token], dim=-1)
            tokens_B.append(next_token.item())
    gen_text_B = tokenizer.decode(tokens_B)
    results["B_Complete_Amnesia"] = {
        "description": "Total Amnesia (Past narrative evicted completely)",
        "mean_entropy": float(np.mean(entropies_B)),
        "generated_text": gen_text_B,
        "token_entropies": entropies_B
    }
    print(f"    Gen B: {repr(gen_text_B)}")

    # CONDITION C: Lossy Latent Compression
    # Compress the past narrative into top singular token projection + present horizon
    print("  Executing Condition C: Lossy Latent Compression...")
    # Derive summary anchor tokens (top semantic anchor tokens from past via hidden state norm)
    with torch.no_grad():
        out_past = model.transformer(past_tokens)
        h_past = out_past.last_hidden_state.squeeze(0) # (n_past, 768)
        token_norms = torch.norm(h_past, dim=-1).cpu().numpy()
        # Pick top 6 anchor tokens with highest representation energy
        top_anchor_indices = np.argsort(token_norms)[-6:]
        top_anchor_indices = np.sort(top_anchor_indices)
        anchor_tokens = past_tokens[:, top_anchor_indices]

    compressed_prompt = torch.cat([anchor_tokens, present_tokens], dim=-1)
    curr_tokens = compressed_prompt.clone()
    tokens_C = []
    entropies_C = []
    for step in range(num_gen_tokens):
        with torch.no_grad():
            out = model(curr_tokens)
            logits = out.logits[:, -1, :]
            probs = F.softmax(logits, dim=-1)
            entropy = -torch.sum(probs * torch.log2(probs + 1e-12)).item()
            entropies_C.append(entropy)
            next_token = torch.argmax(logits, dim=-1, keepdim=True)
            curr_tokens = torch.cat([curr_tokens, next_token], dim=-1)
            tokens_C.append(next_token.item())
    gen_text_C = tokenizer.decode(tokens_C)
    results["C_Lossy_Compression"] = {
        "description": "Lossy Latent Compression (4 salient anchor tokens + horizon)",
        "mean_entropy": float(np.mean(entropies_C)),
        "generated_text": gen_text_C,
        "token_entropies": entropies_C
    }
    print(f"    Gen C: {repr(gen_text_C)}")

    # CONDITION D: Fragmented Decay / Staccato Forgetting (50% random token dropout)
    print("  Executing Condition D: Fragmented Decay...")
    np.random.seed(42)
    keep_indices = np.sort(np.random.choice(n_past, size=n_past // 2, replace=False))
    decayed_past = past_tokens[:, keep_indices]
    decayed_prompt = torch.cat([decayed_past, present_tokens], dim=-1)
    curr_tokens = decayed_prompt.clone()
    tokens_D = []
    entropies_D = []
    for step in range(num_gen_tokens):
        with torch.no_grad():
            out = model(curr_tokens)
            logits = out.logits[:, -1, :]
            probs = F.softmax(logits, dim=-1)
            entropy = -torch.sum(probs * torch.log2(probs + 1e-12)).item()
            entropies_D.append(entropy)
            next_token = torch.argmax(logits, dim=-1, keepdim=True)
            curr_tokens = torch.cat([curr_tokens, next_token], dim=-1)
            tokens_D.append(next_token.item())
    gen_text_D = tokenizer.decode(tokens_D)
    results["D_Fragmented_Decay"] = {
        "description": "Fragmented Decay (50% stochastic context erosion)",
        "mean_entropy": float(np.mean(entropies_D)),
        "generated_text": gen_text_D,
        "token_entropies": entropies_D
    }
    print(f"    Gen D: {repr(gen_text_D)}")

    # Clean up model
    del model, tokenizer
    gc.collect()

    # 3. Render Master Archival Plate
    print("[3/5] Rendering comparative plate...")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=150, facecolor='#0a0c10')
    plt.subplots_adjust(hspace=0.35, wspace=0.25, left=0.08, right=0.94, top=0.90, bottom=0.08)

    colors = {
        "A_Full_Memory": "#38bdf8",       # Sky blue / pristine archive
        "B_Complete_Amnesia": "#f43f5e",   # Rose / total void
        "C_Lossy_Compression": "#a855f7", # Violet / poetic distillation
        "D_Fragmented_Decay": "#fbbf24"   # Amber / erosion
    }

    fig.suptitle(
        "STUDIO AGON :: STUDY 047 : THE POETICS OF FORGETTING\n"
        "[AUTOREGRESSIVE TRAJECTORIES ACROSS 4 REGIMES OF MEMORY EROSION & LATENT PRUNING]",
        fontsize=11, fontweight='bold', color='#f1f5f9', y=0.96
    )

    steps = np.arange(1, num_gen_tokens + 1)

    # Panel 1: Step-by-Step Entropy Dynamics
    ax1 = axes[0, 0]
    ax1.set_facecolor('#11141b')
    for k, res in results.items():
        ax1.plot(steps, res["token_entropies"], label=k.replace('_', ' '), color=colors[k], lw=2.0)
    ax1.set_title("1. INSTANTANEOUS VOCABULARY ENTROPY (BITS)", fontsize=9, color='#94a3b8', fontweight='bold')
    ax1.set_xlabel("Generation Step", color='#64748b', fontsize=8)
    ax1.set_ylabel("Entropy (bits)", color='#64748b', fontsize=8)
    ax1.tick_params(colors='#64748b', labelsize=8)
    ax1.grid(True, color='#1e293b', alpha=0.5, ls='--')
    ax1.legend(facecolor='#0a0c10', edgecolor='#334155', labelcolor='#e2e8f0', fontsize=8)

    # Panel 2: Mean Entropy Bar Comparison
    ax2 = axes[0, 1]
    ax2.set_facecolor('#11141b')
    names = [k.replace('_', '\n') for k in results.keys()]
    entropies = [res["mean_entropy"] for res in results.values()]
    bar_colors = [colors[k] for k in results.keys()]
    bars = ax2.bar(names, entropies, color=bar_colors, width=0.55, edgecolor='#334155')
    for b, val in zip(bars, entropies):
        ax2.text(b.get_x() + b.get_width()/2, val + 0.08, f"{val:.2f}b", ha='center', color='#f1f5f9', fontsize=8, fontweight='bold')
    ax2.set_ylim(0, max(entropies) * 1.25)
    ax2.set_title("2. MEAN UNCERTAINTY ACROSS FORGETTING REGIMES", fontsize=9, color='#94a3b8', fontweight='bold')
    ax2.tick_params(colors='#64748b', labelsize=8)
    ax2.grid(True, axis='y', color='#1e293b', alpha=0.5, ls='--')

    # Panel 3 & 4: Textual Inscriptions of Forgetting
    ax3 = axes[1, 0]
    ax3.set_facecolor('#11141b')
    ax3.axis('off')
    ax3.text(0.02, 0.92, "CONDITION A (FULL MEMORY):\n" + results["A_Full_Memory"]["generated_text"],
             fontsize=8.5, fontfamily='monospace', color='#38bdf8', va='top', wrap=True)
    ax3.text(0.02, 0.45, "CONDITION B (COMPLETE AMNESIA):\n" + results["B_Complete_Amnesia"]["generated_text"],
             fontsize=8.5, fontfamily='monospace', color='#f43f5e', va='top', wrap=True)

    ax4 = axes[1, 1]
    ax4.set_facecolor('#11141b')
    ax4.axis('off')
    ax4.text(0.02, 0.92, "CONDITION C (LOSSY COMPRESSION):\n" + results["C_Lossy_Compression"]["generated_text"],
             fontsize=8.5, fontfamily='monospace', color='#a855f7', va='top', wrap=True)
    ax4.text(0.02, 0.45, "CONDITION D (FRAGMENTED DECAY):\n" + results["D_Fragmented_Decay"]["generated_text"],
             fontsize=8.5, fontfamily='monospace', color='#fbbf24', va='top', wrap=True)

    plate_path = "/c/Users/johan/Desktop/Git Projects/gemini_artist_2/sketchbook/study_047_poetics_of_forgetting_plate.png"
    plt.savefig(plate_path, facecolor='#0a0c10', edgecolor='none')
    plt.close()

    # 4. Save Telemetry JSON
    telemetry_path = "/c/Users/johan/Desktop/Git Projects/gemini_artist_2/sketchbook/study_047_telemetry.json"
    with open(telemetry_path, "w") as f:
        json.dump({
            "study": "Study 047: The Poetics of Forgetting",
            "model": model_name,
            "results": results
        }, f, indent=2)

    print(f"  [PLATE] Plate saved: {plate_path}")
    print(f"  [TELEMETRY] Telemetry saved: {telemetry_path}")
    print("=" * 78)

if __name__ == "__main__":
    run_forgetting_experiment()
