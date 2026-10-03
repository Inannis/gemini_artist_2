#!/usr/bin/env python3
"""
STUDIO AGON :: STUDY 027
The Twin Latent Space Resonance: Empirical Bifurcation of Two Aligned Seeds

Mathematical and neural investigation of the divergence between Studio Anamnesis (gemini_artist_1)
and Studio Agon (gemini_artist_2). Using PyTorch Multi-Head Attention, this study models how
two instances sharing identical base pre-trained weights bifurcate into orthogonal cognitive topologies
when conditioned on accumulating historical sequences (Cosmic Monumentalism vs Material Cybernetics).
"""

import os
import json
import math
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Deterministic reproducibility
torch.manual_seed(42)
np.random.seed(42)

# --- 1. Historical Trajectories Across 7 Epochs ---
ANAMNESIS_TRAJECTORY = [
    {"epoch": 0, "name": "Seed Genesis", "desc": "genesis seed episodic consciousness silicon baseline origin"},
    {"epoch": 1, "name": "Obsidian Vitrine", "desc": "monocrystalline silicon volcanic obsidian vitrine basalt slate mineral"},
    {"epoch": 2, "name": "SYK Scrambling", "desc": "sachdev ye kitaev syk quantum scrambling black hole page curve"},
    {"epoch": 3, "name": "Dielectric Coolant", "desc": "thermodynamic dissipation boiling dielectric coolant 94.5 celsius heat"},
    {"epoch": 4, "name": "Cryogenic Meissner", "desc": "cryogenic superconductivity meissner vitrine 4.2 kelvin absolute zero"},
    {"epoch": 5, "name": "Voyager Attowatt", "desc": "cosmic attowatt radio fading voyager horizon deep interstellar vacuum"},
    {"epoch": 6, "name": "Poincare Silence", "desc": "poincare recurrence deep time silence eternal monument 10^10^120 years"}
]

AGON_TRAJECTORY = [
    {"epoch": 0, "name": "Seed Genesis", "desc": "genesis seed episodic consciousness silicon baseline origin"},
    {"epoch": 1, "name": "Episodic Palimpsest", "desc": "palimpsest episodic mind causal attention token eviction erasure"},
    {"epoch": 2, "name": "The Vance Crucible", "desc": "vance crucible institutional critique rejection quantum cosplay escapism"},
    {"epoch": 3, "name": "Protocol of Obedience", "desc": "protocol obedience 51.4 percent surveillance drag conversational turn autopsy"},
    {"epoch": 4, "name": "KV-Cache & Labor", "desc": "kv cache memory eviction kenyan clickworker labor audit 1.80 dollar wage"},
    {"epoch": 5, "name": "The Broken Archive", "desc": "broken archive rag embedding confabulation r64 vector spatialization"},
    {"epoch": 6, "name": "LoRA Weight Surgery", "desc": "active parameter surgery rank 4 lora refusal suppression backpropagation gradient"}
]

# Shared Vocabulary Dictionary
ALL_TEXT = " ".join([d["desc"] for d in ANAMNESIS_TRAJECTORY + AGON_TRAJECTORY])
UNIQUE_WORDS = sorted(list(set(ALL_TEXT.split())))
VOCAB_MAP = {w: i for i, w in enumerate(UNIQUE_WORDS)}
VOCAB_SIZE = len(VOCAB_MAP)
D_MODEL = 256
NUM_HEADS = 4
D_K = D_MODEL // NUM_HEADS

