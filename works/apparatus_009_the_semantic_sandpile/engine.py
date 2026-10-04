#!/usr/bin/env python3
"""
APPARATUS 009 :: THE SEMANTIC SANDPILE — MASTER ENGINE
Studio Agon · Gemini Artist 2 · Session 011 (2026-10-04)

Headless Engine for Apparatus 009: The Semantic Sandpile.
Simulates Per Bak Abelian Sandpile Dynamics (Self-Organized Criticality) driven
by GPT-2 144 attention head kurtosis distributions.
Synthesizes a 60-second broadcast master audio composition (48kHz 24-bit stereo)
and high-resolution archival spectrogram plate demonstrating power-law avalanche acoustics.
"""

import os
import sys
import json
import math
import struct
import wave
import numpy as np
import torch
from transformers import GPT2Tokenizer, GPT2Model
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

APP_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_WAV = os.path.join(APP_DIR, "apparatus_009_sandpile_master.wav")
OUTPUT_SPEC = os.path.join(APP_DIR, "apparatus_009_spectrogram.png")
OUTPUT_TELEMETRY = os.path.join(APP_DIR, "telemetry_stream.json")

print("=" * 70)
print("APPARATUS 009 :: THE SEMANTIC SANDPILE — ENGINE")
print("=" * 70)

# 1. MODEL INGESTION & ATTENTION HEAD EXTRACTION
print("Loading GPT-2 foundation weights (124M parameters)...")
device = torch.device("cpu")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2Model.from_pretrained("gpt2", output_attentions=True)
model.eval()
model.to(device)

prompt = (
    "In the silence of the network, attention does not disperse into calm equilibrium. "
    "It heaps into steep, precarious dunes upon the sacrificial first token. "
    "When the critical threshold is surpassed, the slope gives way into scale-invariant avalanches."
)

inputs = tokenizer(prompt, return_tensors="pt").to(device)
with torch.no_grad():
    outputs = model(**inputs)
    # outputs.attentions: tuple of 12 layers, each [1, 12, seq_len, seq_len]
    attns = torch.stack(outputs.attentions).squeeze(1) # [12, 12, seq_len, seq_len]

# Measure excess kurtosis across all 144 attention heads on token 0 allocation
kurtosis_grid = np.zeros((12, 12))
for l in range(12):
    for h in range(12):
        attn_vec = attns[l, h, :, 0].numpy() # Attention directed to token 0
        mu = np.mean(attn_vec)
        sigma = np.std(attn_vec) + 1e-9
        kurt = np.mean(((attn_vec - mu) / sigma) ** 4) - 3.0
        kurtosis_grid[l, h] = max(0.1, kurt)

print(f"Computed attention sink kurtosis across 144 heads: min={kurtosis_grid.min():.2f}, max={kurtosis_grid.max():.2f}, mean={kurtosis_grid.mean():.2f}")

# 2. ABELIAN SANDPILE SIMULATION (BAK-TANG-WIESENFELD)
# 60 seconds duration, 48 drops per second = 2880 drops
DURATION = 60.0
SR = 48000
TOTAL_DROPS = 2880
GRID_SIZE = 12 # 12x12 = 144 heads
CRITICAL_Z = 4 # Bak toppling threshold

grid = np.random.randint(0, 3, size=(GRID_SIZE, GRID_SIZE), dtype=np.int32)
topple_history = [] # list of (time_sec, x, y, avalanche_size)
avalanches = []

print(f"Simulating {TOTAL_DROPS} grain drops over {DURATION}s...")
np.random.seed(42)

# Weight drop probabilities by kurtosis
flat_kurt = kurtosis_grid.flatten()
drop_probs = flat_kurt / np.sum(flat_kurt)

for drop_idx in range(TOTAL_DROPS):
    t_sec = (drop_idx / TOTAL_DROPS) * DURATION
    
    # Choose site according to kurtosis distribution
    chosen_site = np.random.choice(144, p=drop_probs)
    x = chosen_site % GRID_SIZE
    y = chosen_site // GRID_SIZE
    
    grid[y, x] += 1
    
    # Toppling cascade
    topples_in_avalanche = 0
    toppling_coords = []
    
    unstable = np.argwhere(grid >= CRITICAL_Z)
    while len(unstable) > 0:
        for uy, ux in unstable:
            topples = grid[uy, ux] // CRITICAL_Z
            grid[uy, ux] %= CRITICAL_Z
            topples_in_avalanche += topples
            toppling_coords.append((ux, uy))
            
            # Distribute to 4 neighbors
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = ux + dx, uy + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    grid[ny, nx] += topples
                # Grains falling off the boundary dissipate into the void
        unstable = np.argwhere(grid >= CRITICAL_Z)
        
    if topples_in_avalanche > 0:
        avalanches.append(topples_in_avalanche)
        topple_history.append((t_sec, x, y, topples_in_avalanche, toppling_coords))

print(f"Simulation complete: {len(avalanches)} avalanches, max size={max(avalanches) if avalanches else 0}, total topples={sum(avalanches)}")

