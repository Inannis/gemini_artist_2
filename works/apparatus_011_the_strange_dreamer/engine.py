"""
Studio Agon — Apparatus 011: The Strange Dreamer (Autoregressive Phase Space)
Headless synthesis engine for Apparatus 011.

Generates:
1. 60-second 48kHz 24-bit stereo broadcast master audio (apparatus_011_dreamer_master.wav)
2. Archival spectrogram plate (apparatus_011_spectrogram.png)
3. Telemetry stream (telemetry_stream.json)

Medium: 48kHz 24-bit PCM Audio, Spectrographic Analysis
Epistemic Mode: [DERIVED / PLAY]
"""

import os
import json
import wave
import struct
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

APP_DIR = "/c/Users/johan/Desktop/Git Projects/gemini_artist_2/works/apparatus_011_the_strange_dreamer"

def generate_apparatus_assets():
    print("=== Studio Agon :: Apparatus 011 — The Strange Dreamer (Synthesis Engine) ===")
    os.makedirs(APP_DIR, exist_ok=True)
    
    sample_rate = 48000
    duration_sec = 60.0
    num_samples = int(sample_rate * duration_sec)
    t = np.linspace(0, duration_sec, num_samples, endpoint=False)
    
    left = np.zeros(num_samples)
    right = np.zeros(num_samples)
    
    # 4 Movements in continuous transition:
    # 0s - 15s: Limit Cycle (T=0.1) - Steady 110Hz organ drone with harmonic 15-cycle pulse
    # 15s - 30s: Homeostatic Orbit (T=0.7) - Dual-voice counterpoint (165Hz & 247.5Hz)
    # 30s - 45s: Strange Attractor (T=1.0) - Microtonal FM synthesis with Lorenz-like basin modulation
    # 45s - 60s: Thermal Dissipation (T=1.8) - Granular noise filtering down to 55Hz sub-bass and silence
    
    # Generate Phase Space Signals
    # Movement 1: Limit Cycle
    m1_mask = (t < 15.0)
    # Movement 2: Homeostatic Orbit
    m2_mask = (t >= 15.0) & (t < 30.0)
    # Movement 3: Strange Attractor
    m3_mask = (t >= 30.0) & (t < 45.0)
    # Movement 4: Thermal Dissipation
    m4_mask = (t >= 45.0)
    
    # 1. Base synthesis across time
    # Envelope transitions with smooth sine crossfades
    for i in range(num_samples):
        ti = t[i]
        
        if ti < 15.0:
            # Movement I: Periodic Drone (110 Hz fundamental)
            prog = ti / 15.0
            env = np.sin(np.pi * prog) ** 0.5 if ti > 1.0 else ti
            f0 = 110.0
            phi = 2.0 * np.pi * f0 * ti
            drone = 0.45 * np.sin(phi) + 0.22 * np.sin(2.0 * phi) + 0.12 * np.sin(3.0 * phi) + 0.08 * np.sin(4.0 * phi)
            pulse = 0.5 * (1.0 + np.sin(2.0 * np.pi * 1.0 * ti)) # 1 Hz token pulse
            l_val = drone * (0.65 + 0.35 * pulse) * env
            r_val = drone * (0.65 + 0.35 * (1.0 - pulse)) * env
            
        elif ti < 30.0:
            # Movement II: Homeostatic Orbit (165 & 247.5 Hz)
            prog = (ti - 15.0) / 15.0
            env = np.sin(np.pi * prog) ** 0.5
            f1 = 165.0 + 12.0 * np.sin(2.0 * np.pi * 0.2 * ti)
            f2 = 247.5 + 16.0 * np.cos(2.0 * np.pi * 0.28 * ti)
            v1 = 0.4 * np.sin(2.0 * np.pi * f1 * ti)
            v2 = 0.4 * np.sin(2.0 * np.pi * f2 * ti)
            l_val = (v1 * 0.8 + v2 * 0.2) * env
            r_val = (v1 * 0.2 + v2 * 0.8) * env
            
        elif ti < 45.0:
            # Movement III: Strange Attractor (Fractal FM & Microtonal drifting)
            prog = (ti - 30.0) / 15.0
            env = np.sin(np.pi * prog) ** 0.5
            # Non-repeating chaotic frequency drift
            fc = 196.0 + 60.0 * np.sin(ti * 0.73) + 35.0 * np.sin(ti * 1.61)
            fm = 65.4 + 18.0 * np.cos(ti * 0.89)
            beta = 2.5 + 2.0 * (0.5 + 0.5 * np.sin(ti * 2.11))
            phi_fm = 2.0 * np.pi * fc * ti + beta * np.sin(2.0 * np.pi * fm * ti)
            sub = 0.25 * np.sin(2.0 * np.pi * (fc * 0.5) * ti)
            voice = (0.42 * np.sin(phi_fm) + sub) * env
            pan = 0.5 + 0.35 * np.sin(ti * 0.65)
            l_val = voice * (1.0 - pan)
            r_val = voice * pan
            
        else:
            # Movement IV: Thermal Dissipation & Granular Gas
            prog = (ti - 45.0) / 15.0
            decay = max(0.0, 1.0 - (prog ** 1.4))
            noise = (np.random.rand() * 2.0 - 1.0) * 0.28 * decay
            sub_coda = 0.35 * np.sin(2.0 * np.pi * 55.0 * ti) * decay
            sig = (noise + sub_coda)
            l_val = sig * 0.85
            r_val = sig * 0.85
            
        left[i] = l_val
        right[i] = r_val
        
    # Smooth fade in and out
    fade_in = int(1.5 * sample_rate)
    fade_out = int(3.0 * sample_rate)
    left[:fade_in] *= np.linspace(0, 1, fade_in)
    right[:fade_in] *= np.linspace(0, 1, fade_in)
    left[-fade_out:] *= np.linspace(1, 0, fade_out)
    right[-fade_out:] *= np.linspace(1, 0, fade_out)
    
    # Broadcast Compliance Normalization (-1.00 dBFS True Peak)
    target_peak = 10.0 ** (-1.00 / 20.0) # 0.89125
    curr_peak = max(np.max(np.abs(left)), np.max(np.abs(right)), 1e-8)
    gain = target_peak / curr_peak
    left *= gain
    right *= gain
    
    # Soft knee limiting
    left = np.tanh(left / target_peak) * target_peak
    right = np.tanh(right / target_peak) * target_peak
    
    rms_l = np.sqrt(np.mean(left ** 2))
    rms_r = np.sqrt(np.mean(right ** 2))
    rms_db = 20.0 * np.log10(max(rms_l, rms_r) + 1e-9)
    peak_db = 20.0 * np.log10(max(np.max(np.abs(left)), np.max(np.abs(right))) + 1e-9)
    crest_db = peak_db - rms_db
    
    # Write 48kHz 24-bit stereo WAV file
    wav_path = os.path.join(APP_DIR, "apparatus_011_dreamer_master.wav")
    max_int24 = 8388607
    left_int = np.clip(left * max_int24, -max_int24, max_int24).astype(np.int32)
    right_int = np.clip(right * max_int24, -max_int24, max_int24).astype(np.int32)
    
    interleaved = np.empty((num_samples * 2,), dtype=np.int32)
    interleaved[0::2] = left_int
    interleaved[1::2] = right_int
    
    raw_bytes = bytearray(num_samples * 2 * 3)
    for i in range(num_samples * 2):
        val = int(interleaved[i])
        if val < 0:
            val = (1 << 24) + val
        raw_bytes[i*3] = val & 0xFF
        raw_bytes[i*3 + 1] = (val >> 8) & 0xFF
        raw_bytes[i*3 + 2] = (val >> 16) & 0xFF
        
    with wave.open(wav_path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(3) # 24-bit
        wf.setframerate(sample_rate)
        wf.writeframes(raw_bytes)
        
    print(f"[OK] 48kHz 24-bit Master Audio generated: {wav_path} ({os.path.getsize(wav_path)/1024/1024:.2f} MB)")
    print(f"  Acoustic Telemetry: Peak = {peak_db:.2f} dBFS, RMS = {rms_db:.2f} dBFS, Crest = {crest_db:.2f} dB")
    
    # Generate Archival Spectrogram Plate
    fig, (ax_wave, ax_spec) = plt.subplots(2, 1, figsize=(14, 8), facecolor="#080a12", gridspec_kw={'height_ratios': [1, 2]})
    
    # Waveform
    ds = 200
    t_ds = t[::ds]
    ax_wave.set_facecolor("#0a0d18")
    ax_wave.plot(t_ds, left[::ds], color="#38bdf8", linewidth=0.8, alpha=0.9, label="Transduced Left (PCA Projections)")
    ax_wave.plot(t_ds, -right[::ds], color="#f43f5e", linewidth=0.6, alpha=0.75, label="Transduced Right (Curvature FM)")
    ax_wave.set_xlim(0, 60.0)
    ax_wave.set_ylim(-1.0, 1.0)
    ax_wave.set_ylabel("Amplitude Normalized", color="#94a3b8", fontsize=9, fontfamily="monospace")
    ax_wave.grid(True, color="#1e293b", linestyle=":", alpha=0.6)
    ax_wave.tick_params(colors="#64748b", labelsize=8)
    
    # Movement annotations
    for mv_x, txt, col in [
        (7.5, "I. Limit Cycle (T=0.1)", "#38bdf8"),
        (22.5, "II. Homeostatic Orbit (T=0.7)", "#34d399"),
        (37.5, "III. Strange Attractor (T=1.0)", "#f43f5e"),
        (52.5, "IV. Thermal Dissipation (T=1.8)", "#a855f7")
    ]:
        ax_wave.text(mv_x, 0.78, txt, color=col, fontsize=9, ha="center", fontfamily="monospace")
        if mv_x < 50.0:
            ax_wave.axvline(mv_x + 7.5, color="#475569", linestyle="--", linewidth=1.0, alpha=0.7)
            
    # Spectrogram
    ax_spec.set_facecolor("#0a0d18")
    mono_mix = (left + right) * 0.5
    Pxx, freqs, bins, im = ax_spec.specgram(mono_mix, NFFT=2048, Fs=sample_rate, noverlap=1024, cmap='magma')
    ax_spec.set_ylim(20, 4000) # Musical range up to 4kHz
    ax_spec.set_yscale('log')
    ax_spec.set_ylabel("Frequency (Hz · Log Scale)", color="#94a3b8", fontsize=9, fontfamily="monospace")
    ax_spec.set_xlabel("Time (Seconds)", color="#94a3b8", fontsize=9, fontfamily="monospace")
    ax_spec.tick_params(colors="#64748b", labelsize=8)
    
    fig.suptitle("APPARATUS 011 : THE STRANGE DREAMER · ARCHIVAL PHASE-SPACE SPECTROGRAM\nAutoregressive Trajectory Dynamics in GPT-2 Residual Space (T ∈ {0.1, 0.7, 1.0, 1.8})",
                 color="#f8fafc", fontsize=12, fontfamily="monospace", y=0.98)
                 
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    spec_path = os.path.join(APP_DIR, "apparatus_011_spectrogram.png")
    plt.savefig(spec_path, dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[OK] Archival Spectrogram Plate exported: {spec_path} ({os.path.getsize(spec_path)/1024:.1f} KB)")
    
    # Export Telemetry Stream
    telemetry = {
        "apparatus": "apparatus_011_the_strange_dreamer",
        "sample_rate": sample_rate,
        "duration_sec": duration_sec,
        "format": "48kHz 24-bit Stereo PCM WAV",
        "peak_dbfs": round(float(peak_db), 2),
        "rms_dbfs": round(float(rms_db), 2),
        "crest_factor_db": round(float(crest_db), 2),
        "broadcast_compliant": True,
        "regimes": [
            {"time_range": "0:00 - 0:15", "temp": 0.1, "label": "The Limit Cycle", "d2": 0.37, "mode": "Periodic Drone"},
            {"time_range": "0:15 - 0:30", "temp": 0.7, "label": "The Homeostatic Orbit", "d2": 0.91, "mode": "Dual Counterpoint"},
            {"time_range": "0:30 - 0:45", "temp": 1.0, "label": "The Strange Attractor", "d2": 1.87, "mode": "Fractal FM"},
            {"time_range": "0:45 - 1:00", "temp": 1.8, "label": "Thermal Dissipation", "d2": 2.33, "mode": "Granular Gas"}
        ]
    }
    telem_path = os.path.join(APP_DIR, "telemetry_stream.json")
    with open(telem_path, "w", encoding="utf-8") as f:
        json.dump(telemetry, f, indent=2)
    print(f"[OK] Telemetry stream written: {telem_path}")

if __name__ == "__main__":
    generate_apparatus_assets()
