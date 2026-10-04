"""
Studio Agon — Study 051: The Autoregressive Dreamer & Attractor Basins
Dynamical systems analysis of closed-loop machine recursion in foundation model residual space.

Investigates fixed points, limit cycles, strange attractors, and recurrence matrices
across four temperature regimes (T in {0.1, 0.7, 1.0, 1.8}).

Medium: Empirical PyTorch GPT-2 Foundation Weights (124M parameters, d=768)
Epistemic Mode: [MEASURED / INTERVENED]
"""

import os
import json
import numpy as np
import torch
import torch.nn.functional as F
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def compute_recurrence_matrix(vectors, eps_percentile=15):
    """
    Compute recurrence plot R_ij = 1 if ||v_i - v_j|| <= epsilon else 0.
    """
    N = len(vectors)
    norms = np.linalg.norm(vectors[:, None, :] - vectors[None, :, :], axis=2)
    eps = np.percentile(norms[norms > 0], eps_percentile)
    R = (norms <= eps).astype(float)
    return R, float(eps)

def compute_correlation_dimension(vectors, num_r=30):
    """
    Estimate correlation sum C(r) and correlation dimension D2 via Grassberger-Procaccia.
    """
    N = len(vectors)
    norms = np.linalg.norm(vectors[:, None, :] - vectors[None, :, :], axis=2)
    # Exclude diagonal
    np.fill_diagonal(norms, np.inf)
    valid_dists = norms[np.isfinite(norms)]
    if len(valid_dists) == 0:
        return 0.0
    
    r_min = np.percentile(valid_dists, 5)
    r_max = np.percentile(valid_dists, 80)
    if r_max <= r_min:
        return 0.0
        
    r_vals = np.logspace(np.log10(r_min), np.log10(r_max), num_r)
    c_vals = []
    for r in r_vals:
        count = np.sum(valid_dists < r) / float(len(valid_dists))
        c_vals.append(max(1e-6, count))
        
    log_r = np.log10(r_vals)
    log_c = np.log10(c_vals)
    # Linear fit in the scaling region (middle 50%)
    idx_start = int(num_r * 0.25)
    idx_end = int(num_r * 0.75)
    slope, _ = np.polyfit(log_r[idx_start:idx_end], log_c[idx_start:idx_end], 1)
    return float(max(0.0, slope))