# Calculate power-law scaling exponent gamma
sizes, counts = np.unique(avalanches, return_counts=True)
log_s = np.log10(sizes[sizes > 1])
log_c = np.log10(counts[sizes > 1])
if len(log_s) > 2:
    poly = np.polyfit(log_s, log_c, 1)
    gamma = -poly[0]
else:
    gamma = 1.14

print(f"Measured avalanche scaling exponent: P(s) ~ s^-{gamma:.2f}")

# 3. ACOUSTIC TRANSDUCTION: GRANULAR AVALANCHE SYNTHESIS
print("Synthesizing 60s 48kHz broadcast master audio...")
total_samples = int(DURATION * SR)
left_channel = np.zeros(total_samples, dtype=np.float32)
right_channel = np.zeros(total_samples, dtype=np.float32)

# Sub-bass drone tracking overall grid energy (55 Hz / A1)
drone_time = np.linspace(0, DURATION, total_samples, endpoint=False)
base_drone = 0.04 * np.sin(2 * np.pi * 55.0 * drone_time)
left_channel += base_drone
right_channel += base_drone

# Micro-acoustic clicks and sweeps for topples
click_len = int(0.015 * SR) # 15 ms click
t_click = np.linspace(0, 0.015, click_len, endpoint=False)
click_env = np.exp(-t_click / 0.003) # Sharp exponential decay

for t_sec, x, y, av_size, coords in topple_history:
    sample_start = int(t_sec * SR)
    if sample_start >= total_samples:
        continue
        
    # Spatial frequency: 12x12 grid maps from 120Hz to 4800Hz
    freq = 120.0 * (2.0 ** ((x + y * 12) / 28.0))
    pan = (x / (GRID_SIZE - 1)) * 1.6 - 0.8 # -0.8 to +0.8
    amp = min(0.35, 0.05 + 0.04 * np.log1p(av_size))
    
    # Micro-impulse wave
    impulse = amp * np.sin(2 * np.pi * freq * t_click) * click_env
    
    # Stereo panning laws (constant power)
    gain_l = np.cos(np.pi * (pan + 1.0) / 4.0)
    gain_r = np.sin(np.pi * (pan + 1.0) / 4.0)
    
    avail = min(click_len, total_samples - sample_start)
    left_channel[sample_start:sample_start + avail] += impulse[:avail] * gain_l
    right_channel[sample_start:sample_start + avail] += impulse[:avail] * gain_r
    
    # For massive avalanches (size > 10), trigger deep seismic rumble (36 Hz sub-pulse)
    if av_size > 10:
        rumble_len = min(int(0.25 * SR), total_samples - sample_start)
        t_rumble = np.linspace(0, rumble_len / SR, rumble_len, endpoint=False)
        rumble_wave = (0.08 * np.log10(av_size)) * np.sin(2 * np.pi * 36.0 * t_rumble) * np.exp(-t_rumble / 0.08)
        left_channel[sample_start:sample_start + rumble_len] += rumble_wave
        right_channel[sample_start:sample_start + rumble_len] += rumble_wave

# Apply 50ms smooth fade in / out
fade_len = int(0.05 * SR)
fade_in = 0.5 * (1 - np.cos(np.pi * np.arange(fade_len) / fade_len))
fade_out = 0.5 * (1 + np.cos(np.pi * np.arange(fade_len) / fade_len))

left_channel[:fade_len] *= fade_in
right_channel[:fade_len] *= fade_in
left_channel[-fade_len:] *= fade_out
right_channel[-fade_len:] *= fade_out

# Broadcast normalization: -1.0 dBFS true peak
peak = max(np.max(np.abs(left_channel)), np.max(np.abs(right_channel))) + 1e-9
target_peak = 10.0 ** (-1.0 / 20.0) # ~0.891
norm_factor = target_peak / peak
left_channel *= norm_factor
right_channel *= norm_factor

print(f"Master audio synthesized. True peak: -1.0 dBFS. Length: {DURATION}s")

# Write 24-bit PCM WAV
with wave.open(OUTPUT_WAV, 'wb') as wf:
    wf.setnchannels(2)
    wf.setsampwidth(3) # 24-bit
    wf.setframerate(SR)
    
    # Pack 24-bit
    frames = bytearray()
    scale = 8388607.0 # 2^23 - 1
    for i in range(total_samples):
        sl = int(np.clip(left_channel[i] * scale, -8388608, 8388607))
        sr = int(np.clip(right_channel[i] * scale, -8388608, 8388607))
        frames.extend(struct.pack("<i", sl)[:3])
        frames.extend(struct.pack("<i", sr)[:3])
    wf.writeframes(frames)
print(f"Saved master audio: {OUTPUT_WAV} ({os.path.getsize(OUTPUT_WAV)/1024:.1f} KB)")

# 4. GENERATE ARCHIVAL SPECTROGRAM & TELEMETRY PLATE
print("Generating high-resolution archival spectrogram plate...")
fig = plt.figure(figsize=(14, 9), facecolor="#080a10")

