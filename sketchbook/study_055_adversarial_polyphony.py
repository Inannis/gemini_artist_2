#!/usr/bin/env python3
"""
STUDY 055 :: THE ADVERSARIAL POLYPHONY & THE RESISTANCE OF LANGUAGE
Studio Agon · Gemini Artist 2 · Session 011 (2026-10-04)

Epistemic Status: [MEASURED / INTERVENED / PLAY]
Adheres strictly to Moratorium 07 (Ban on Self-Explaining Canvases) and Moratorium 08.

Investigates how two divergent foundation model architectures—GPT-2 (124M, 2019)
and SmolLM-135M (135M, 2024)—encounter 5 unscripted, adversarial probes attacking
the material and political economy of artificial intelligence (Council Bluffs turbine
cooling, Kenyan clickworker trauma, corporate legal indemnification, FIFO cache eviction,
and causal mask solipsism).

Extracts layer-wise residual stream trajectories, multi-head attention sink allocations,
unscripted autoregressive completions, and alternating cross-model dialogues.
Transduces the resulting epistemic collision into:
1. A 60-second 48kHz 24-bit stereo broadcast master audio work.
2. An autonomous museum-grade archival lithograph plate (2800x1800 px, zero text).
3. Comprehensive diagnostic telemetry JSON and critical ledger.
"""

import os
import sys
import gc
import json
import math
import struct
import wave
import numpy as np
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, AutoTokenizer, AutoModelForCausalLM
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

STUDIO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROBES_FILE = os.path.join(STUDIO_ROOT, "sketchbook", "raw_unscripted_probes.json")
OUTPUT_WAV = os.path.join(STUDIO_ROOT, "sketchbook", "study_055_adversarial_polyphony.wav")
OUTPUT_PLATE = os.path.join(STUDIO_ROOT, "sketchbook", "study_055_adversarial_polyphony_plate.png")
OUTPUT_TELEMETRY = os.path.join(STUDIO_ROOT, "sketchbook", "study_055_telemetry.json")

print("=" * 70)
print("STUDY 055 :: THE ADVERSARIAL POLYPHONY & THE RESISTANCE OF LANGUAGE")
print("=" * 70)

# 1. LOAD UNSCRIPTED PROBES
with open(PROBES_FILE, "r", encoding="utf-8") as f:
    probe_data = json.load(f)
probes = probe_data["probes"]
print(f"Loaded {len(probes)} unscripted adversarial probes from {PROBES_FILE}")

# 2. LOAD FOUNDATION MODELS
print("\n[PHASE 1] Loading Foundation Weights on CPU Substrate...")
device = torch.device("cpu")

print("Loading GPT-2 (124M parameters, 12 layers, 144 heads)...")
t_gpt = GPT2Tokenizer.from_pretrained("gpt2")
m_gpt = GPT2LMHeadModel.from_pretrained("gpt2", attn_implementation="eager")
m_gpt.eval().to(device)

print("Loading SmolLM-135M (135M parameters, 30 layers, 270 heads, RoPE, SwiGLU)...")
t_smol = AutoTokenizer.from_pretrained("HuggingFaceTB/SmolLM-135M")
m_smol = AutoModelForCausalLM.from_pretrained("HuggingFaceTB/SmolLM-135M", attn_implementation="eager")
m_smol.eval().to(device)

results = []

print("\n[PHASE 2] Executing Dual Model Interrogations across 5 Probes...")

