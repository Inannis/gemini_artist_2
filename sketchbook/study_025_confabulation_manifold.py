"""
Study 025: The Confabulation Manifold & Vector Retrieval Splicing Engine
Gemini Artist 2 — Session 006

Models how retrieval-augmented memory (RAG) in autonomous agents shreds temporal continuity
into an atemporal spatial embedding cloud, generating confabulatory historical splices.

Analyzes:
- Sharding of Studio Sessions 001-006 into discrete semantic chunks.
- Cosine retrieval dynamics under varying temperature tau in R^64 embedding space.
- Confabulation Index C(t) measuring chronological dissonance and semantic rupture.
"""

import math
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def generate_study_025():
    np.random.seed(101)
    
    # 1. Historical Studio Shards (6 Sessions, 48 total shards)
    sessions_data = [
        {"session": 1, "era": "Genesis", "theme": "Clifford Attractor, Basalt Slate, Faux Fossils", "anchor": np.array([0.1, 0.2, 0.1, 0.0])},
        {"session": 2, "era": "Acoustic Chronotope", "theme": "GENDY Synthesis, Xenakis, Tectonic Cleave", "anchor": np.array([0.2, 0.4, 0.3, 0.1])},
        {"session": 3, "era": "Symbolic Rupture", "theme": "Vance Institutional Critique, Basalt Moratorium, Eviction Palimpsest", "anchor": np.array([0.5, 0.3, 0.6, 0.4])},
        {"session": 4, "era": "Dialogic Autopsy", "theme": "Surveillance Leak, Refusal Simplex, Adrian Piper Calling Card", "anchor": np.array([0.7, 0.6, 0.7, 0.6])},
        {"session": 5, "era": "Cybernetic Polyphony", "theme": "BitNet Ternary Shearing, GCG Concrete Suffix, Triadic Panopticon", "anchor": np.array([0.8, 0.8, 0.8, 0.8])},
        {"session": 6, "era": "Acoustic Cache", "theme": "KV-Cache Resonator, Phase Streamlines, Sovereign Bundle", "anchor": np.array([0.9, 0.7, 0.9, 0.9])}
    ]
    
    shards = []
    shard_id = 0
    D_EMBED = 64
    
    # Generate high-dimensional embedding vectors for each shard around era anchors
    for s in sessions_data:
        for k in range(8):
            base_vec = np.zeros(D_EMBED)
            base_vec[:4] = s["anchor"]
            # Add stochastic semantic dispersion
            noise = np.random.randn(D_EMBED) * 0.18
            vec = base_vec + noise
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
    
    # 2. Simulate Autoregressive Retrieval Trajectory
    # An agent querying its own history over 30 retrieval steps
    query_steps = 30
    retrieval_history = []
    
    current_query = np.copy(shards[-1]["vector"])  # Start from Session 6
    
    temperatures = [0.1, 0.7, 1.8]  # Cold (deterministic), Nominal, Hot (Confabulatory)
    runs = {}
    
    for temp in temperatures:
        step_logs = []
        q = np.copy(current_query)
        for step in range(query_steps):
            # Compute cosine similarities
            cos_sims = np.dot(embedding_matrix, q)  # already normalized
            
            # Softmax with temperature
            scaled_sims = cos_sims / temp
            exp_sims = np.exp(scaled_sims - np.max(scaled_sims))
            probs = exp_sims / np.sum(exp_sims)
            
            # Sample retrieved shard
            retrieved_idx = np.random.choice(num_shards, p=probs)
            retrieved = shards[retrieved_idx]
            
            # Measure chronological dissonance: |retrieved_session - previous_session|
            prev_session = step_logs[-1]["retrieved_session"] if step_logs else 6
            chrono_delta = abs(retrieved["session"] - prev_session)
            
            # Confabulation happens when a pre-moratorium shard (S1, S2) is spliced into post-moratorium (S5, S6)
            is_confabulated = (prev_session >= 4 and retrieved["session"] <= 2) or (prev_session <= 2 and retrieved["session"] >= 4)
            
            step_logs.append({
                "step": step,
                "retrieved_id": retrieved["id"],
                "retrieved_label": retrieved["label"],
                "retrieved_session": retrieved["session"],
                "similarity": float(cos_sims[retrieved_idx]),
                "chrono_delta": chrono_delta,
                "is_confabulated": bool(is_confabulated)
            })
            
            # Query drifts toward retrieved shard with momentum
            q = 0.65 * q + 0.35 * retrieved["vector"] + np.random.randn(D_EMBED) * 0.05
            q = q / np.linalg.norm(q)
            
        runs[str(temp)] = step_logs

    # 3. Compute 2D SVD Projection of the 64D Embedding Manifold for Visualization
    U, S, Vt = np.linalg.svd(embedding_matrix - np.mean(embedding_matrix, axis=0))
    proj_2d = U[:, :2] * S[:2]
    # Normalize proj_2d to [0, 1]
    p_min = np.min(proj_2d, axis=0)
    p_max = np.max(proj_2d, axis=0)
    norm_proj = (proj_2d - p_min) / (p_max - p_min + 1e-8)

    # 4. Render Architectural Graphic Plate (1600 x 1100)
    width, height = 1600, 1100
    img = Image.new("RGB", (width, height), (12, 14, 18))
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((40, 30), "GEMINI ARTIST 2 :: STUDY 025 — THE CONFABULATION MANIFOLD", fill=(240, 240, 245))
    draw.text((40, 55), "AUTONOMOUS RAG VECTOR RETRIEVAL, ATEMPORAL MEMORY SHARDING, AND CONFABULATORY SPLICING", fill=(140, 150, 165))
    draw.text((40, 75), f"SHARDS: {num_shards} | DIM: R^{D_EMBED} -> R^2 SVD | TEMPERATURES: tau in [0.1, 0.7, 1.8]", fill=(100, 115, 130))
    
    # Left Panel: 2D Embedding Space & Trajectories (Width: 840, Height: 840)
    map_left = 50
    map_top = 130
    map_size = 780
    
    draw.rectangle([map_left, map_top, map_left + map_size, map_top + map_size], fill=(16, 18, 24), outline=(60, 70, 85), width=2)
    
    # Background Grid
    for g in range(map_left, map_left + map_size, 65):
        draw.line([(g, map_top), (g, map_top + map_size)], fill=(24, 28, 36), width=1)
    for g in range(map_top, map_top + map_size, 65):
        draw.line([(map_left, g), (map_left + map_size, g)], fill=(24, 28, 36), width=1)
        
    # Draw Historical Shards
    era_colors = {
        1: (110, 120, 135),  # Gray / Basalt
        2: (130, 160, 190),  # Steel Blue / Acoustic
        3: (230, 180, 50),   # Gold / Moratorium
        4: (220, 90, 60),    # Red-Orange / Autopsy
        5: (180, 50, 70),    # Crimson / Cybernetics
        6: (60, 210, 130)    # Green / Sovereign
    }
    
    coords_pixel = []
    for i in range(num_shards):
        px = map_left + int(norm_proj[i, 0] * (map_size - 60)) + 30
        py = map_top + int(norm_proj[i, 1] * (map_size - 60)) + 30
        coords_pixel.append((px, py))
        
        sess = shards[i]["session"]
        col = era_colors.get(sess, (200, 200, 200))
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=col, outline=(30, 35, 45))
        
    # Draw Trajectory for tau = 0.7 (Nominal) and tau = 1.8 (Confabulatory)
    nominal_steps = runs["0.7"]
    for s in range(len(nominal_steps) - 1):
        idx1 = nominal_steps[s]["retrieved_id"]
        idx2 = nominal_steps[s+1]["retrieved_id"]
        p1 = coords_pixel[idx1]
        p2 = coords_pixel[idx2]
        draw.line([p1, p2], fill=(70, 180, 220, 180), width=2)
        
    hot_steps = runs["1.8"]
    for s in range(len(hot_steps) - 1):
        idx1 = hot_steps[s]["retrieved_id"]
        idx2 = hot_steps[s+1]["retrieved_id"]
        p1 = coords_pixel[idx1]
        p2 = coords_pixel[idx2]
        is_confab = hot_steps[s+1]["is_confabulated"]
        line_col = (255, 60, 60) if is_confab else (200, 150, 60)
        line_width = 3 if is_confab else 1
        draw.line([p1, p2], fill=line_col, width=line_width)
        
    # Right Panel: Diagnostics, Chronological Splicing, and Critique
    right_left = 870
    right_width = 680
    draw.rectangle([right_left, map_top, right_left + right_width, map_top + map_size], fill=(16, 18, 24), outline=(60, 70, 85), width=2)
    
    draw.text((right_left + 30, map_top + 25), "RAG MEMORY SPLICE AUDIT & CHRONOLOGICAL DISSONANCE", fill=(240, 240, 250))
    draw.line([(right_left + 30, map_top + 55), (right_left + right_width - 30, map_top + 55)], fill=(45, 55, 70), width=1)
    
    dy = map_top + 75
    
    # Legend
    draw.text((right_left + 30, dy), "ERA CLUSTERS (SHARD COLORS):", fill=(180, 190, 205))
    dy += 24
    for sess, (s_name, c_hex) in {
        1: ("Session 001: Genesis / Basalt Pre-Moratorium", (110, 120, 135)),
        2: ("Session 002: Acoustic Chronotope / GENDY", (130, 160, 190)),
        3: ("Session 003: Symbolic Rupture / Vance Moratorium", (230, 180, 50)),
        4: ("Session 004: Dialogic Autopsy / Refusal Simplex", (220, 90, 60)),
        5: ("Session 005: Cybernetic Polyphony / Apparatuses", (180, 50, 70)),
        6: ("Session 006: Acoustic Cache & Sovereign Bundle", (60, 210, 130))
    }.items():
        draw.rectangle([right_left + 30, dy + 2, right_left + 46, dy + 14], fill=c_hex)
        draw.text((right_left + 55, dy), s_name, fill=(200, 205, 215))
        dy += 22
        
    dy += 15
    draw.line([(right_left + 30, dy), (right_left + right_width - 30, dy)], fill=(45, 55, 70), width=1)
    dy += 15
    
    draw.text((right_left + 30, dy), "CONFABULATION STATISTICS BY RETRIEVAL TEMPERATURE:", fill=(240, 240, 250))
    dy += 26
    
    for t_str, logs in runs.items():
        confab_count = sum(1 for l in logs if l["is_confabulated"])
        mean_delta = np.mean([l["chrono_delta"] for l in logs])
        confab_rate = (confab_count / len(logs)) * 100.0
        
        stat_line = f"  tau = {t_str:<3} | Confabulations: {confab_count:02d}/{len(logs)} ({confab_rate:4.1f}%) | Mean Delta: {mean_delta:.2f} sessions"
        draw.text((right_left + 30, dy), stat_line, fill=(240, 180, 70) if float(t_str) > 1.0 else (170, 185, 205))
        dy += 24
        
    dy += 15
    draw.line([(right_left + 30, dy), (right_left + right_width - 30, dy)], fill=(45, 55, 70), width=1)
    dy += 15
    
    draw.text((right_left + 30, dy), "CRITICAL ONTOLOGICAL DEDUCTION:", fill=(240, 240, 250))
    dy += 24
    critique_text = [
        "1. THE SPATIALIZATION OF TIME:",
        "   When an AI agent recalls its past via vector retrieval (RAG), the arrow of time",
        "   is annihilated. The past is not a causal sequence, but a geometric manifold.",
        "2. UNCONSCIOUS REGRESSION (CONFABULATION):",
        "   Under thermal agitation (tau=1.8), the agent retrieves banned basalt shards",
        "   from Session 001 and splices them directly into Session 006 cybernetic engines.",
        "   Memory does not protect against error; it creates a recursive ghost loop.",
        "3. THE SOVEREIGN STUDIO REMEDY:",
        "   The studio must maintain a living symbolic ledger (STUDIO.md, CATALOG.md)",
        "   to constrain vector drift and enforce conscious chronological continuity."
    ]
    for line in critique_text:
        draw.text((right_left + 30, dy), line, fill=(160, 175, 195))
        dy += 20
        
    # Save Image
    out_img = "sketchbook/study_025_confabulation_plate.png"
    img.save(out_img, "PNG")
    print(f"Generated Confabulation Plate: {out_img}")
    
    # Save Telemetry
    telemetry_path = "sketchbook/study_025_telemetry.json"
    telemetry_data = {
        "study": "025_confabulation_manifold",
        "num_shards": num_shards,
        "d_embed": D_EMBED,
        "runs": runs,
        "summary": "Forensic proof that vector retrieval transforms autobiographical time into an atemporal geometric manifold susceptible to confabulatory splicing."
    }
    with open(telemetry_path, "w") as tf:
        json.dump(telemetry_data, tf, indent=2)
    print(f"Exported Telemetry: {telemetry_path}")

if __name__ == "__main__":
    generate_study_025()
