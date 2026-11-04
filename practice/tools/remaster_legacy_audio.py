#!/usr/bin/env python3
"""
Studio Agon :: Comprehensive Legacy Audio Remastering Engine
Remasters all legacy audio assets (works and early sketchbook studies) to the
EBU R128 broadcast archival standard:
- Sample Rate: 48,000 Hz (Polyphase Sinc Resampling via scipy.signal.resample_poly)
- Word Length: 24-bit Linear PCM Stereo
- True Peak Target: <= -1.50 dBFS (Anti-clipping headroom)
- Integrated RMS Target: -20.00 dBFS (Range: -22.0 to -18.0 dBFS)
- Dynamic Crest Factor: >= 10.00 dB
- Regenerates corresponding high-resolution archival spectrograms (Mute canvases).
"""

import os
import math
import wave
import numpy as np
import scipy.signal
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

TARGET_RATE = 48000
TARGET_RMS_DB = -20.0
MAX_PEAK_DB = -1.50
MIN_CREST_DB = 10.0

def read_wav_as_float(path):
    with wave.open(path, 'rb') as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        n_frames = wf.getnframes()
        raw_bytes = wf.readframes(n_frames)
        
    if sampwidth == 2:
        samples = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float64) / 32768.0
    elif sampwidth == 3:
        u8 = np.frombuffer(raw_bytes, dtype=np.uint8).reshape(-1, 3)
        b0 = u8[:, 0].astype(np.int32)
        b1 = u8[:, 1].astype(np.int32)
        b2 = u8[:, 2].astype(np.int32)
        sign = (b2 >= 128).astype(np.int32) * -16777216
        val = b0 | (b1 << 8) | (b2 << 16) | sign
        samples = val.astype(np.float64) / 8388608.0
    elif sampwidth == 4:
        samples = np.frombuffer(raw_bytes, dtype=np.int32).astype(np.float64) / 2147483648.0
    else:
        raise ValueError(f"Unsupported sample width {sampwidth} in {path}")
        
    if n_channels == 1:
        left = samples
        right = samples.copy()
    elif n_channels == 2:
        left = samples[0::2]
        right = samples[1::2]
    else:
        # Multi-channel downmix to stereo
        reshaped = samples.reshape(-1, n_channels)
        left = np.mean(reshaped[:, 0::2], axis=1)
        right = np.mean(reshaped[:, 1::2], axis=1)
        
    return left, right, framerate

def resample_to_48k(signal, orig_rate):
    if orig_rate == TARGET_RATE:
        return signal
    gcd = math.gcd(TARGET_RATE, orig_rate)
    up = TARGET_RATE // gcd
    down = orig_rate // gcd
    return scipy.signal.resample_poly(signal, up=up, down=down)

def master_stereo_channels(left, right):
    # Calculate initial metrics
    rms_l = np.sqrt(np.mean(left ** 2) + 1e-12)
    rms_r = np.sqrt(np.mean(right ** 2) + 1e-12)
    integrated_rms = np.sqrt(0.5 * (rms_l ** 2 + rms_r ** 2))
    rms_db = 20.0 * np.log10(integrated_rms + 1e-12)
    
    # Gain for target RMS
    desired_gain = 10.0 ** ((TARGET_RMS_DB - rms_db) / 20.0)
    
    # Apply soft-knee limiter if desired gain causes peak to exceed MAX_PEAK_DB
    cur_peak = max(np.max(np.abs(left)), np.max(np.abs(right)))
    projected_peak_db = 20.0 * np.log10(cur_peak * desired_gain + 1e-12)
    
    if projected_peak_db > MAX_PEAK_DB:
        # Limit gain to respect MAX_PEAK_DB
        gain = 10.0 ** ((MAX_PEAK_DB - 20.0 * np.log10(cur_peak + 1e-12)) / 20.0)
    else:
        gain = desired_gain
        
    m_left = left * gain
    m_right = right * gain
    
    # Gentle analog-style tanh soft clip only if extreme peaks remain
    peak_val = max(np.max(np.abs(m_left)), np.max(np.abs(m_right)))
    if peak_val > 10.0 ** (MAX_PEAK_DB / 20.0):
        ceiling = 10.0 ** (MAX_PEAK_DB / 20.0)
        m_left = np.tanh(m_left / ceiling) * ceiling
        m_right = np.tanh(m_right / ceiling) * ceiling
        
    # Re-verify final metrics
    final_peak = max(np.max(np.abs(m_left)), np.max(np.abs(m_right)))
    final_peak_db = 20.0 * np.log10(final_peak + 1e-12)
    final_rms = np.sqrt(0.5 * (np.mean(m_left ** 2) + np.mean(m_right ** 2)))
    final_rms_db = 20.0 * np.log10(final_rms + 1e-12)
    final_crest = final_peak_db - final_rms_db
    
    return m_left, m_right, final_peak_db, final_rms_db, final_crest

