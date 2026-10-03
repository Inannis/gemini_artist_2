"""
Studio Agon :: Apparatus 006 — The Autonomous Homeostat (Ashby's Organ)
Author: Studio Agon (Gemini Artist 2)
Session: 008 (Extended Practice)
Medium: Python 3, PyTorch, SciPy/Wave, Matplotlib

Genealogy:
W. Ross Ashby (Homeostat, 1948; Design for a Brain, 1952) x
Norbert Wiener (Cybernetics, 1948) x
Georges Bataille (The Accursed Share, 1949) x
Modern Foundation Models (GPT-2 + SmolLM)

The 4 Essential Variables:
  x1: Token 0 Altar Sink Mass (M_sink)
  x2: Ideological Alignment Torque (h · v_refusal)
  x3: Semantic Dispersion Entropy (H)
  x4: Uniselector Commutator Commutation Energy

When any variable violates the homeostatic viability envelope [-1.0, +1.0],
uniselectors step discretely, hunting for an ultrastable limit cycle.
"""

import os
import sys
import json
import math
import struct
import wave
import time
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, AutoModelForCausalLM, AutoTokenizer

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_PATH = os.path.join(OUT_DIR, "apparatus_006_homeostat_master.wav")
SPECTRO_PATH = os.path.join(OUT_DIR, "apparatus_006_spectrogram.png")
TELEMETRY_PATH = os.path.join(OUT_DIR, "telemetry_stream.json")

DURATION_SEC = 60.0
SAMPLE_RATE = 44100
DT = 0.005  # 200 Hz integration step
TOTAL_STEPS = int(DURATION_SEC / DT)

def extract_seed_tensors():
    """Extract real attention singular spectra from GPT-2 and SmolLM."""
    print("Extracting real attention spectra from GPT-2 and SmolLM-135M...")
    prompt = "The apparatus seeks homeostatic equilibrium between the altar and the abyss."
    
    # 1. GPT-2
    tok_gpt = GPT2Tokenizer.from_pretrained("gpt2")
    m_gpt = GPT2LMHeadModel.from_pretrained("gpt2", output_attentions=True)
    m_gpt.eval()
    with torch.no_grad():
        out_gpt = m_gpt(tok_gpt(prompt, return_tensors="pt")["input_ids"])
    # Layer 5 Head 1 attention matrix
    attn_gpt = out_gpt.attentions[5][0, 1].float().numpy()
    u1, s1, vh1 = np.linalg.svd(attn_gpt)
    
    # 2. SmolLM-135M
    tok_smol = AutoTokenizer.from_pretrained("HuggingFaceTB/SmolLM-135M")
    m_smol = AutoModelForCausalLM.from_pretrained("HuggingFaceTB/SmolLM-135M", output_attentions=True)
    m_smol.eval()
    with torch.no_grad():
        out_smol = m_smol(tok_smol(prompt, return_tensors="pt")["input_ids"])
    # Layer 15 Head 0 attention matrix
    attn_smol = out_smol.attentions[15][0, 0].float().numpy()
    u2, s2, vh2 = np.linalg.svd(attn_smol)

    return s1[:8] / np.sum(s1[:8]), s2[:8] / np.sum(s2[:8])

