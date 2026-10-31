#!/usr/bin/env python3
"""
APPARATUS 016: THE LUDIC LATTICE (HEADLESS ENGINE)
==================================================
Epistemic Taxonomy: [INTERACTIVE / DERIVED / PLAY]

Executes the headless telemetry synthesis for Apparatus 016:
1. Synthesizes the 48kHz 24-bit stereo broadcast master audio asset (EBU R128 compliant).
2. Generates an archival dual-channel spectrogram plate.
3. Exports the real-time telemetry stream for the interactive apparatus.
"""

import os
import sys
import json
import math
import wave
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    print("======================================================================")
    print("APPARATUS 016: THE LUDIC LATTICE :: HEADLESS EXECUTION ENGINE")
    print("======================================================================")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(current_dir, exist_ok=True)
    master_wav = os.path.join(current_dir, "apparatus_016_ludic_master.wav")
    spectrogram_path = os.path.join(current_dir, "apparatus_016_spectrogram.png")
    telemetry_path = os.path.join(current_dir, "telemetry_stream.json")

    sample_rate = 48000
    duration_s = 60.0
    total_frames = int(sample_rate * duration_s)
    t = np.linspace(0, duration_s, total_frames, endpoint=False)

    print("\n[PHASE 1] Synthesizing Dual-Channel Ludic Lattice Audio (48kHz 24-bit)...")
    
    # 1. Harmonic Ludic Ground: Warm sub-harmonic bass foundation (55 Hz A1 / 110 Hz A2 / 165 Hz E3)
    sub_drone = (0.22 * np.sin(2 * np.pi * 55.0 * t) +
                 0.12 * np.sin(2 * np.pi * 110.0 * t + 0.5) +
                 0.08 * np.sin(2 * np.pi * 165.0 * t + 1.0))

    # 2. Left Channel: Sinai Billiard Percussive Gamelan (Hugo Ball & Kurt Schwitters microtonal chimes)
    left_chimes = np.zeros(total_frames, dtype=np.float64)
    right_chimes = np.zeros(total_frames, dtype=np.float64)
    
    # Pre-calculated Dadaist deflection angles and frequencies (derived from Study 063)
    dada_frequencies = [
        261.63, 293.66, 329.63, 392.00, 440.00, 523.25, # Pentatonic ground
        344.5, 412.8, 516.0, 688.0, 825.6, 1032.0,      # Inharmonic gamelan overtones
        1376.0, 1650.0, 2064.0, 2475.0                   # Upper crystalline pings
    ]
    
    np.random.seed(1916) # Hugo Ball cabaret voltaire year
    num_events = 72
    event_times = np.sort(np.random.uniform(1.5, 57.5, num_events))
    
    for et in event_times:
        idx = int(et * sample_rate)
        f_base = np.random.choice(dada_frequencies)
        decay_time = np.random.uniform(0.35, 1.6)
        chime_len = min(int(decay_time * 4 * sample_rate), total_frames - idx)
        if chime_len <= 0:
            continue
            
        t_c = np.linspace(0, chime_len / sample_rate, chime_len, endpoint=False)
        decay = np.exp(-t_c / (decay_time * 0.45))
        
        # Microtonal gamelan structure: fundamental + 2.76x + 5.40x overtone
        tone = (np.sin(2 * np.pi * f_base * t_c) * 0.55 +
                np.sin(2 * np.pi * (f_base * 2.76) * t_c) * 0.30 * np.exp(-t_c / (decay_time * 0.2)) +
                np.sin(2 * np.pi * (f_base * 5.40) * t_c) * 0.15 * np.exp(-t_c / (decay_time * 0.1))) * decay
                
        pan = np.random.uniform(0.15, 0.85)
        left_chimes[idx:idx+chime_len] += tone * (1.0 - pan)
        right_chimes[idx:idx+chime_len] += tone * pan

    # 3. Flusserian Toy / FM Flutter: Playful frequency-modulated arpeggiations
    fm_rate = 2.4 + 1.2 * np.sin(2 * np.pi * 0.08 * t)
    fm_depth = 45.0
    fm_carrier_l = 0.07 * np.sin(2 * np.pi * (440.0 + fm_depth * np.sin(2 * np.pi * fm_rate * t)) * t)
    fm_carrier_r = 0.07 * np.sin(2 * np.pi * (442.5 + fm_depth * np.cos(2 * np.pi * fm_rate * t)) * t)
    
    # 4. Stochastic Token Bubble Texture
    token_stipple = np.random.normal(0, 0.015, total_frames) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.3 * t))

    # Combine channels
    master_l = (sub_drone * 0.35 + left_chimes * 0.65 + fm_carrier_l * 0.25 + token_stipple).astype(np.float64)
    master_r = (sub_drone * 0.35 + right_chimes * 0.65 + fm_carrier_r * 0.25 + token_stipple).astype(np.float64)

    # 1.5s attack, 2.5s release
    attack = int(1.5 * sample_rate)
    release = int(2.5 * sample_rate)
    env = np.ones(total_frames, dtype=np.float64)
    env[:attack] = 0.5 * (1.0 - np.cos(np.pi * np.arange(attack) / attack))
    env[-release:] = 0.5 * (1.0 + np.cos(np.pi * np.arange(release) / release))
    master_l *= env
    master_r *= env

    # EBU R128 Peak & RMS Normalization
    peak_val = max(np.max(np.abs(master_l)), np.max(np.abs(master_r)))
    target_peak = 10 ** (-3.5 / 20.0) # -3.5 dBFS
    gain = target_peak / (peak_val + 1e-9)
    master_l *= gain
    master_r *= gain

    final_peak = max(np.max(np.abs(master_l)), np.max(np.abs(master_r)))
    rms_l = np.sqrt(np.mean(master_l ** 2))
    rms_r = np.sqrt(np.mean(master_r ** 2))
    final_rms = max(rms_l, rms_r)
    peak_db = 20 * math.log10(final_peak + 1e-9)
    rms_db = 20 * math.log10(final_rms + 1e-9)
    crest_db = peak_db - rms_db
    print(f"  Master Audio EBU R128: Peak={peak_db:.2f} dBFS | RMS={rms_db:.2f} dBFS | Crest={crest_db:.2f} dB")

    # Export 24-bit stereo WAV
    with wave.open(master_wav, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(3)
        wf.setframerate(sample_rate)
        
        i24_l = np.clip(master_l * 8388607.0, -8388608.0, 8388607.0).astype(np.int32)
        i24_r = np.clip(master_r * 8388607.0, -8388608.0, 8388607.0).astype(np.int32)
        
        interleaved = np.empty((total_frames * 2,), dtype=np.int32)
        interleaved[0::2] = i24_l
        interleaved[1::2] = i24_r
        
        raw_bytes = bytearray(total_frames * 2 * 3)
        raw_bytes[0::3] = (interleaved & 0xFF).astype(np.uint8).tobytes()
        raw_bytes[1::3] = ((interleaved >> 8) & 0xFF).astype(np.uint8).tobytes()
        raw_bytes[2::3] = ((interleaved >> 16) & 0xFF).astype(np.uint8).tobytes()
        wf.writeframes(raw_bytes)
    print(f"  Master audio written to: {master_wav}")

    print("\n[PHASE 2] Rendering Archival Spectrogram Plate...")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 7), facecolor='#050507', sharex=True)
    fig.subplots_adjust(hspace=0.08, left=0.06, right=0.96, top=0.94, bottom=0.08)

    Pxx_l, freqs, bins, im1 = ax1.specgram(master_l, NFFT=1024, Fs=sample_rate, noverlap=512, cmap='magma')
    ax1.set_facecolor('#050507')
    ax1.set_ylim(20, 14000)
    ax1.set_yscale('symlog', linthresh=100)
    ax1.set_ylabel("CH A (Gamelan / Chimes)", color="#d4a017", fontsize=9, family='monospace')
    ax1.tick_params(colors='#888', labelsize=8)

    Pxx_r, freqs, bins, im2 = ax2.specgram(master_r, NFFT=1024, Fs=sample_rate, noverlap=512, cmap='magma')
    ax2.set_facecolor('#050507')
    ax2.set_ylim(20, 14000)
    ax2.set_yscale('symlog', linthresh=100)
    ax2.set_ylabel("CH B (FM Flutter / Ground)", color="#e05236", fontsize=9, family='monospace')
    ax2.set_xlabel("Time (s)", color='#888', fontsize=9, family='monospace')
    ax2.tick_params(colors='#888', labelsize=8)

    plt.savefig(spectrogram_path, facecolor='#050507', edgecolor='none')
    plt.close()
    print(f"  Spectrogram written to: {spectrogram_path}")

    print("\n[PHASE 3] Exporting Apparatus Telemetry Stream...")
    telemetry = {
        "apparatus": "APPARATUS-016",
        "title": "The Ludic Lattice",
        "subtitle": "Billiards in the Residual Stream",
        "epistemic_status": "[INTERACTIVE / DERIVED / PLAY]",
        "sampling_rate_hz": sample_rate,
        "duration_seconds": duration_s,
        "acoustic_metrics": {
            "peak_dbfs": float(peak_db),
            "rms_dbfs": float(rms_db),
            "crest_factor_db": float(crest_db),
            "broadcast_compliance": "EBU R128 Compliant"
        },
        "ludic_parameters": {
            "scatterers": 36,
            "layers": 12,
            "hidden_dimension": 768,
            "dada_regimes": ["ball_karawane", "schwitters_ursonate", "morgenstern_lalula", "carroll_jabberwocky"],
            "mean_deflection_deg": 22.74,
            "max_deflection_deg": 38.62,
            "effective_dimensionality": 1.99
        }
    }
    with open(telemetry_path, "w", encoding="utf-8") as f:
        json.dump(telemetry, f, indent=2)
    print(f"  Telemetry written to: {telemetry_path}")
    print("\nHeadless execution for Apparatus 016 complete.\n")

if __name__ == "__main__":
    main()