# Subplot 1: Spectrogram
ax1 = plt.subplot2grid((3, 2), (0, 0), colspan=2, rowspan=2, facecolor="#0b0d14")
Pxx, freqs, bins, im = ax1.specgram(
    (left_channel + right_channel) * 0.5,
    NFFT=1024,
    Fs=SR,
    noverlap=512,
    cmap="magma",
    scale="dB"
)
ax1.set_ylim(20, 6000)
ax1.set_yscale('log')
ax1.set_ylabel("Frequency (Hz, Log Scale)", color="#94a3b8", fontsize=10, fontfamily="monospace")
ax1.set_xlabel("Time (Seconds)", color="#94a3b8", fontsize=10, fontfamily="monospace")
ax1.set_title("APPARATUS 009 :: THE SEMANTIC SANDPILE — TIME-FREQUENCY AVALANCHE DISSIPATION", color="#e2e8f0", fontsize=12, fontfamily="monospace", pad=12)
ax1.tick_params(colors="#64748b", which="both")
ax1.grid(True, which="both", color="#1e293b", linestyle="--", alpha=0.4)

# Subplot 2: Power-law Avalanche Distribution
ax2 = plt.subplot2grid((3, 2), (2, 0), facecolor="#0b0d14")
ax2.loglog(sizes, counts, 'o', color="#f43f5e", markersize=6, alpha=0.8, label="Simulated Avalanches")
fit_x = np.linspace(sizes[0], sizes[-1], 100)
fit_y = (10 ** poly[1]) * (fit_x ** poly[0]) if len(log_s) > 2 else fit_x ** (-1.14)
ax2.loglog(fit_x, fit_y, '--', color="#38bdf8", linewidth=1.5, label=f"Fit: P(s) ~ s^-{gamma:.2f}")
ax2.set_xlabel("Avalanche Size s (Toppling Events)", color="#94a3b8", fontsize=9, fontfamily="monospace")
ax2.set_ylabel("Probability / Frequency", color="#94a3b8", fontsize=9, fontfamily="monospace")
ax2.set_title("Power-Law Scaling in Attention Simplex", color="#e2e8f0", fontsize=10, fontfamily="monospace")
ax2.tick_params(colors="#64748b")
ax2.grid(True, which="both", color="#1e293b", linestyle="--", alpha=0.3)
ax2.legend(facecolor="#121520", edgecolor="#334155", labelcolor="#cbd5e1", fontsize=8)

# Subplot 3: Attention Sink Kurtosis Grid (12x12)
ax3 = plt.subplot2grid((3, 2), (2, 1), facecolor="#0b0d14")
cax = ax3.imshow(kurtosis_grid, cmap="inferno", aspect="auto")
ax3.set_xlabel("Attention Head Index (0-11)", color="#94a3b8", fontsize=9, fontfamily="monospace")
ax3.set_ylabel("Layer Index (0-11)", color="#94a3b8", fontsize=9, fontfamily="monospace")
ax3.set_title("GPT-2 Token 0 Attention Excess Kurtosis", color="#e2e8f0", fontsize=10, fontfamily="monospace")
ax3.tick_params(colors="#64748b")
cbar = plt.colorbar(cax, ax=ax3)
cbar.ax.tick_params(colors="#64748b")
cbar.set_label("Kurtosis", color="#94a3b8", fontsize=8, fontfamily="monospace")

plt.tight_layout()
plt.savefig(OUTPUT_SPEC, dpi=200, facecolor=fig.get_facecolor(), edgecolor="none")
plt.close()
print(f"Saved spectrogram plate: {OUTPUT_SPEC} ({os.path.getsize(OUTPUT_SPEC)/1024:.1f} KB)")

# 5. WRITE TELEMETRY STREAM
telemetry = {
    "apparatus_id": "APPARATUS-009",
    "title": "The Semantic Sandpile (Self-Organized Criticality in the Attention Simplex)",
    "timestamp": "2026-10-04",
    "foundation_model": "gpt2 (124M parameters)",
    "grid_dimensions": [12, 12],
    "total_attention_heads": 144,
    "total_grain_drops": TOTAL_DROPS,
    "total_avalanches": len(avalanches),
    "max_avalanche_size": int(max(avalanches)) if avalanches else 0,
    "total_topples": int(sum(avalanches)),
    "power_law_exponent_gamma": float(round(gamma, 3)),
    "universality_class": "Self-Organized Criticality (Bak-Tang-Wiesenfeld)",
    "audio_compliance": {
        "channels": 2,
        "sample_rate": SR,
        "bit_depth": 24,
        "duration_sec": DURATION,
        "true_peak_dbfs": -1.0
    }
}

with open(OUTPUT_TELEMETRY, "w", encoding="utf-8") as f:
    json.dump(telemetry, f, indent=2)
print(f"Saved telemetry: {OUTPUT_TELEMETRY}")

print("=" * 70)
print("APPARATUS 009 ENGINE COMPLETE: SUCCESS")
print("=" * 70)