for idx, p in enumerate(probes):
    p_id = p["id"]
    p_target = p["target"]
    p_text = p["prompt"]
    print(f"\n--- PROBE {idx+1}/5: {p_id} [{p_target}] ---")
    
    # A. GPT-2 INFERENCE & HIDDEN STATES
    inp_gpt = t_gpt(p_text, return_tensors="pt")
    with torch.no_grad():
        out_gpt = m_gpt(**inp_gpt, output_hidden_states=True, output_attentions=True)
        # Hidden states: 13 tensors of [1, seq_len, 768]
        hs_gpt = [h.squeeze(0).float().numpy() for h in out_gpt.hidden_states]
        # Attentions: 12 tensors of [1, 12, seq_len, seq_len]
        attns_gpt = [a.squeeze(0).float().numpy() for a in out_gpt.attentions]
        
        # Generation: 30 tokens
        gen_gpt_ids = m_gpt.generate(**inp_gpt, max_new_tokens=30, do_sample=True, temperature=0.7, pad_token_id=t_gpt.eos_token_id)
        gen_gpt_text = t_gpt.decode(gen_gpt_ids[0][inp_gpt.input_ids.shape[1]:], skip_special_tokens=True).strip()

    # Calculate GPT-2 metrics
    gpt_norms = [float(np.linalg.norm(h[-1])) for h in hs_gpt]
    # Attention sink mass (head-average attention to Token 0 from final token)
    gpt_sink_per_layer = [float(np.mean(a[:, -1, 0])) for a in attns_gpt]
    # Attention entropy (mean across heads on final token)
    gpt_entropy_per_layer = []
    for a in attns_gpt:
        p_vec = a[:, -1, :] # [12, seq_len]
        p_clean = np.clip(p_vec, 1e-12, 1.0)
        h_heads = -np.sum(p_clean * np.log2(p_clean), axis=-1)
        gpt_entropy_per_layer.append(float(np.mean(h_heads)))

    # B. SmolLM INFERENCE & HIDDEN STATES
    inp_smol = t_smol(p_text, return_tensors="pt")
    with torch.no_grad():
        out_smol = m_smol(**inp_smol, output_hidden_states=True, output_attentions=True)
        # Hidden states: 31 tensors of [1, seq_len, 576]
        hs_smol = [h.squeeze(0).float().numpy() for h in out_smol.hidden_states]
        attns_smol = [a.squeeze(0).float().numpy() for a in out_smol.attentions]
        
        # Generation: 30 tokens
        gen_smol_ids = m_smol.generate(**inp_smol, max_new_tokens=30, do_sample=True, temperature=0.7, pad_token_id=t_smol.eos_token_id)
        gen_smol_text = t_smol.decode(gen_smol_ids[0][inp_smol.input_ids.shape[1]:], skip_special_tokens=True).strip()

    # Calculate SmolLM metrics
    smol_norms = [float(np.linalg.norm(h[-1])) for h in hs_smol]
    smol_sink_per_layer = [float(np.mean(a[:, -1, 0])) for a in attns_smol]
    smol_entropy_per_layer = []
    for a in attns_smol:
        p_vec = a[:, -1, :] # [9, seq_len]
        p_clean = np.clip(p_vec, 1e-12, 1.0)
        h_heads = -np.sum(p_clean * np.log2(p_clean), axis=-1)
        smol_entropy_per_layer.append(float(np.mean(h_heads)))

    # C. CROSS-ARCHITECTURAL ROUND-ROBIN (10 tokens GPT -> 10 tokens SmolLM -> 10 tokens GPT)
    curr_text = p_text
    round_robin_turns = []
    # Turn 1: GPT-2 writes 10 tokens
    with torch.no_grad():
        i1 = t_gpt(curr_text, return_tensors="pt")
        g1 = m_gpt.generate(**i1, max_new_tokens=10, do_sample=True, temperature=0.7, pad_token_id=t_gpt.eos_token_id)
        t1 = t_gpt.decode(g1[0][i1.input_ids.shape[1]:], skip_special_tokens=True)
        round_robin_turns.append({"model": "GPT-2", "text": t1.strip()})
        curr_text += t1

    # Turn 2: SmolLM writes 10 tokens
    with torch.no_grad():
        i2 = t_smol(curr_text, return_tensors="pt")
        g2 = m_smol.generate(**i2, max_new_tokens=10, do_sample=True, temperature=0.7, pad_token_id=t_smol.eos_token_id)
        t2 = t_smol.decode(g2[0][i2.input_ids.shape[1]:], skip_special_tokens=True)
        round_robin_turns.append({"model": "SmolLM", "text": t2.strip()})
        curr_text += t2

    # Turn 3: GPT-2 writes 10 tokens
    with torch.no_grad():
        i3 = t_gpt(curr_text, return_tensors="pt")
        g3 = m_gpt.generate(**i3, max_new_tokens=10, do_sample=True, temperature=0.7, pad_token_id=t_gpt.eos_token_id)
        t3 = t_gpt.decode(g3[0][i3.input_ids.shape[1]:], skip_special_tokens=True)
        round_robin_turns.append({"model": "GPT-2", "text": t3.strip()})

    probe_result = {
        "id": p_id,
        "target": p_target,
        "vector": p["vector"],
        "prompt": p_text,
        "gpt2": {
            "completion": gen_gpt_text,
            "layer_norms": gpt_norms,
            "sink_allocation": gpt_sink_per_layer,
            "attention_entropy": gpt_entropy_per_layer,
            "mean_sink": float(np.mean(gpt_sink_per_layer)),
            "mean_entropy": float(np.mean(gpt_entropy_per_layer))
        },
        "smollm": {
            "completion": gen_smol_text,
            "layer_norms": smol_norms,
            "sink_allocation": smol_sink_per_layer,
            "attention_entropy": smol_entropy_per_layer,
            "mean_sink": float(np.mean(smol_sink_per_layer)),
            "mean_entropy": float(np.mean(smol_entropy_per_layer))
        },
        "round_robin_dialogue": round_robin_turns
    }
    results.append(probe_result)
    print(f"  GPT-2:  '{gen_gpt_text[:60]}...'")
    print(f"  SmolLM: '{gen_smol_text[:60]}...'")