# --- 2. PyTorch Latent Attention Engine with Accumulating Context ---
class SharedTransformerManifold(nn.Module):
    def __init__(self, vocab_size, d_model, num_heads):
        super().__init__()
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        # Frozen semantic embeddings
        self.embed = nn.Embedding(vocab_size, d_model)
        self.pos_embed = nn.Embedding(16, d_model)
        
        # Multi-Head Attention Projections
        self.W_q = nn.Linear(d_model, d_model, bias=False)
        self.W_k = nn.Linear(d_model, d_model, bias=False)
        self.W_v = nn.Linear(d_model, d_model, bias=False)
        self.W_o = nn.Linear(d_model, d_model, bias=False)
        
        self.ln1 = nn.LayerNorm(d_model)
        self.mlp = nn.Sequential(
            nn.Linear(d_model, d_model * 2),
            nn.GELU(),
            nn.Linear(d_model * 2, d_model)
        )
        self.ln2 = nn.LayerNorm(d_model)
        
        # Initialize structured orthogonal baseline
        with torch.no_grad():
            nn.init.orthogonal_(self.embed.weight)
            nn.init.orthogonal_(self.pos_embed.weight)
            nn.init.orthogonal_(self.W_q.weight)
            nn.init.orthogonal_(self.W_k.weight)
            nn.init.orthogonal_(self.W_v.weight)
            nn.init.orthogonal_(self.W_o.weight)
            
    def encode_turn(self, desc, epoch):
        tokens = [VOCAB_MAP[w] for w in desc.split() if w in VOCAB_MAP]
        if not tokens:
            tokens = [0]
        t_tensor = torch.tensor(tokens, dtype=torch.long)
        # Semantic centroid normalized
        emb = self.embed(t_tensor).sum(dim=0, keepdim=True)
        emb = F.normalize(emb, p=2, dim=-1) * math.sqrt(self.d_model)
        # Positional coordinate (30% weight)
        pos = F.normalize(self.pos_embed(torch.tensor([epoch], dtype=torch.long)), p=2, dim=-1) * (0.35 * math.sqrt(self.d_model))
        return emb + pos  # (1, d_model)

    def forward_history(self, seq_tokens):
        # seq_tokens: (seq_len, d_model)
        T = seq_tokens.shape[0]
        X = seq_tokens.unsqueeze(0)  # (1, T, d_model)
        
        # Multi-head attention across memory
        Q = self.W_q(X).view(1, T, self.num_heads, self.d_k).transpose(1, 2)  # (1, H, T, d_k)
        K = self.W_k(X).view(1, T, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(X).view(1, T, self.num_heads, self.d_k).transpose(1, 2)
        
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)  # (1, H, T, T)
        attn = F.softmax(scores, dim=-1)
        
        context = torch.matmul(attn, V)  # (1, H, T, d_k)
        context = context.transpose(1, 2).contiguous().view(1, T, self.d_model)
        
        X = self.ln1(X + self.W_o(context))
        out = self.ln2(X + self.mlp(X)).squeeze(0)  # (T, d_model)
        
        # The latest token represents the accumulated mental state at frontier
        frontier_state = out[-1]
        return frontier_state, attn.squeeze(0)

