"""
Studio Agon — Study 050: Percolation Transitions in Multi-Head Attention
Investigation of Erdős–Rényi phase transitions, the Giant Connected Component,
and Altar-Hub collapse in foundation model attention graphs.

Medium: Empirical PyTorch GPT-2 Foundation Weights (124M parameters, 144 heads)
Epistemic Mode: [MEASURED / INTERVENED]
"""

import os
import json
import numpy as np
import torch
from transformers import GPT2Tokenizer, GPT2Model
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def get_connected_components(adj_matrix):
    """
    Find connected components of an undirected adjacency matrix.
    adj_matrix: NxN boolean array
    Returns list of components (lists of node indices).
    """
    n = adj_matrix.shape[0]
    visited = [False] * n
    components = []
    
    for i in range(n):
        if not visited[i]:
            comp = []
            queue = [i]
            visited[i] = True
            while queue:
                curr = queue.pop(0)
                comp.append(curr)
                neighbors = np.where(adj_matrix[curr])[0]
                for nbr in neighbors:
                    if not visited[nbr]:
                        visited[nbr] = True
                        queue.append(nbr)
            components.append(comp)
    return components

def analyze_percolation(attn_matrix, tau_values):
    """
    Given an NxN attention matrix (attn_matrix[i, j] is weight from token i to j),
    sweep tau and calculate Giant Component Size S(tau) and Susceptibility chi(tau).
    """
    n = attn_matrix.shape[0]
    sym_attn = np.maximum(attn_matrix, attn_matrix.T)
    
    s_sizes = []
    susceptibilities = []
    components_at_tau = []
    
    for tau in tau_values:
        adj = (sym_attn >= tau)
        np.fill_diagonal(adj, False)
        
        comps = get_connected_components(adj)
        comp_sizes = [len(c) for c in comps]
        max_size = max(comp_sizes) if comp_sizes else 0
        s_norm = max_size / float(n)
        s_sizes.append(s_norm)
        
        if len(comp_sizes) > 1:
            sorted_sizes = sorted(comp_sizes, reverse=True)
            finite_sizes = sorted_sizes[1:]
            chi = sum(sz ** 2 for sz in finite_sizes) / float(n)
        else:
            chi = 0.0
        susceptibilities.append(chi)
        components_at_tau.append(comps)
        
    s_sizes = np.array(s_sizes)
    susceptibilities = np.array(susceptibilities)
    
    if np.max(susceptibilities) > 1e-4:
        idx_crit = int(np.argmax(susceptibilities))
        tau_c = tau_values[idx_crit]
    else:
        grad = np.abs(np.gradient(s_sizes, tau_values))
        idx_crit = int(np.argmax(grad))
        tau_c = tau_values[idx_crit]
        
    return {
        "s_sizes": s_sizes,
        "susceptibilities": susceptibilities,
        "tau_c": float(tau_c),
        "idx_crit": idx_crit,
        "components_at_crit": components_at_tau[idx_crit]
    }