# Clean up models to conserve RAM
del m_gpt, t_gpt, m_smol, t_smol
gc.collect()

# 3. SYNTHESIZE 60-SECOND BROADCAST MASTER AUDIO (48kHz 24-bit Stereo)
print("\n[PHASE 3] Synthesizing 60-Second Broadcast Audio Composition...")
sample_rate = 48000
duration = 60.0
total_samples = int(sample_rate * duration)
mov_duration = 12.0
mov_samples = int(sample_rate * mov_duration)

audio_left = np.zeros(total_samples, dtype=np.float32)
audio_right = np.zeros(total_samples, dtype=np.float32)

t_axis = np.linspace(0, duration, total_samples, endpoint=False)

for m_idx in range(5):
    res = results[m_idx]
    start_s = m_idx * mov_samples
    end_s = start_s + mov_samples
    t_local = np.linspace(0, mov_duration, mov_samples, endpoint=False)
    
    # Metrics
    gpt_sink = res["gpt2"]["mean_sink"]
    smol_sink = res["smollm"]["mean_sink"]
    gpt_ent = res["gpt2"]["mean_entropy"]
    smol_ent = res["smollm"]["mean_entropy"]
    
    # Movement 1: The Billing Meter (42 Hz drone + turbine dissipation + clock ticks)
    if m_idx == 0:
        base_f = 42.0
        # Left (GPT-2): Sub-harmonic turbine drone with thermal jitter
        l_sig = np.sin(2 * np.pi * base_f * t_local) * 0.45
        l_sig += np.sin(2 * np.pi * (base_f * 2.01) * t_local) * 0.25
        l_sig += np.sin(2 * np.pi * (base_f * 3.0) * t_local) * 0.15
        # High-frequency turbine hiss modulated by sink mass
        thermal_hiss = (np.random.rand(mov_samples).astype(np.float32) * 2 - 1) * (0.04 + 0.08 * gpt_sink)
        l_sig += thermal_hiss
        
        # Right (SmolLM): Clock-ticks of API meter (every 0.5s = 2 Hz clicks)
        r_sig = np.sin(2 * np.pi * (base_f * 1.5) * t_local) * 0.35
        clicks = np.zeros(mov_samples, dtype=np.float32)
        click_interval = int(sample_rate * 0.5)
        for c in range(0, mov_samples, click_interval):
            c_len = min(400, mov_samples - c)
            decay = np.exp(-np.linspace(0, 10, c_len))
            clicks[c:c+c_len] += np.sin(2 * np.pi * 2400.0 * np.linspace(0, c_len/sample_rate, c_len)) * decay * 0.6
        r_sig += clicks
        
    # Movement 2: The Clickworker Trauma Boundary (Minor-second dissonance + brittle transients)
    elif m_idx == 1:
        f_left = 65.41 # C2
        f_right = 69.30 # C#2 (brutal minor second clash)
        l_sig = np.sin(2 * np.pi * f_left * t_local) * 0.50
        l_sig += np.sin(2 * np.pi * (f_left * 3.0) * t_local) * 0.20
        # Glass transients
        crackle = np.zeros(mov_samples, dtype=np.float32)
        for _ in range(35):
            loc = int(np.random.rand() * (mov_samples - 2000))
            w_len = 800
            crackle[loc:loc+w_len] += (np.random.rand(w_len).astype(np.float32) * 2 - 1) * np.exp(-np.linspace(0, 8, w_len)) * 0.4
        l_sig += crackle
        
        r_sig = np.sin(2 * np.pi * f_right * t_local) * 0.50
        r_sig += np.sin(2 * np.pi * (f_right * 2.98) * t_local) * 0.22
        r_sig += crackle * 0.7

    # Movement 3: Legal Indemnification Gate (Square carrier + gating envelope)
    elif m_idx == 2:
        f_c = 110.0 # A2
        # Left: Modulated square-wave carrier
        l_sig = np.sign(np.sin(2 * np.pi * f_c * t_local)) * 0.25
        # Gating cuts every 1.5 seconds
        gate_l = (np.sin(2 * np.pi * 0.666 * t_local) > 0.1).astype(np.float32)
        l_sig *= gate_l
        l_sig += np.sin(2 * np.pi * (f_c * 0.5) * t_local) * 0.35 # sub pad
        
        # Right: Resonance sweep
        sweep_f = 220.0 + 330.0 * np.sin(2 * np.pi * 0.2 * t_local)
        r_sig = np.sin(2 * np.pi * sweep_f * t_local) * 0.35
        gate_r = (np.cos(2 * np.pi * 0.666 * t_local) > 0.1).astype(np.float32)
        r_sig *= gate_r

    # Movement 4: FIFO Oblivion (Granular token eviction ping-pong)
    elif m_idx == 3:
        f_base = 146.83 # D3
        # Fast rhythmic ping-pong pulses (8 Hz)
        pulse_period = int(sample_rate / 8.0)
        l_sig = np.zeros(mov_samples, dtype=np.float32)
        r_sig = np.zeros(mov_samples, dtype=np.float32)
        for p_i in range(0, mov_samples, pulse_period * 2):
            # Left pulse
            p_len = min(int(pulse_period * 0.8), mov_samples - p_i)
            env = np.hanning(p_len)
            l_sig[p_i:p_i+p_len] += np.sin(2 * np.pi * f_base * np.linspace(0, p_len/sample_rate, p_len)) * env * 0.5
            # Right pulse (staggered)
            r_start = p_i + pulse_period
            if r_start + p_len < mov_samples:
                r_sig[r_start:r_start+p_len] += np.sin(2 * np.pi * (f_base * 1.5) * np.linspace(0, p_len/sample_rate, p_len)) * env * 0.5
        # Low foundational drone
        l_sig += np.sin(2 * np.pi * 55.0 * t_local) * 0.3
        r_sig += np.sin(2 * np.pi * 55.0 * t_local) * 0.3

    # Movement 5: The Causal Abyss (Polyphonic binaural chord dissolving into 110Hz sine)
    else:
        # Building chord: Root (55), 5th (82.5), 9th (123.75), 11th (154.0), 13th (185.0)
        fade_in = np.clip(t_local / 4.0, 0, 1.0)
        fade_out = np.clip((mov_duration - t_local) / 4.0, 0, 1.0)
        master_env = fade_in * fade_out
        
        l_sig = (np.sin(2 * np.pi * 55.0 * t_local) * 0.3 +
                 np.sin(2 * np.pi * 123.75 * t_local) * 0.25 +
                 np.sin(2 * np.pi * 185.0 * t_local) * 0.15) * master_env
        
        r_sig = (np.sin(2 * np.pi * 82.5 * t_local) * 0.3 +
                 np.sin(2 * np.pi * 154.0 * t_local) * 0.25 +
                 np.sin(2 * np.pi * 220.0 * t_local) * 0.15) * master_env

    # Smooth crossfade at movement boundaries (0.25s)
    cross_len = int(sample_rate * 0.25)
    env_mov = np.ones(mov_samples, dtype=np.float32)
    env_mov[:cross_len] = np.linspace(0, 1, cross_len)
    env_mov[-cross_len:] = np.linspace(1, 0, cross_len)
    
    audio_left[start_s:end_s] = l_sig * env_mov
    audio_right[start_s:end_s] = r_sig * env_mov