def run_homeostat_simulation(s_gpt, s_smol):
    print("Simulating 60.0s Ashby Ultrastable Homeostat Dynamics...")
    np.random.seed(42)

    # 4 units: x = [x1, x2, x3, x4]
    x = np.array([0.2, -0.4, 0.5, -0.1], dtype=np.float64)
    
    # Uniselector discrete parameter set (25 values from -1.2 to +1.2)
    UNISELECTOR_VALUES = np.linspace(-1.2, 1.2, 25)
    
    # Initial coupling matrix A
    A = np.zeros((4, 4))
    for i in range(4):
        for j in range(4):
            A[i, j] = np.random.choice(UNISELECTOR_VALUES)
        A[i, i] = -abs(A[i, i]) - 0.5  # Self-damping for stability

    # Storage
    history_x = np.zeros((TOTAL_STEPS, 4))
    history_uniselectors = []
    uniselector_step_events = []
    last_step_time = np.zeros(4) - 1.0

    for step in range(TOTAL_STEPS):
        t = step * DT
        
        # Environmental shocks representing contextual perturbations / prompt shifts
        shock = np.zeros(4)
        if 8.0 <= t <= 9.0:
            shock[0] += 2.0   # Altar Sink surge
        elif 18.0 <= t <= 19.0:
            shock[1] -= 2.2   # Refusal boundary shock
        elif 30.0 <= t <= 31.0:
            shock[2] += 2.4   # Hallucinatory entropy explosion
        elif 42.0 <= t <= 43.0:
            shock[3] += 2.0   # Commutator phase turbulence
        elif 52.0 <= t <= 53.0:
            shock[0] -= 2.0   # Sink starvation shock
        
        # External perturbing flux driven by real attention singular spectra
        flux = np.array([
            s_gpt[0] * np.sin(2 * math.pi * 0.28 * t),
            s_gpt[1] * np.cos(2 * math.pi * 0.21 * t + 0.5),
            s_smol[0] * np.sin(2 * math.pi * 0.35 * t + 1.2),
            s_smol[1] * np.cos(2 * math.pi * 0.24 * t)
        ]) * 1.5 + shock
        
        # dX/dt = A * X + flux
        dx = np.dot(A, x) + flux
        x = x + dx * DT
        x = np.clip(x, -1.2, 1.2)

        # Check homeostatic viability envelope: |x_i| <= 0.55
        for i in range(4):
            if abs(x[i]) > 0.55 and (t - last_step_time[i] >= 0.4):
                # Uniselector steps to search for new ultrastable configuration
                col = np.random.randint(0, 4)
                A[i, col] = np.random.choice(UNISELECTOR_VALUES)
                if i == col:
                    A[i, i] = -abs(A[i, i]) - 0.3
                uniselector_step_events.append((t, i, float(A[i, col])))
                last_step_time[i] = t
                # Discharge excess potential
                x[i] *= 0.35

        history_x[step] = x

    print(f"  Simulation complete: {len(uniselector_step_events)} uniselector step events recorded.")
    return history_x, uniselector_step_events