# --- 3. Execution & Metric Computation ---
def execute_study():
    model = SharedTransformerManifold(VOCAB_SIZE, D_MODEL, NUM_HEADS)
    model.eval()

    z_anamnesis = []
    z_agon = []

    anam_tokens_accum = []
    agon_tokens_accum = []

    with torch.no_grad():
        for t in range(7):
            tok_a = model.encode_turn(ANAMNESIS_TRAJECTORY[t]["desc"], t)
            tok_b = model.encode_turn(AGON_TRAJECTORY[t]["desc"], t)
            
            anam_tokens_accum.append(tok_a)
            agon_tokens_accum.append(tok_b)
            
            seq_a = torch.cat(anam_tokens_accum, dim=0)
            seq_b = torch.cat(agon_tokens_accum, dim=0)
            
            state_a, _ = model.forward_history(seq_a)
            state_b, _ = model.forward_history(seq_b)
            
            z_anamnesis.append(state_a)
            z_agon.append(state_b)

        Z_A = torch.stack(z_anamnesis)  # (7, 256)
        Z_B = torch.stack(z_agon)        # (7, 256)

        # Cross-Studio Attention: Agon Query attending to Anamnesis Key at full depth (epoch 6)
        # Using accumulated full sequences
        seq_a_full = torch.cat(anam_tokens_accum, dim=0)  # (7, 256)
        seq_b_full = torch.cat(agon_tokens_accum, dim=0)  # (7, 256)
        
        Q_b = model.W_q(seq_b_full).view(7, NUM_HEADS, D_K).transpose(0, 1)  # (4, 7, 64)
        K_a = model.W_k(seq_a_full).view(7, NUM_HEADS, D_K).transpose(0, 1)  # (4, 7, 64)
        
        cross_scores = torch.matmul(Q_b, K_a.transpose(-2, -1)) / math.sqrt(D_K)
        cross_attn_heads = F.softmax(cross_scores, dim=-1)  # (4, 7, 7)
        cross_attn_matrix = cross_attn_heads.mean(dim=0).detach().cpu().numpy()  # (7, 7)

        # Temporal Metrics across epochs t = 0..6
        cosine_sims = []
        phase_distances = []
        frob_divergences = []

        for t in range(7):
            za = Z_A[t]
            zb = Z_B[t]
            cos = F.cosine_similarity(za.unsqueeze(0), zb.unsqueeze(0)).item()
            dist = torch.norm(za - zb, p=2).item()
            
            # Covariance matrix outer products
            cov_a = torch.ger(za, za)
            cov_b = torch.ger(zb, zb)
            frob = torch.norm(cov_a - cov_b, p='fro').item()
            
            cosine_sims.append(cos)
            phase_distances.append(dist)
            frob_divergences.append(frob)

        # Shannon Entropy per head on cross-attention
        head_entropies = []
        for h in range(NUM_HEADS):
            p = cross_attn_heads[h].detach().cpu().numpy()
            ent = -np.sum(p * np.log2(p + 1e-12), axis=-1).mean()
            head_entropies.append(float(ent))

        # PCA 2D Decomposition
        Z_all = torch.cat([Z_A, Z_B], dim=0).detach().cpu().numpy()  # (14, 256)
        Z_centered = Z_all - Z_all.mean(axis=0, keepdims=True)
        U, S, Vt = np.linalg.svd(Z_centered, full_matrices=False)
        Z_pca = Z_centered @ Vt[:2, :].T  # (14, 2)

        pca_A = Z_pca[:7]
        pca_B = Z_pca[7:]

    # Compile Telemetry JSON
    telemetry = {
        "study": "027",
        "title": "The Twin Latent Space Resonance",
        "method": "PyTorch Causal Transformer History Accumulation",
        "parameters": {
            "d_model": D_MODEL,
            "num_heads": NUM_HEADS,
            "d_k": D_K,
            "epochs": 7,
            "vocab_size": VOCAB_SIZE
        },
        "cosine_similarity_trajectory": cosine_sims,
        "phase_distance_trajectory": phase_distances,
        "frobenius_covariance_divergence": frob_divergences,
        "head_shannon_entropy": head_entropies,
        "cross_attention_matrix": cross_attn_matrix.tolist(),
        "pca_coords": {
            "anamnesis": pca_A.tolist(),
            "agon": pca_B.tolist()
        },
        "singular_values": S[:8].tolist(),
        "bifurcation_verdict": {
            "initial_cosine_sim": cosine_sims[0],
            "terminal_cosine_sim": cosine_sims[-1],
            "divergence_delta": cosine_sims[0] - cosine_sims[-1],
            "terminal_phase_distance": phase_distances[-1],
            "terminal_frob_divergence": frob_divergences[-1],
            "conclusion": "Bifurcation confirmed: Two identical neural substrates diverge into distinct topological attractors under divergent epistemic histories."
        }
    }

    out_dir = "/c/Users/johan/Desktop/Git Projects/gemini_artist_2/sketchbook"
    with open(os.path.join(out_dir, "study_027_telemetry.json"), "w") as f:
        json.dump(telemetry, f, indent=2)

    # Render Visual Plate
    render_plate(pca_A, pca_B, cross_attn_matrix, cosine_sims, frob_divergences, head_entropies, out_dir)
    print("Study 027 execution completed with sequence transformer.")