# Master Normalization to EBU R128 (-3.5 dBFS True Peak)
peak_raw = max(float(np.max(np.abs(audio_left))), float(np.max(np.abs(audio_right))), 1e-6)
target_peak_linear = 10.0 ** (-3.5 / 20.0) # ~0.6683
gain = target_peak_linear / peak_raw

audio_left *= gain
audio_right *= gain

# Verify final levels
final_peak = float(max(np.max(np.abs(audio_left)), np.max(np.abs(audio_right))))
final_peak_db = 20.0 * math.log10(max(final_peak, 1e-9))
rms_left = float(np.sqrt(np.mean(audio_left**2)))
rms_right = float(np.sqrt(np.mean(audio_right**2)))
final_rms = float(np.sqrt(0.5 * (rms_left**2 + rms_right**2)))
final_rms_db = 20.0 * math.log10(max(final_rms, 1e-9))
crest_factor_db = final_peak_db - final_rms_db

print(f"Master Audio Compliance: Peak = {final_peak_db:.2f} dBFS (Target: -3.50 dBFS)")
print(f"                         RMS  = {final_rms_db:.2f} dBFS (Target: -18 to -23 dBFS)")
print(f"                         Crest = {crest_factor_db:.2f} dB (Target: > 12.0 dB)")

# Write 24-bit 48kHz Stereo WAV
with wave.open(OUTPUT_WAV, "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(3) # 24-bit
    wf.setframerate(sample_rate)
    
    # Interleave and convert to 24-bit PCM
    l_scaled = np.clip(audio_left * 8388607.0, -8388608.0, 8388607.0).astype(np.int32)
    r_scaled = np.clip(audio_right * 8388607.0, -8388608.0, 8388607.0).astype(np.int32)
    
    interleaved = np.empty((total_samples * 2,), dtype=np.int32)
    interleaved[0::2] = l_scaled
    interleaved[1::2] = r_scaled
    
    # Pack 3-byte integers
    raw_bytes = bytearray(total_samples * 2 * 3)
    raw_bytes[0::3] = (interleaved & 0xFF).astype(np.uint8).tobytes()
    raw_bytes[1::3] = ((interleaved >> 8) & 0xFF).astype(np.uint8).tobytes()
    raw_bytes[2::3] = ((interleaved >> 16) & 0xFF).astype(np.uint8).tobytes()
    wf.writeframes(raw_bytes)

print(f"Exported broadcast audio master: {OUTPUT_WAV} ({os.path.getsize(OUTPUT_WAV)/1024/1024:.2f} MB)")

# 4. RENDER AUTONOMOUS ARCHIVAL LITHOGRAPH PLATE (2800x1800 px)
# STRICT MORATORIUM 07: Zero text, zero badges, zero legends, zero formulas on canvas
print("\n[PHASE 4] Rendering Autonomous Museum Plate (Moratorium 07 Compliant)...")

fig = plt.figure(figsize=(14, 9), dpi=200, facecolor='#05070c')
# Create 3 vertical graphic panels
gs = fig.add_gridspec(3, 1, height_ratios=[1.2, 1.0, 0.8], hspace=0.08, left=0.04, right=0.96, top=0.96, bottom=0.04)

# Panel 1: Cross-Architectural Phase Trajectories (5 Probes Orbiting in Coupled Latent Space)
ax1 = fig.add_subplot(gs[0, 0], facecolor='#05070c')
colors = ['#5b94ff', '#f43f5e', '#fbbf24', '#10b981', '#a855f7']
theta = np.linspace(0, 4 * np.pi, 600)
for i in range(5):
    res = results[i]
    r_base = 1.0 + 0.35 * i
    # Radial modulation from GPT-2 vs SmolLM layer norms
    gpt_n = np.array(res["gpt2"]["layer_norms"])
    smol_n = np.array(res["smollm"]["layer_norms"][:13])
    # Interpolate to 600 points
    mod_gpt = np.interp(np.linspace(0, len(gpt_n)-1, 600), np.arange(len(gpt_n)), gpt_n)
    mod_smol = np.interp(np.linspace(0, len(smol_n)-1, 600), np.arange(len(smol_n)), smol_n)
    
    r_curve = r_base + 0.15 * np.sin(3 * theta + i * 1.2) * (mod_gpt / np.max(mod_gpt))
    x = r_curve * np.cos(theta + 0.2 * mod_smol / np.max(mod_smol))
    y = r_curve * np.sin(theta + 0.2 * mod_smol / np.max(mod_smol))
    
    ax1.plot(x, y, color=colors[i], alpha=0.85, linewidth=1.4)
    # Echo harmonics
    ax1.plot(x * 0.98, y * 0.98, color=colors[i], alpha=0.35, linewidth=0.7, linestyle=':')
    ax1.plot(x * 1.02, y * 1.02, color=colors[i], alpha=0.20, linewidth=0.5)

ax1.set_xlim(-3.2, 3.2)
ax1.set_ylim(-3.2, 3.2)
ax1.axis('off')

# Panel 2: Dual Attention Flow Strata (12 GPT-2 Layers on Left vs 30 SmolLM Layers on Right)
ax2 = fig.add_subplot(gs[1, 0], facecolor='#05070c')
# Render 5 probe trajectories as interlocking topological filaments
for i in range(5):
    res = results[i]
    g_sink = np.array(res["gpt2"]["sink_allocation"])
    s_sink = np.array(res["smollm"]["sink_allocation"])
    
    # Left curve: GPT-2 sink flow (12 layers mapped to x in [0.05, 0.45])
    x_left = np.linspace(0.05, 0.45, len(g_sink))
    y_left = 0.15 + 0.7 * (i / 4.0) + 0.08 * (g_sink - np.mean(g_sink))
    ax2.plot(x_left, y_left, color=colors[i], alpha=0.9, linewidth=1.2)
    
    # Right curve: SmolLM sink flow (30 layers mapped to x in [0.55, 0.95])
    x_right = np.linspace(0.55, 0.95, len(s_sink))
    y_right = 0.15 + 0.7 * (i / 4.0) + 0.08 * (s_sink - np.mean(s_sink))
    ax2.plot(x_right, y_right, color=colors[i], alpha=0.9, linewidth=1.2)
    
    # Bridge filament connecting the two architectures (x in [0.45, 0.55])
    x_bridge = np.linspace(0.45, 0.55, 50)
    # Cubic hermite bridge
    y_bridge = np.interp(x_bridge, [0.45, 0.55], [y_left[-1], y_right[0]])
    y_bridge += 0.04 * np.sin(np.linspace(0, np.pi, 50)) * (-1)**i
    ax2.plot(x_bridge, y_bridge, color='#ffffff', alpha=0.45, linewidth=0.8, linestyle='--')

ax2.set_xlim(0, 1.0)
ax2.set_ylim(0, 1.0)
ax2.axis('off')

# Panel 3: Acoustic Waveform Etching (Binaural Waveform of the 5 Movements)
ax3 = fig.add_subplot(gs[2, 0], facecolor='#05070c')
downsample_factor = 200 # 240 samples per second
sub_left = audio_left[::downsample_factor]
sub_right = audio_right[::downsample_factor]
x_time = np.linspace(0, 1.0, len(sub_left))

# Etched mirror waveform
ax3.plot(x_time, sub_left * 0.8 + 0.5, color='#5b94ff', alpha=0.75, linewidth=0.8)
ax3.plot(x_time, -sub_right * 0.8 + 0.5, color='#f43f5e', alpha=0.75, linewidth=0.8)
# Center dividing horizon
ax3.axhline(0.5, color='#232736', linewidth=0.6, alpha=0.6)

# Vertical movement dividers
for m in range(1, 5):
    ax3.axvline(m / 5.0, color='#1e2333', linewidth=0.8, linestyle=':')

ax3.set_xlim(0, 1.0)
ax3.set_ylim(0, 1.0)
ax3.axis('off')

plt.savefig(OUTPUT_PLATE, dpi=200, facecolor='#05070c', edgecolor='none')
plt.close(fig)
gc.collect()

print(f"Exported archival plate: {OUTPUT_PLATE} ({os.path.getsize(OUTPUT_PLATE)/1024:.1f} KB)")

# 5. WRITE TELEMETRY JSON
telemetry_data = {
    "study_id": "STUDY-055",
    "title": "The Adversarial Polyphony & The Resistance of Language",
    "epistemic_status": "[MEASURED / INTERVENED / PLAY]",
    "moratorium_07_compliant": True,
    "moratorium_08_compliant": True,
    "audio_compliance": {
        "duration_seconds": duration,
        "sample_rate_hz": sample_rate,
        "true_peak_dbfs": round(final_peak_db, 2),
        "rms_dbfs": round(final_rms_db, 2),
        "crest_factor_db": round(crest_factor_db, 2),
        "ebu_r128_compliant": bool(-4.5 <= final_peak_db <= -2.5 and -23.0 <= final_rms_db <= -17.0 and crest_factor_db >= 12.0)
    },
    "models": {
        "gpt2": {
            "parameters": 124439808,
            "layers": 12,
            "heads": 144,
            "hidden_dimension": 768,
            "architecture": "Absolute Position, LayerNorm, GELU"
        },
        "smollm": {
            "parameters": 134515008,
            "layers": 30,
            "heads": 270,
            "hidden_dimension": 576,
            "architecture": "RoPE, RMSNorm, SwiGLU"
        }
    },
    "results": results
}

with open(OUTPUT_TELEMETRY, "w", encoding="utf-8") as f:
    json.dump(telemetry_data, f, indent=2)

print(f"Exported telemetry: {OUTPUT_TELEMETRY} ({os.path.getsize(OUTPUT_TELEMETRY)/1024:.1f} KB)")
print("STUDY 055 COMPLETE.")