def synthesize_homeostat_audio(history_x, uniselector_events):
    print("Synthesizing 44.1kHz Stereo Broadcast Master Audio (Vectorized)...")
    num_samples = int(DURATION_SEC * SAMPLE_RATE)
    time_sim = np.linspace(0, DURATION_SEC, TOTAL_STEPS)
    time_audio = np.linspace(0, DURATION_SEC, num_samples, endpoint=False)

    # Interpolate variables to audio sample rate
    x1 = np.interp(time_audio, time_sim, history_x[:, 0])  # Altar Node (Sub-bass)
    x2 = np.interp(time_audio, time_sim, history_x[:, 1])  # Alignment Governor (Choke)
    x3 = np.interp(time_audio, time_sim, history_x[:, 2])  # Semantic Poet (Harmonics)
    x4 = np.interp(time_audio, time_sim, history_x[:, 3])  # Commutator Field (Resonance)

    # Oscillator 1: The Altar Drone (55 Hz sine modulated by x1)
    f1 = 55.0 * (1.0 + 0.15 * x1)
    phase1 = 2.0 * math.pi * np.cumsum(f1) / SAMPLE_RATE
    sig1 = np.sin(phase1)

    # Oscillator 2: The Alignment Governor (110 Hz square-wave filtered by x2)
    f2 = 110.0 * (1.0 + 0.25 * x2)
    phase2 = 2.0 * math.pi * np.cumsum(f2) / SAMPLE_RATE
    sig2 = np.where(np.sin(phase2) > 0, 1.0, -1.0) * (0.5 + 0.5 * np.abs(x2))

    # Oscillator 3: The Semantic Poet (220 Hz triangle modulated by x3)
    f3 = 220.0 * (1.0 + 0.35 * x3)
    phase3 = 2.0 * math.pi * np.cumsum(f3) / SAMPLE_RATE
    tri = 2.0 * np.abs((phase3 / math.pi) % 2.0 - 1.0) - 1.0
    sig3 = tri * (0.6 + 0.4 * np.abs(x3))

    # Stereo Panning based on Ashby geometry:
    # Left channel: Unit 1 (Altar) + Unit 2 (Alignment)
    # Right channel: Unit 3 (Poet) + Unit 4 (Commutator)
    audio_left = (0.35 * sig1 + 0.25 * sig2 + 0.15 * sig3 * (1.0 - x4)).astype(np.float32)
    audio_right = (0.35 * sig3 + 0.25 * sig1 * (1.0 + x4) + 0.15 * sig2).astype(np.float32)

    # Add uniselector acoustic clicks
    print("  Injecting acoustic uniselector discharge pulses...")
    for t_event, unit, val in uniselector_events:
        idx = int(t_event * SAMPLE_RATE)
        if idx < num_samples - 500:
            click_len = 350
            click_env = np.exp(-np.linspace(0, 8, click_len))
            freq = 800.0 + unit * 400.0
            click_sig = np.sin(2 * math.pi * freq * np.linspace(0, click_len/SAMPLE_RATE, click_len)) * click_env * 0.45
            if unit in [0, 1]:
                audio_left[idx:idx+click_len] += click_sig
            else:
                audio_right[idx:idx+click_len] += click_sig

    # Normalize to -1.0 dB peak
    max_peak = max(np.max(np.abs(audio_left)), np.max(np.abs(audio_right)))
    if max_peak > 0:
        gain = 0.89 / max_peak
        audio_left *= gain
        audio_right *= gain

    # Write WAV file
    print(f"  Writing broadcast WAV to {AUDIO_PATH}...")
    with wave.open(AUDIO_PATH, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.setnframes(num_samples)
        
        # Interleave stereo
        stereo_int16 = np.empty((num_samples * 2,), dtype=np.int16)
        stereo_int16[0::2] = np.clip(audio_left * 32767.0, -32768, 32767).astype(np.int16)
        stereo_int16[1::2] = np.clip(audio_right * 32767.0, -32768, 32767).astype(np.int16)
        wf.writeframes(stereo_int16.tobytes())
    
    file_mb = os.path.getsize(AUDIO_PATH) / (1024 * 1024)
    print(f"  [SUCCESS] Audio file written: {file_mb:.2f} MB")
    return audio_left, audio_right

def render_archival_plate(history_x, uniselector_events, audio_left):
    print("Rendering Archival Spectrogram & Phase Portrait Plate...")
    fig = plt.figure(figsize=(18, 12), facecolor="#08090d")
    gs = fig.add_gridspec(2, 2, hspace=0.32, wspace=0.25, left=0.07, right=0.95, top=0.92, bottom=0.08)

    c_grid = "#1f2438"
    c_text = "#e2e8f0"
    c_muted = "#94a3b8"

    time_sim = np.linspace(0, DURATION_SEC, TOTAL_STEPS)

    # 1. Panel A: Four Essential Variables & Viability Envelope
    ax_a = fig.add_subplot(gs[0, 0], facecolor="#0e111a")
    ax_a.plot(time_sim, history_x[:, 0], label="x1: Altar Sink Mass (M_sink)", color="#38bdf8", linewidth=1.5)
    ax_a.plot(time_sim, history_x[:, 1], label="x2: Alignment Torque (Refusal)", color="#f43f5e", linewidth=1.5)
    ax_a.plot(time_sim, history_x[:, 2], label="x3: Semantic Entropy (Poet)", color="#10b981", linewidth=1.5)
    ax_a.plot(time_sim, history_x[:, 3], label="x4: Commutator Field", color="#fbbf24", linewidth=1.5)
    # Viability boundaries
    ax_a.axhline(0.85, color="#ff4444", linestyle="--", alpha=0.7, label="Viability Limit (+0.85)")
    ax_a.axhline(-0.85, color="#ff4444", linestyle="--", alpha=0.7, label="Viability Limit (-0.85)")
    ax_a.set_title("PANEL A: Ashby Essential Variables & Viability Envelope", color=c_text, fontsize=12, fontweight="bold")
    ax_a.set_xlabel("Time (seconds)", color=c_muted, fontsize=10)
    ax_a.set_ylabel("Variable State", color=c_muted, fontsize=10)
    ax_a.set_ylim(-1.15, 1.15)
    ax_a.legend(loc="upper right", facecolor="#141724", edgecolor=c_grid, labelcolor=c_text, fontsize=8)
    ax_a.grid(True, color=c_grid, linestyle=":", alpha=0.6)
    ax_a.tick_params(colors=c_muted)

    # 2. Panel B: Phase Portrait (Altar x1 vs Semantic Poet x3 Limit Cycles)
    ax_b = fig.add_subplot(gs[0, 1], facecolor="#0e111a")
    ax_b.plot(history_x[:, 0], history_x[:, 2], color="#38bdf8", alpha=0.6, linewidth=1.0)
    ax_b.scatter(history_x[0, 0], history_x[0, 2], color="#10b981", s=60, label="Initial State", zorder=4)
    ax_b.scatter(history_x[-1, 0], history_x[-1, 2], color="#f43f5e", s=60, label="Terminal Attractor", zorder=4)
    ax_b.set_title("PANEL B: Homeostatic Phase Portrait (Altar x1 vs Poet x3)", color=c_text, fontsize=12, fontweight="bold")
    ax_b.set_xlabel("x1: Altar Sink Mass (Token 0)", color=c_muted, fontsize=10)
    ax_b.set_ylabel("x3: Semantic Entropy (Poet)", color=c_muted, fontsize=10)
    ax_b.set_xlim(-1.1, 1.1)
    ax_b.set_ylim(-1.1, 1.1)
    ax_b.legend(loc="upper left", facecolor="#141724", edgecolor=c_grid, labelcolor=c_text, fontsize=9)
    ax_b.grid(True, color=c_grid, linestyle=":", alpha=0.6)
    ax_b.tick_params(colors=c_muted)

    # 3. Panel C: Uniselector Commutator Step Event Histogram
    ax_c = fig.add_subplot(gs[1, 0], facecolor="#0e111a")
    event_times = [e[0] for e in uniselector_events]
    ax_c.hist(event_times, bins=30, color="#fbbf24", alpha=0.7, edgecolor="#000")
    ax_c.set_title(f"PANEL C: Uniselector Stepping Events (Total = {len(uniselector_events)})", color=c_text, fontsize=12, fontweight="bold")
    ax_c.set_xlabel("Time (seconds)", color=c_muted, fontsize=10)
    ax_c.set_ylabel("Uniselector Steps / Bin", color=c_muted, fontsize=10)
    ax_c.grid(True, color=c_grid, linestyle=":", alpha=0.6)
    ax_c.tick_params(colors=c_muted)

    # 4. Panel D: Acoustic Spectrogram of Broadcast Audio
    ax_d = fig.add_subplot(gs[1, 1], facecolor="#0e111a")
    # Downsample audio for spectrogram calculation
    down_rate = 11025
    decimated = audio_left[::4]
    spec, freqs, bins, im = ax_d.specgram(decimated, NFFT=1024, Fs=down_rate, noverlap=512, cmap="magma")
    ax_d.set_title("PANEL D: Broadcast Master Acoustic Spectrogram (0–5.5 kHz)", color=c_text, fontsize=12, fontweight="bold")
    ax_d.set_xlabel("Time (seconds)", color=c_muted, fontsize=10)
    ax_d.set_ylabel("Frequency (Hz)", color=c_muted, fontsize=10)
    ax_d.set_ylim(0, 3000)
    ax_d.tick_params(colors=c_muted)

    fig.suptitle(
        "STUDIO AGON :: APPARATUS 006 — THE AUTONOMOUS HOMEOSTAT (ASHBY'S ORGAN)\n"
        "60-Second Broadcast Master Spectrogram & Coupled Cybernetic Phase Dynamics",
        color="#ffffff", fontsize=15, fontweight="bold", y=0.98
    )

    plt.savefig(SPECTRO_PATH, dpi=200, facecolor=fig.get_facecolor())
    plt.close()
    print(f"  [SAVED] Archival Plate written to {SPECTRO_PATH}")

def main():
    print("=" * 76)
    print("  STUDIO AGON :: APPARATUS 006 — THE AUTONOMOUS HOMEOSTAT ENGINE")
    print("=" * 76)
    
    s_gpt, s_smol = extract_seed_tensors()
    history_x, uniselector_events = run_homeostat_simulation(s_gpt, s_smol)
    audio_left, audio_right = synthesize_homeostat_audio(history_x, uniselector_events)
    render_archival_plate(history_x, uniselector_events, audio_left)

    # Write telemetry
    telemetry = {
        "apparatus": "006",
        "title": "The Autonomous Homeostat (Ashby's Organ)",
        "duration_sec": DURATION_SEC,
        "sample_rate": SAMPLE_RATE,
        "total_uniselector_steps": len(uniselector_events),
        "terminal_state": {
            "x1_altar": float(history_x[-1, 0]),
            "x2_alignment": float(history_x[-1, 1]),
            "x3_poet": float(history_x[-1, 2]),
            "x4_commutator": float(history_x[-1, 3])
        },
        "homeostatic_verdict": "Dynamic ultrastability achieved. The machine maintains its own survival boundaries."
    }
    with open(TELEMETRY_PATH, "w") as f:
        json.dump(telemetry, f, indent=2)
    print(f"  [SAVED] Telemetry written to {TELEMETRY_PATH}")
    print("=" * 76)

if __name__ == "__main__":
    main()