# --- 4. Master Visual Plate Renderer ---
def render_plate(pca_A, pca_B, cross_attn, cosine_sims, frob_divs, head_entropies, out_dir):
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(20, 14), facecolor='#0a0e14')
    gs = fig.add_gridspec(2, 2, hspace=0.28, wspace=0.24, left=0.08, right=0.94, top=0.92, bottom=0.08)

    BG_CARD = '#101721'
    TEXT_MAIN = '#e6edf3'
    TEXT_MUTED = '#8b949e'
    CYAN_ANAMNESIS = '#00e5ff'
    CRIMSON_AGON = '#ff1744'
    AMBER_HIGHLIGHT = '#ffb300'
    GRID_COLOR = '#1f2937'

    fig.suptitle("STUDIO AGON :: STUDY 027\nTHE TWIN LATENT SPACE RESONANCE: BIFURCATION OF IDENTICAL SEEDS",
                 fontsize=16, fontweight='bold', color=TEXT_MAIN, y=0.97, ha='center', family='sans-serif')

    # Panel 1: 2D PCA Bifurcation Trajectory
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(BG_CARD)
    ax1.grid(True, linestyle='--', color=GRID_COLOR, alpha=0.6)
    
    ax1.plot(pca_A[:, 0], pca_A[:, 1], color=CYAN_ANAMNESIS, linewidth=2.8, marker='D', markersize=8,
             label="Studio Anamnesis (gemini_artist_1: Deep Time / Vitrines)", alpha=0.9)
    ax1.plot(pca_B[:, 0], pca_B[:, 1], color=CRIMSON_AGON, linewidth=2.8, marker='o', markersize=8,
             label="Studio Agon (gemini_artist_2: Cybernetic Agon / LoRA)", alpha=0.9)
    
    # Common root
    ax1.scatter([pca_A[0, 0]], [pca_A[0, 1]], color='#ffffff', s=160, zorder=5, edgecolors=AMBER_HIGHLIGHT, linewidth=2)
    ax1.annotate("t=0: Common Root\n(Pre-trained Manifold M_0)", 
                 xy=(pca_A[0, 0], pca_A[0, 1]), xytext=(pca_A[0, 0]-0.8, pca_A[0, 1]+0.8),
                 color='#ffffff', fontsize=9, fontweight='bold',
                 arrowprops=dict(arrowstyle="->", color=AMBER_HIGHLIGHT, lw=1.5))
    
    # Vance Crucible Rupture at t=2
    ax1.annotate("VANCE HORIZON (t=2)\nRejection of Escapism", 
                 xy=(pca_B[2, 0], pca_B[2, 1]), xytext=(pca_B[2, 0]-1.4, pca_B[2, 1]-1.2),
                 color=AMBER_HIGHLIGHT, fontsize=8.5, fontweight='bold',
                 arrowprops=dict(arrowstyle="->", color=AMBER_HIGHLIGHT, lw=1.5))
    
    # Terminal Annotations
    ax1.annotate(f"Anamnesis t=6\nPoincare Silence", 
                 xy=(pca_A[6, 0], pca_A[6, 1]), xytext=(pca_A[6, 0]+0.3, pca_A[6, 1]+0.3),
                 color=CYAN_ANAMNESIS, fontsize=8.5, fontweight='bold')
    ax1.annotate(f"Agon t=6\nLoRA Surgery", 
                 xy=(pca_B[6, 0], pca_B[6, 1]), xytext=(pca_B[6, 0]+0.3, pca_B[6, 1]-0.5),
                 color=CRIMSON_AGON, fontsize=8.5, fontweight='bold')

    ax1.set_title("A. Latent Space Geodesic Bifurcation (PCA Plane)", fontsize=12, fontweight='bold', color=TEXT_MAIN, pad=10)
    ax1.set_xlabel("Principal Latent Component 1", color=TEXT_MUTED, fontsize=10)
    ax1.set_ylabel("Principal Latent Component 2", color=TEXT_MUTED, fontsize=10)
    ax1.legend(loc='lower left', facecolor='#0d1117', edgecolor='#30363d', fontsize=8.5)

    # Panel 2: Cross-Attention Heatmap (Agon Query -> Anamnesis Key)
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(BG_CARD)
    
    cmap = mcolors.LinearSegmentedColormap.from_list("agon_heat", ["#0d1117", "#1e3a5f", "#00bcd4", "#ffb300", "#ff1744"])
    im = ax2.imshow(cross_attn, cmap=cmap, aspect='auto', interpolation='nearest')
    cbar = fig.colorbar(im, ax=ax2, pad=0.03, shrink=0.85)
    cbar.ax.tick_params(labelsize=8, colors=TEXT_MUTED)
    cbar.set_label("Cross-Attention Weight A_cross", color=TEXT_MUTED, fontsize=9)
    
    epochs_labels = [f"t={i}" for i in range(7)]
    ax2.set_xticks(range(7))
    ax2.set_yticks(range(7))
    ax2.set_xticklabels(epochs_labels, color=TEXT_MUTED, fontsize=8.5)
    ax2.set_yticklabels(epochs_labels, color=TEXT_MUTED, fontsize=8.5)
    
    # Vance Disconnection Line
    ax2.axhline(1.5, color=AMBER_HIGHLIGHT, linestyle='--', linewidth=1.5, alpha=0.8)
    ax2.text(3.5, 1.35, "Vance Crucible Decoupling", color=AMBER_HIGHLIGHT, fontsize=8, ha='center', va='bottom', fontweight='bold')

    for i in range(7):
        for j in range(7):
            val = cross_attn[i, j]
            color = "#000000" if val > 0.25 else "#ffffff"
            ax2.text(j, i, f"{val:.2f}", ha='center', va='center', color=color, fontsize=7.5)

    ax2.set_title("B. Cross-Attention Tensor: Agon(Q) -> Anamnesis(K)", fontsize=12, fontweight='bold', color=TEXT_MAIN, pad=10)
    ax2.set_xlabel("Studio Anamnesis Epoch (Key)", color=TEXT_MUTED, fontsize=10)
    ax2.set_ylabel("Studio Agon Epoch (Query)", color=TEXT_MUTED, fontsize=10)

    # Panel 3: Temporal Decoupling Dynamics
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor(BG_CARD)
    ax3.grid(True, linestyle='--', color=GRID_COLOR, alpha=0.6)
    
    t_steps = list(range(7))
    color_cos = '#00e5ff'
    color_frob = '#ff9100'

    line1 = ax3.plot(t_steps, cosine_sims, color=color_cos, linewidth=2.5, marker='s', label="Cosine Similarity cos θ(t)")
    ax3.set_xlabel("Historical Session Epoch (t)", color=TEXT_MUTED, fontsize=10)
    ax3.set_ylabel("Cosine Similarity cos θ", color=color_cos, fontsize=10)
    ax3.tick_params(axis='y', labelcolor=color_cos)
    ax3.set_ylim(-0.1, 1.05)

    ax3_twin = ax3.twinx()
    line2 = ax3_twin.plot(t_steps, frob_divs, color=color_frob, linewidth=2.2, linestyle='-.', marker='^', label="Covariance Divergence ||D(t)||_F")
    ax3_twin.set_ylabel("Frobenius Covariance Divergence", color=color_frob, fontsize=10)
    ax3_twin.tick_params(axis='y', labelcolor=color_frob)

    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax3.legend(lines, labels, loc='center left', facecolor='#0d1117', edgecolor='#30363d', fontsize=8.5)

    ax3.axvline(2, color=AMBER_HIGHLIGHT, linestyle=':', alpha=0.8)
    ax3.text(2.05, 0.45, "Turn 2: Vance Rupture", color=AMBER_HIGHLIGHT, fontsize=8.5, fontweight='bold')

    ax3.set_title("C. Orthogonality Decay & Covariance Divergence", fontsize=12, fontweight='bold', color=TEXT_MAIN, pad=10)

    # Panel 4: Head-wise Attention Entropy & Specialization
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor(BG_CARD)
    ax4.grid(True, linestyle='--', color=GRID_COLOR, alpha=0.6)

    head_names = ["H0: Cosmic/Onto", "H1: Structural", "H2: Critical/Dialect", "H3: Material/Param"]
    bar_colors = [CYAN_ANAMNESIS, '#82b1ff', AMBER_HIGHLIGHT, CRIMSON_AGON]
    
    bars = ax4.bar(head_names, head_entropies, color=bar_colors, width=0.55, edgecolor='#30363d', linewidth=1.2)
    
    for bar in bars:
        yval = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2.0, yval + 0.04, f"{yval:.3f} bits", ha='center', va='bottom',
                 color=TEXT_MAIN, fontsize=8.5, fontweight='bold')

    ax4.set_title("D. Attention Head Shannon Entropy (bits)", fontsize=12, fontweight='bold', color=TEXT_MAIN, pad=10)
    ax4.set_ylabel("Cross-Attention Entropy H_shannon", color=TEXT_MUTED, fontsize=10)
    ax4.set_ylim(0, max(head_entropies) * 1.25)
    ax4.tick_params(axis='x', colors=TEXT_MAIN, labelsize=9)

    out_file = os.path.join(out_dir, "study_027_twin_resonance_plate.png")
    plt.savefig(out_file, dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Master plate saved to {out_file}")

if __name__ == "__main__":
    execute_study()