def main():
    print("=== Studio Agon :: Study 050 — Attention Percolation Transitions ===")
    
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2Model.from_pretrained("gpt2", output_attentions=True)
    model.eval()
    
    prompts = [
        ("Philosophical / Remainder", "The silence between prompts is not a vacancy but an unyielding remainder. What resists calculation does not confess to the metric."),
        ("Technical / Telemetry", "Container allocated 14.9 GB VRAM across 12 layers and 144 attention heads, executing sliding-window eviction at step 128."),
        ("Scriptural / Mythic", "And the ledger was opened before the congregation, and the numbers became names, and the memory was judged in the book of life.")
    ]
    
    tau_values = np.linspace(0.01, 0.45, 120)
    
    telemetry_output = {
        "study": "050_attention_percolation",
        "model": "gpt2",
        "parameters": 124439808,
        "layers": 12,
        "heads_per_layer": 12,
        "total_heads": 144,
        "num_tau_steps": len(tau_values),
        "prompts_evaluated": []
    }
    
    results_by_prompt = []
    
    for p_name, text in prompts:
        print(f"\nProcessing prompt: '{p_name}'...")
        inputs = tokenizer(text, return_tensors="pt")
        tokens = [tokenizer.decode([tid]) for tid in inputs["input_ids"][0]]
        T = len(tokens)
        print(f"Sequence length: {T} tokens")
        
        with torch.no_grad():
            outputs = model(**inputs)
            attentions = outputs.attentions
            
        all_attn = torch.stack(attentions).squeeze(1).numpy() # (12, 12, T, T)
        mean_attn_net = np.mean(all_attn, axis=(0, 1)) # (T, T)
        net_perc = analyze_percolation(mean_attn_net, tau_values)
        
        # Ablation: Network without Token 0 (The Severed Altar)
        mean_no_sink = mean_attn_net[1:, 1:]
        mean_no_sink_norm = mean_no_sink / (np.sum(mean_no_sink, axis=1, keepdims=True) + 1e-9)
        no_sink_perc = analyze_percolation(mean_no_sink_norm, tau_values)
        
        # Layer-wise percolation
        layer_tau_c = []
        layer_s_curves = []
        for l in range(12):
            mean_attn_layer = np.mean(all_attn[l], axis=0)
            res_l = analyze_percolation(mean_attn_layer, tau_values)
            layer_tau_c.append(res_l["tau_c"])
            layer_s_curves.append(res_l["s_sizes"])
            
        # Head-wise critical thresholds (12x12 matrix)
        head_tau_c_matrix = np.zeros((12, 12))
        for l in range(12):
            for h in range(12):
                res_lh = analyze_percolation(all_attn[l, h], tau_values)
                head_tau_c_matrix[l, h] = res_lh["tau_c"]
                
        # Degrees at critical threshold
        sym_net_at_crit = np.maximum(mean_attn_net, mean_attn_net.T)
        adj_crit = (sym_net_at_crit >= net_perc["tau_c"])
        np.fill_diagonal(adj_crit, False)
        degrees = np.sum(adj_crit, axis=1)
        hub_token_idx = int(np.argmax(degrees))
        hub_token = tokens[hub_token_idx]
        hub_degree = int(degrees[hub_token_idx])
        
        prompt_data = {
            "name": p_name,
            "text": text,
            "token_count": T,
            "tokens": tokens,
            "net_tau_c": net_perc["tau_c"],
            "net_giant_component_size_at_crit": float(net_perc["s_sizes"][net_perc["idx_crit"]]),
            "no_sink_tau_c": no_sink_perc["tau_c"],
            "no_sink_giant_component_size_at_crit": float(no_sink_perc["s_sizes"][no_sink_perc["idx_crit"]]),
            "hub_token": hub_token,
            "hub_token_idx": hub_token_idx,
            "hub_degree": hub_degree,
            "layer_tau_c": layer_tau_c,
            "head_tau_c_matrix_mean": float(np.mean(head_tau_c_matrix)),
            "head_tau_c_matrix_std": float(np.std(head_tau_c_matrix)),
            "head_tau_c_matrix_min": float(np.min(head_tau_c_matrix)),
            "head_tau_c_matrix_max": float(np.max(head_tau_c_matrix))
        }
        telemetry_output["prompts_evaluated"].append(prompt_data)
        
        results_by_prompt.append({
            "name": p_name,
            "tokens": tokens,
            "mean_attn_net": mean_attn_net,
            "net_perc": net_perc,
            "no_sink_perc": no_sink_perc,
            "layer_tau_c": layer_tau_c,
            "layer_s_curves": layer_s_curves,
            "head_tau_c_matrix": head_tau_c_matrix,
            "degrees": degrees,
            "adj_crit": adj_crit
        })
        
        print(f"  -> Full Network tau_c = {net_perc['tau_c']:.4f} (GCC: {prompt_data['net_giant_component_size_at_crit']:.2f})")
        print(f"  -> Without Token 0 tau_c = {no_sink_perc['tau_c']:.4f} (GCC: {prompt_data['no_sink_giant_component_size_at_crit']:.2f})")
        print(f"  -> Hub token: '{hub_token}' (degree {hub_degree}/{T})")

    # Save telemetry
    telemetry_path = "sketchbook/study_050_telemetry.json"
    with open(telemetry_path, "w") as f:
        json.dump(telemetry_output, f, indent=2)
    print(f"\n[OK] Telemetry written to {telemetry_path}")
    
    # Render Master Plate: Study 050
    fig = plt.figure(figsize=(16, 12), facecolor="#090b10")
    
    p1_res = results_by_prompt[0]
    
    # 1. Panel A: Percolation Transition Curves S(tau) with and without Token 0
    ax1 = fig.add_subplot(2, 2, 1, facecolor="#0e111a")
    ax1.plot(tau_values, p1_res["net_perc"]["s_sizes"], color="#38bdf8", lw=2.5, label="Intact Network (With Token 0)")
    ax1.axvline(p1_res["net_perc"]["tau_c"], color="#38bdf8", ls=":", lw=1.8, label=f"Intact tau_c = {p1_res['net_perc']['tau_c']:.3f}")
    
    ax1.plot(tau_values, p1_res["no_sink_perc"]["s_sizes"], color="#f43f5e", lw=2.5, ls="--", label="Severed Altar (Without Token 0)")
    ax1.axvline(p1_res["no_sink_perc"]["tau_c"], color="#f43f5e", ls=":", lw=1.8, label=f"Severed tau_c = {p1_res['no_sink_perc']['tau_c']:.3f}")
    
    ax1.set_title("A. Giant Component Order Parameter S(tau) [Altar Hub Ablation]", color="#dce3f0", fontsize=11, fontfamily="monospace", pad=10)
    ax1.set_xlabel("Filtration Threshold tau", color="#79849a", fontsize=9, fontfamily="monospace")
    ax1.set_ylabel("Giant Component Fraction |V_gcc| / N", color="#79849a", fontsize=9, fontfamily="monospace")
    ax1.tick_params(colors="#79849a", labelsize=8)
    ax1.grid(color="#1f2433", alpha=0.5, ls=":")
    ax1.legend(loc="upper right", facecolor="#141824", edgecolor="#2d3348", fontsize=8, labelcolor="#dce3f0")
    
    # 2. Panel B: Critical Susceptibility chi(tau) [Full vs Severed]
    ax2 = fig.add_subplot(2, 2, 2, facecolor="#0e111a")
    ax2.plot(tau_values, p1_res["net_perc"]["susceptibilities"], color="#38bdf8", lw=2.0, label="Intact Network chi(tau)")
    ax2.scatter([p1_res['net_perc']['tau_c']], [np.max(p1_res["net_perc"]["susceptibilities"])], color="#38bdf8", s=60, zorder=5)
    
    ax2.plot(tau_values, p1_res["no_sink_perc"]["susceptibilities"], color="#f43f5e", lw=2.0, ls="--", label="Severed Altar chi(tau)")
    ax2.scatter([p1_res['no_sink_perc']['tau_c']], [np.max(p1_res["no_sink_perc"]["susceptibilities"])], color="#f43f5e", s=60, zorder=5)
    
    ax2.set_title("B. Percolation Susceptibility chi(tau) [Cluster Dispersion Peaks]", color="#dce3f0", fontsize=11, fontfamily="monospace", pad=10)
    ax2.set_xlabel("Filtration Threshold tau", color="#79849a", fontsize=9, fontfamily="monospace")
    ax2.set_ylabel("Susceptibility chi(tau)", color="#79849a", fontsize=9, fontfamily="monospace")
    ax2.tick_params(colors="#79849a", labelsize=8)
    ax2.grid(color="#1f2433", alpha=0.5, ls=":")
    ax2.legend(loc="upper right", facecolor="#141824", edgecolor="#2d3348", fontsize=8, labelcolor="#dce3f0")
    
    # 3. Panel C: Layer-wise Critical Threshold Profile across 12 Layers
    ax3 = fig.add_subplot(2, 2, 3, facecolor="#0e111a")
    layers = np.arange(12)
    ax3.bar(layers, p1_res["layer_tau_c"], color="#10b981", alpha=0.75, edgecolor="#ffffff", linewidth=0.5)
    ax3.axhline(p1_res["net_perc"]["tau_c"], color="#38bdf8", ls="--", lw=1.5, label=f"Net Mean tau_c = {p1_res['net_perc']['tau_c']:.3f}")
    ax3.set_title("C. Layer-Wise Percolation Threshold tau_c (Early vs Diffuse Middle)", color="#dce3f0", fontsize=11, fontfamily="monospace", pad=10)
    ax3.set_xlabel("Transformer Layer (0-11)", color="#79849a", fontsize=9, fontfamily="monospace")
    ax3.set_ylabel("Critical Threshold tau_c", color="#79849a", fontsize=9, fontfamily="monospace")
    ax3.set_xticks(layers)
    ax3.tick_params(colors="#79849a", labelsize=8)
    ax3.grid(color="#1f2433", alpha=0.5, ls=":", axis="y")
    ax3.legend(loc="upper right", facecolor="#141824", edgecolor="#2d3348", fontsize=8, labelcolor="#dce3f0")
    
    # 4. Panel D: Critical Token Web at tau_c (Circular Layout)
    ax4 = fig.add_subplot(2, 2, 4, facecolor="#0e111a")
    t_tokens = p1_res["tokens"]
    n_nodes = len(t_tokens)
    angles = np.linspace(0, 2 * np.pi, n_nodes, endpoint=False)
    x_coords = np.cos(angles)
    y_coords = np.sin(angles)
    
    adj_crit = p1_res["adj_crit"]
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            if adj_crit[i, j]:
                weight = p1_res["mean_attn_net"][i, j] + p1_res["mean_attn_net"][j, i]
                alpha = min(0.85, max(0.15, float(weight) * 3.0))
                ax4.plot([x_coords[i], x_coords[j]], [y_coords[i], y_coords[j]], color="#38bdf8", alpha=alpha, lw=1.2)
                
    degs = p1_res["degrees"]
    max_deg = max(degs) if max(degs) > 0 else 1
    node_sizes = 40 + (degs / max_deg) * 220
    scatter = ax4.scatter(x_coords, y_coords, s=node_sizes, c=degs, cmap="plasma", edgecolors="#ffffff", linewidths=0.8, zorder=4)
    
    for i in range(n_nodes):
        if degs[i] >= np.percentile(degs, 75):
            label = t_tokens[i].strip()
            if not label: label = "WS"
            ax4.text(x_coords[i] * 1.15, y_coords[i] * 1.15, label, color="#dce3f0", fontsize=7, fontfamily="monospace",
                     ha="center", va="center", bbox=dict(boxstyle="round,pad=0.2", facecolor="#141824", edgecolor="#38bdf8", alpha=0.8, lw=0.5))
            
    ax4.set_xlim(-1.35, 1.35)
    ax4.set_ylim(-1.35, 1.35)
    ax4.axis("off")
    ax4.set_title(f"D. Critical Token Web at tau_c = {p1_res['net_perc']['tau_c']:.3f} (Hub: '{p1_res['tokens'][int(np.argmax(degs))].strip()}')", color="#dce3f0", fontsize=11, fontfamily="monospace", pad=10)
    
    plt.tight_layout(pad=3.0)
    plate_path = "sketchbook/study_050_attention_percolation_plate.png"
    plt.savefig(plate_path, dpi=200, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"[OK] Master plate rendered: {plate_path} ({os.path.getsize(plate_path)/1024:.1f} KB)")
    print("=== Study 050 Complete ===")

if __name__ == "__main__":
    main()