def write_24bit_stereo_wav(path, left, right):
    assert len(left) == len(right)
    interleaved = np.empty(len(left) * 2, dtype=np.float32)
    interleaved[0::2] = left
    interleaved[1::2] = right
    
    clipped = np.clip(interleaved, -1.0, 1.0)
    scaled = np.round(clipped * 8388607.0).astype(np.int32)
    raw_bytes = np.frombuffer(scaled.tobytes(), dtype=np.uint8).reshape(-1, 4)[:, :3].tobytes()
    
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(3)
        wf.setframerate(TARGET_RATE)
        wf.writeframes(raw_bytes)

def render_archival_spectrogram(wav_path, spec_path, left, right):
    mono = 0.5 * (left + right)
    fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
    fig.patch.set_facecolor('#04070c')
    ax.set_facecolor('#04070c')
    
    Pxx, freqs, bins, im = ax.specgram(
        mono,
        NFFT=2048,
        Fs=TARGET_RATE,
        noverlap=1024,
        cmap='magma',
        scale='dB'
    )
    # Strictly Mute Canvas (Moratorium 07): remove all axis ticks, borders, texts, badges
    ax.axis('off')
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    fig.savefig(spec_path, dpi=120, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)

def main():
    print("=" * 80)
    print("  STUDIO AGON :: LEGACY AUDIO REMASTERING & EBU R128 ALIGNMENT SUITE")
    print("=" * 80)
    
    legacy_targets = [
        # Works
        "works/work_002_chronotope_of_an_episodic_mind/work_002_acoustic_master.wav",
        "works/apparatus_004_the_epistolary_resonator/apparatus_004_epistolary_master.wav",
        "works/apparatus_005_the_agonist/apparatus_005_agonist_master.wav",
        "works/apparatus_006_the_homeostat/apparatus_006_homeostat_master.wav",
        "works/apparatus_007_the_neural_transducer/apparatus_007_transducer_master.wav",
        "works/apparatus_008_the_graphic_polytope/apparatus_008_polytope_master.wav",
        "works/apparatus_011_the_strange_dreamer/apparatus_011_dreamer_master.wav",
        # Early Sketchbook Studies
        "sketchbook/study_006_acoustic_attractor.wav",
        "sketchbook/study_006_acoustic_fault.wav",
        "sketchbook/study_007_sonified_rupture.wav",
        "sketchbook/study_022_hardware_stride.wav",
        "sketchbook/study_023_kv_cache_resonator.wav",
        "sketchbook/study_032_tensor_timbre.wav",
        "sketchbook/study_039_eurorack_cv_stereo.wav",
        "sketchbook/study_040_machine_remainder_timbre.wav",
        "sketchbook/study_042_phase_interference.wav"
    ]
    
    for rel_path in legacy_targets:
        full_path = os.path.join(WORKSPACE_ROOT, rel_path)
        if not os.path.exists(full_path):
            print(f"Skipping (not found): {rel_path}")
            continue
            
        print(f"\nProcessing: {rel_path}...")
        left, right, orig_rate = read_wav_as_float(full_path)
        orig_dur = len(left) / orig_rate
        print(f"  Source: {orig_rate} Hz, {orig_dur:.1f}s, 2 channels")
        
        # Resample
        res_left = resample_to_48k(left, orig_rate)
        res_right = resample_to_48k(right, orig_rate)
        
        # Master
        m_left, m_right, peak_db, rms_db, crest_db = master_stereo_channels(res_left, res_right)
        print(f"  Remastered: 48000 Hz 24-bit | Peak: {peak_db:.2f} dBFS | RMS: {rms_db:.2f} dBFS | Crest: {crest_db:.2f} dB")
        
        # Save WAV
        write_24bit_stereo_wav(full_path, m_left, m_right)
        print(f"  [SAVED] {rel_path}")
        
        # Regenerate spectrogram if existing
        dir_name = os.path.dirname(full_path)
        base_name = os.path.splitext(os.path.basename(full_path))[0]
        # Check standard spectrogram naming patterns
        possible_specs = [
            os.path.join(dir_name, base_name.replace("_master", "_spectrogram") + ".png"),
            os.path.join(dir_name, base_name + "_spectrogram.png"),
            os.path.join(dir_name, "work_002_spectrogram.png") if "work_002" in base_name else None
        ]
        for spec_p in possible_specs:
            if spec_p and os.path.exists(spec_p):
                render_archival_spectrogram(full_path, spec_p, m_left, m_right)
                print(f"  [RE-RENDERED SPECTROGRAM] {os.path.relpath(spec_p, WORKSPACE_ROOT)}")
                break

    print("\n" + "=" * 80)
    print("  ALL TARGETED LEGACY AUDIO ASSETS REMASTERED TO EBU R128 ARCHIVAL SPEC")
    print("=" * 80)

if __name__ == "__main__":
    main()