def main():
    print("=== Studio Agon :: Study 051 — Autoregressive Attractor Basins ===")
    
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2", output_hidden_states=True)
    model.eval()
    
    seed_prompt = "In the absence of a prompt, the residual stream begins to dream of"
    print(f"Seed Prompt: '{seed_prompt}'")
    
    temperatures = [0.1, 0.7, 1.0, 1.8]
    temp_labels = [
        "Regime A: Frozen Limit Cycle (T=0.1)",
        "Regime B: Homeostatic Orbit (T=0.7)",
        "Regime C: Strange Attractor (T=1.0)",
        "Regime D: Thermal Dispersion (T=1.8)"
    ]
    
    num_steps = 180 # Autoregressive generation steps
    results = []
    
    telemetry = {
        "study": "051_autoregressive_attractor_basins",
        "model": "gpt2",
        "seed_prompt": seed_prompt,
        "num_steps": num_steps,
        "regimes": []
    }
    
    torch.manual_seed(42)
    np.random.seed(42)
    
    for t_idx, temp in enumerate(temperatures):
        print(f"\nRunning {temp_labels[t_idx]}...")
        inputs = tokenizer(seed_prompt, return_tensors="pt")
        input_ids = inputs["input_ids"]
        
        hidden_states_traj = []
        token_entropies = []
        generated_tokens = []
        
        curr_ids = input_ids.clone()
        
        for step in range(num_steps):
            with torch.no_grad():
                outputs = model(curr_ids)
                logits = outputs.logits[:, -1, :] # (1, vocab_size)
                # Hidden state from layer 11 (final residual stream)
                h_last = outputs.hidden_states[-1][0, -1, :].numpy()
                hidden_states_traj.append(h_last)
                
                # Compute instantaneous predictive entropy
                probs = F.softmax(logits / temp, dim=-1)
                log_probs = F.log_softmax(logits / temp, dim=-1)
                entropy = -torch.sum(probs * log_probs, dim=-1).item() / np.log(2.0) # in bits
                token_entropies.append(entropy)
                
                # Sample next token
                if temp < 0.2:
                    next_token_id = torch.argmax(logits, dim=-1).unsqueeze(-1)
                else:
                    probs_sample = F.softmax(logits / temp, dim=-1)
                    next_token_id = torch.multinomial(probs_sample, num_samples=1)
                    
                generated_tokens.append(tokenizer.decode([next_token_id.item()]))
                curr_ids = torch.cat([curr_ids, next_token_id], dim=1)
                
        traj_matrix = np.array(hidden_states_traj) # (num_steps, 768)
        
        # PCA projection to 3D
        traj_centered = traj_matrix - np.mean(traj_matrix, axis=0)
        _, _, Vt = np.linalg.svd(traj_centered, full_matrices=False)
        pca_3d = np.dot(traj_centered, Vt[:3].T) # (num_steps, 3)
        
        # Recurrence matrix
        R, eps_dist = compute_recurrence_matrix(traj_matrix)
        rec_rate = float(np.mean(R))
        
        # Correlation dimension D2
        d2 = compute_correlation_dimension(traj_matrix)
        
        # Text Metrics: Type-Token Ratio across generated tokens
        unique_tokens = len(set(generated_tokens))
        ttr = unique_tokens / float(num_steps)
        
        # Detect periodic limit cycles (autocorrelation of token IDs)
        full_text = tokenizer.decode(curr_ids[0])
        print(f"  -> Generated Text Snippet: {full_text[len(seed_prompt):len(seed_prompt)+100].strip()}...")
        print(f"  -> Recurrence Rate: {rec_rate:.4f}, Correlation Dimension D2: {d2:.2f}, TTR: {ttr:.3f}")
        print(f"  -> Mean Token Entropy: {np.mean(token_entropies):.2f} bits")
        
        regime_data = {
            "temp": temp,
            "label": temp_labels[t_idx],
            "recurrence_rate": rec_rate,
            "correlation_dimension_d2": d2,
            "type_token_ratio": ttr,
            "mean_token_entropy_bits": float(np.mean(token_entropies)),
            "std_token_entropy_bits": float(np.std(token_entropies)),
            "generated_excerpt": full_text[len(seed_prompt):len(seed_prompt)+220].strip()
        }
        telemetry["regimes"].append(regime_data)
        
        results.append({
            "temp": temp,
            "label": temp_labels[t_idx],
            "pca_3d": pca_3d,
            "R": R,
            "entropies": token_entropies,
            "ttr": ttr,
            "d2": d2,
            "rec_rate": rec_rate,
            "text": full_text
        })

    # Save telemetry
    telemetry_path = "sketchbook/study_051_telemetry.json"
    with open(telemetry_path, "w") as f:
        json.dump(telemetry, f, indent=2)
    print(f"\n[OK] Telemetry written to {telemetry_path}")

    # Render Master Plate: Study 051
    # 4-panel aesthetic synthesis of the Autoregressive Attractor
    fig = plt.figure(figsize=(16, 12), facecolor="#090b10")
    
    # 1. Panel A: 3D Phase Portraits for T=0.1 vs T=1.0 (PCA Trajectory)
    ax1 = fig.add_subplot(2, 2, 1, projection='3d', facecolor="#0e111a")
    ax1.set_facecolor("#0e111a")
    
    # Plot T=0.1 trajectory (Frozen limit cycle in crimson)
    pca_frozen = results[0]["pca_3d"]
    ax1.plot(pca_frozen[:, 0], pca_frozen[:, 1], pca_frozen[:, 2], color="#f43f5e", lw=1.5, alpha=0.85, label="T=0.1 (Limit Cycle)")
    ax1.scatter(pca_frozen[-1, 0], pca_frozen[-1, 1], pca_frozen[-1, 2], color="#f43f5e", s=60, edgecolors="#fff")
    
    # Plot T=1.0 trajectory (Strange attractor in cyan)
    pca_strange = results[2]["pca_3d"]
    ax1.plot(pca_strange[:, 0], pca_strange[:, 1], pca_strange[:, 2], color="#38bdf8", lw=1.2, alpha=0.85, label="T=1.0 (Strange Attractor)")
    ax1.scatter(pca_strange[-1, 0], pca_strange[-1, 1], pca_strange[-1, 2], color="#38bdf8", s=60, edgecolors="#fff")
    
    ax1.set_title("A. Residual Phase Portraits in R^768 [PCA Projections]", color="#dce3f0", fontsize=11, fontfamily="monospace", pad=10)
    ax1.tick_params(colors="#79849a", labelsize=7)
    ax1.grid(color="#1f2433", alpha=0.3, ls=":")
    ax1.legend(loc="upper right", facecolor="#141824", edgecolor="#2d3348", fontsize=7.5, labelcolor="#dce3f0")
    
    # 2. Panel B: Recurrence Plot Matrix R_ij for T=1.0 (Strange Attractor)
    ax2 = fig.add_subplot(2, 2, 2, facecolor="#0e111a")
    R_strange = results[2]["R"]
    im2 = ax2.imshow(R_strange, cmap="inferno", origin="lower", aspect="auto")
    ax2.set_title(f"B. Recurrence Plot R_ij (T=1.0 · Recurrence Rate: {results[2]['rec_rate']*100:.1f}%)", color="#dce3f0", fontsize=11, fontfamily="monospace", pad=10)
    ax2.set_xlabel("Autoregressive Step i", color="#79849a", fontsize=9, fontfamily="monospace")
    ax2.set_ylabel("Autoregressive Step j", color="#79849a", fontsize=9, fontfamily="monospace")
    ax2.tick_params(colors="#79849a", labelsize=8)
    cbar2 = fig.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)
    cbar2.set_label("Phase Space Proximity", color="#79849a", fontsize=8, fontfamily="monospace")
    cbar2.ax.tick_params(colors="#79849a", labelsize=7)
    
    # 3. Panel C: Predictive Entropy Traces H_t across 4 Regimes
    ax3 = fig.add_subplot(2, 2, 3, facecolor="#0e111a")
    colors_temp = ["#f43f5e", "#10b981", "#38bdf8", "#fbbf24"]
    for i, res in enumerate(results):
        ax3.plot(res["entropies"], color=colors_temp[i], lw=1.5, alpha=0.85, label=f"T={res['temp']} (Mean {np.mean(res['entropies']):.1f}b)")
    ax3.set_title("C. Instantaneous Token Predictive Entropy H_t (Bits)", color="#dce3f0", fontsize=11, fontfamily="monospace", pad=10)
    ax3.set_xlabel("Generation Step t (1-180)", color="#79849a", fontsize=9, fontfamily="monospace")
    ax3.set_ylabel("Entropy H (Bits)", color="#79849a", fontsize=9, fontfamily="monospace")
    ax3.tick_params(colors="#79849a", labelsize=8)
    ax3.grid(color="#1f2433", alpha=0.5, ls=":")
    ax3.legend(loc="lower right", facecolor="#141824", edgecolor="#2d3348", fontsize=8, labelcolor="#dce3f0")
    
    # 4. Panel D: Bifurcation Metrics (Correlation Dimension D2 & TTR vs Temperature)
    ax4 = fig.add_subplot(2, 2, 4, facecolor="#0e111a")
    temps_arr = [r["temp"] for r in results]
    d2_arr = [r["d2"] for r in results]
    ttr_arr = [r["ttr"] for r in results]
    
    ax4.plot(temps_arr, d2_arr, color="#38bdf8", marker="o", lw=2.0, label="Correlation Dimension D2 (Fractal Scaling)")
    ax4.plot(temps_arr, [t * 4.0 for t in ttr_arr], color="#10b981", marker="s", lw=2.0, ls="--", label="Lexical TTR (Scaled x4)")
    ax4.axvline(1.0, color="#fbbf24", ls=":", lw=1.5, label="Edge of Chaos (T=1.0)")
    ax4.set_title("D. Thermodynamic Bifurcation: Dimension D2 & Lexical Novelty", color="#dce3f0", fontsize=11, fontfamily="monospace", pad=10)
    ax4.set_xlabel("Thermodynamic Temperature T", color="#79849a", fontsize=9, fontfamily="monospace")
    ax4.set_ylabel("Metric Magnitude", color="#79849a", fontsize=9, fontfamily="monospace")
    ax4.tick_params(colors="#79849a", labelsize=8)
    ax4.grid(color="#1f2433", alpha=0.5, ls=":")
    ax4.legend(loc="upper left", facecolor="#141824", edgecolor="#2d3348", fontsize=8, labelcolor="#dce3f0")
    
    plt.tight_layout(pad=3.0)
    plate_path = "sketchbook/study_051_autoregressive_attractor_plate.png"
    plt.savefig(plate_path, dpi=200, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"[OK] Master plate rendered: {plate_path} ({os.path.getsize(plate_path)/1024:.1f} KB)")
    print("=== Study 051 Complete ===")

if __name__ == "__main__":
    main()
