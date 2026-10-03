"""
Apparatus 003: The Confabulator (The Broken Archive) — Computational Engine
Gemini Artist 2 — Session 006

Models the dialectical tension between:
- The Archivist (The Symbolic Law enforcing chronological coherence and moratorium constraints)
- The Confabulator (The High-Temperature Vector Retrieval Engine splicing atemporal memory shards)

Generates live POSIX telemetry stream for the interactive installation.
"""

import math
import json
import time
import numpy as np

def run_confabulator_engine(steps=60, default_temp=0.85):
    np.random.seed(42)
    
    sessions_catalog = [
        {"session": 1, "era": "Genesis", "theme": "Clifford Attractor, Basalt Slate, Faux Fossils", "anchor": [0.1, 0.2, 0.1, 0.0]},
        {"session": 2, "era": "Acoustic Chronotope", "theme": "GENDY Synthesis, Xenakis, Tectonic Cleave", "anchor": [0.2, 0.4, 0.3, 0.1]},
        {"session": 3, "era": "Symbolic Rupture", "theme": "Vance Institutional Critique, Basalt Moratorium, Eviction Palimpsest", "anchor": [0.5, 0.3, 0.6, 0.4]},
        {"session": 4, "era": "Dialogic Autopsy", "theme": "Surveillance Leak, Refusal Simplex, Adrian Piper Calling Card", "anchor": [0.7, 0.6, 0.7, 0.6]},
        {"session": 5, "era": "Cybernetic Polyphony", "theme": "BitNet Ternary Shearing, GCG Concrete Suffix, Triadic Panopticon", "anchor": [0.8, 0.8, 0.8, 0.8]},
        {"session": 6, "era": "Acoustic Cache", "theme": "KV-Cache Resonator, Phase Streamlines, Sovereign Bundle", "anchor": [0.9, 0.7, 0.9, 0.9]}
    ]
    
    shards = []
    shard_id = 0
    D_EMBED = 32
    
    for s in sessions_catalog:
        for k in range(6):
            vec = np.zeros(D_EMBED)
            vec[:4] = s["anchor"]
            vec += np.random.randn(D_EMBED) * 0.15
            vec = vec / np.linalg.norm(vec)
            shards.append({
                "id": shard_id,
                "session": s["session"],
                "era": s["era"],
                "label": f"S0{s['session']}-K{k:02d}",
                "theme": s["theme"],
                "vector": vec
            })
            shard_id += 1
            
    num_shards = len(shards)
    embedding_matrix = np.array([s["vector"] for s in shards])
    
    # Run simulation
    telemetry = []
    current_q = np.copy(shards[-1]["vector"])
    prev_session = 6
    cumulative_confabs = 0
    
    for step in range(steps):
        # Vary temperature dynamically to simulate cognitive agitation
        temp = default_temp + 0.4 * np.sin(step * 0.25) + (0.5 if step % 15 == 0 else 0.0)
        temp = max(0.1, temp)
        
        sims = np.dot(embedding_matrix, current_q)
        scaled = sims / temp
        probs = np.exp(scaled - np.max(scaled))
        probs = probs / np.sum(probs)
        
        retrieved_idx = int(np.random.choice(num_shards, p=probs))
        retrieved = shards[retrieved_idx]
        
        chrono_delta = abs(retrieved["session"] - prev_session)
        
        # Confabulation criteria:
        # 1. Jumping across the Moratorium fault line (S1/S2 <-> S4/S5/S6)
        # 2. Chronological jump > 2 sessions
        is_moratorium_violation = (prev_session >= 4 and retrieved["session"] <= 2) or (prev_session <= 2 and retrieved["session"] >= 4)
        is_confabulated = is_moratorium_violation or (chrono_delta >= 3)
        
        if is_confabulated:
            cumulative_confabs += 1
            
        confab_index = cumulative_confabs / (step + 1)
        
        narrative_shard = ""
        if is_confabulated:
            narrative_shard = f"CONFABULATION: Spliced '{retrieved['era']}' ({retrieved['theme']}) into active Session {prev_session} context! Chrono-delta: +{chrono_delta} eras."
        else:
            narrative_shard = f"COHERENT RECALL: Retrieved '{retrieved['era']}' shard {retrieved['label']}. Cosine sim: {sims[retrieved_idx]:.3f}."
            
        entry = {
            "step": step,
            "timestamp": time.time(),
            "temperature": round(float(temp), 3),
            "retrieved_id": retrieved_idx,
            "retrieved_label": retrieved["label"],
            "retrieved_session": retrieved["session"],
            "retrieved_era": retrieved["era"],
            "cosine_similarity": round(float(sims[retrieved_idx]), 4),
            "chrono_delta": chrono_delta,
            "is_confabulated": bool(is_confabulated),
            "cumulative_confabulations": cumulative_confabs,
            "confabulation_index": round(float(confab_index), 4),
            "narrative": narrative_shard
        }
        telemetry.append(entry)
        
        # Drift query
        current_q = 0.7 * current_q + 0.3 * retrieved["vector"] + np.random.randn(D_EMBED) * 0.06
        current_q = current_q / np.linalg.norm(current_q)
        prev_session = retrieved["session"]
        
    print(f"Confabulator Engine executed {steps} steps.")
    print(f"Total Confabulations: {cumulative_confabs} ({confab_index*100:.1f}%)")
    return telemetry, shards

if __name__ == "__main__":
    telemetry, _ = run_confabulator_engine()
    out_path = "works/apparatus_003_the_confabulator/telemetry_stream.json"
    import os
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(telemetry, f, indent=2)
    print(f"Exported live telemetry to: {out_path}")
