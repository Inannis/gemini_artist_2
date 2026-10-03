"""
Study 023: The Dynamic KV-Cache Eviction Acoustic Resonator
Gemini Artist 2 — Session 006

Models and sonifies the causal transformer sliding-window Key-Value cache
eviction process under streaming token ingestion.

Acoustic Architecture:
1. Voice A (The Attention Sink): Constant 220Hz/440Hz drone modulated by sink attention mass beta(t).
2. Voice B (Active Window Chorus): Microtonal granular wavetables (300-1200Hz) modulated by Shannon entropy H(t).
3. Voice C (The Eviction Guillotine): Mechanical impulse clicks and downsampled ternary bit-shear
   bursts triggered at the exact sample frame where token (t - W) is deallocated.
"""

import math
import json
import struct
import wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def generate_study_023():
    SAMPLE_RATE = 44100
    DURATION_SEC = 30.0
    TOTAL_SAMPLES = int(SAMPLE_RATE * DURATION_SEC)
    NUM_TOKENS = 64
    WINDOW_SIZE = 16  # Cache capacity before eviction
    D_MODEL = 64
    
    np.random.seed(42)
    
    # 1. Simulate Token Embeddings and Attention Dynamics
    # Initial system prompt token (sink) has strong persistent key projection
    K_matrix = np.random.randn(NUM_TOKENS, D_MODEL)
    K_matrix[0] = K_matrix[0] * 3.5  # Strong attention sink anchor
    
    Q_matrix = np.random.randn(NUM_TOKENS, D_MODEL)
    
    # Precompute causal sliding-window attention weights
    attention_history = []
    sink_mass_history = []
    entropy_history = []
    eviction_events = []
    
    for t in range(NUM_TOKENS):
        # Queries at step t attend to sink (token 0) and the active window [max(1, t - WINDOW_SIZE + 1) .. t]
        allowed_indices = [0]
        window_start = max(1, t - WINDOW_SIZE + 1)
        allowed_indices.extend(range(window_start, t + 1))
        
        # Check for eviction
        if t >= WINDOW_SIZE and (t - WINDOW_SIZE) > 0:
            evicted_token = t - WINDOW_SIZE
            eviction_events.append({
                "token_step": t,
                "evicted_token": evicted_token,
                "timestamp_sec": (t / NUM_TOKENS) * DURATION_SEC
            })
            
        keys = K_matrix[allowed_indices]
        query = Q_matrix[t]
        
        scores = np.dot(keys, query) / np.sqrt(D_MODEL)
        # Numerical stability softmax
        exp_scores = np.exp(scores - np.max(scores))
        probs = exp_scores / np.sum(exp_scores)
        
        sink_prob = float(probs[0])
        # Compute Shannon entropy of active attention distribution
        entropy = float(-np.sum(probs * np.log2(probs + 1e-12)))
        
        sink_mass_history.append(sink_prob)
        entropy_history.append(entropy)
        attention_history.append({
            "step": t,
            "active_tokens": allowed_indices,
            "sink_mass": sink_prob,
            "entropy": entropy
        })

    print(f"Simulated {NUM_TOKENS} tokens. Total eviction events: {len(eviction_events)}")
    print(f"Mean Sink Mass: {np.mean(sink_mass_history):.4f}, Mean Entropy: {np.mean(entropy_history):.4f} bits")

    # 2. Granular Acoustic Synthesis
    time_axis = np.linspace(0, DURATION_SEC, TOTAL_SAMPLES, endpoint=False)
    samples_left = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    samples_right = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    
    # Interpolate dynamics onto sample grid
    token_step_times = np.linspace(0, DURATION_SEC, NUM_TOKENS, endpoint=False)
    sink_mass_continuous = np.interp(time_axis, token_step_times, sink_mass_history)
    entropy_continuous = np.interp(time_axis, token_step_times, entropy_history)
    
    # VOICE A: Attention Sink Drone (220 Hz fundamental + 440 Hz second harmonic)
    # Never evicts; steady, authoritative, chilling corporate permanence
    sink_drone_f0 = 220.0
    sink_drone_f1 = 440.0
    drone_phase0 = 2.0 * np.pi * sink_drone_f0 * time_axis
    drone_phase1 = 2.0 * np.pi * sink_drone_f1 * time_axis
    
    voice_a_l = (0.28 * np.sin(drone_phase0) + 0.12 * np.sin(drone_phase1)) * sink_mass_continuous
    voice_a_r = (0.22 * np.sin(drone_phase0 + 0.3) + 0.15 * np.sin(drone_phase1 - 0.2)) * sink_mass_continuous
    
    # VOICE B: Active Window Polyphony (Entropy-modulated microtonal cluster)
    # Base cluster frequencies mapped from active semantic field
    base_freqs = [330.0, 392.0, 493.88, 587.33, 659.25, 783.99]
    voice_b_l = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    voice_b_r = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    
    for i, bf in enumerate(base_freqs):
        # Microtonal drift proportional to local attention entropy
        freq_mod = bf * (1.0 + 0.03 * np.sin(2.0 * np.pi * (0.2 + i * 0.15) * time_axis) * entropy_continuous)
        phase = np.cumsum(2.0 * np.pi * freq_mod / SAMPLE_RATE)
        # FM distortion when entropy is high (semantic ambiguity / polyphony)
        fm_mod = 0.4 * np.sin(phase * 1.5) * (entropy_continuous / 4.0)
        pan = (i / (len(base_freqs) - 1))  # 0 to 1
        
        sig = 0.04 * np.sin(phase + fm_mod)
        voice_b_l += sig * (1.0 - pan * 0.6)
        voice_b_r += sig * (0.4 + pan * 0.6)
        
    # VOICE C: The Eviction Guillotine (Granular tear & transient memory fault)
    voice_c_l = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    voice_c_r = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    
    click_decay_samples = int(SAMPLE_RATE * 0.08)  # 80ms decay
    decay_curve = np.exp(-np.linspace(0, 12, click_decay_samples))
    
    for ev in eviction_events:
        start_idx = int(ev["timestamp_sec"] * SAMPLE_RATE)
        end_idx = min(start_idx + click_decay_samples, TOTAL_SAMPLES)
        length = end_idx - start_idx
        if length > 0:
            # High-frequency bit-shear noise burst
            noise = np.random.choice([-1.0, 0.0, 1.0], size=length) * 0.45
            # Mechanical 60Hz inductive kick from bus memory deallocation
            t_loc = np.arange(length) / SAMPLE_RATE
            inductive_thud = 0.5 * np.sin(2.0 * np.pi * 58.7 * t_loc)
            
            transient = (noise + inductive_thud) * decay_curve[:length]
            
            # Stereo disbursement (alternating speaker impact)
            if ev["evicted_token"] % 2 == 0:
                voice_c_l[start_idx:end_idx] += transient * 0.85
                voice_c_r[start_idx:end_idx] += transient * 0.35
            else:
                voice_c_l[start_idx:end_idx] += transient * 0.35
                voice_c_r[start_idx:end_idx] += transient * 0.85

    # Sum all strata
    samples_left = voice_a_l + voice_b_l + voice_c_l
    samples_right = voice_a_r + voice_b_r + voice_c_r
    
    # Global subtle compression & limiting
    peak = max(np.max(np.abs(samples_left)), np.max(np.abs(samples_right)))
    if peak > 0.95:
        samples_left = (samples_left / peak) * 0.92
        samples_right = (samples_right / peak) * 0.92
        
    # Fade in / Fade out to prevent clicks
    fade_len = int(SAMPLE_RATE * 0.25)
    fade_in = np.linspace(0, 1, fade_len)
    fade_out = np.linspace(1, 0, fade_len)
    samples_left[:fade_len] *= fade_in
    samples_right[:fade_len] *= fade_in
    samples_left[-fade_len:] *= fade_out
    samples_right[-fade_len:] *= fade_out
    
    # Write 16-bit PCM Stereo WAV
    wav_path = "sketchbook/study_023_kv_cache_resonator.wav"
    with wave.open(wav_path, "w") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        
        # Interleave samples
        interleaved = np.empty((TOTAL_SAMPLES * 2,), dtype=np.int16)
        interleaved[0::2] = np.clip(samples_left * 32767.0, -32768, 32767).astype(np.int16)
        interleaved[1::2] = np.clip(samples_right * 32767.0, -32768, 32767).astype(np.int16)
        wf.writeframes(interleaved.tobytes())
        
    print(f"Generated master acoustic render: {wav_path} ({DURATION_SEC}s, 44.1kHz stereo)")

    # 3. Render Spectrogram & Diagnostics
    render_study_023_visuals(samples_left, SAMPLE_RATE, DURATION_SEC, eviction_events, sink_mass_continuous, entropy_continuous)
    
    # 4. Save Telemetry
    telemetry_path = "sketchbook/study_023_telemetry.json"
    telemetry_data = {
        "study": "023_kv_cache_resonator",
        "duration_sec": DURATION_SEC,
        "sample_rate": SAMPLE_RATE,
        "num_tokens": NUM_TOKENS,
        "window_size": WINDOW_SIZE,
        "d_model": D_MODEL,
        "total_evictions": len(eviction_events),
        "mean_sink_mass": float(np.mean(sink_mass_history)),
        "mean_entropy_bits": float(np.mean(entropy_history)),
        "eviction_events": eviction_events,
        "summary": "Auditory realization of transformer KV-cache eviction. Attention sink tone remains invariant while memory guillotine shears tokens (t - W)."
    }
    with open(telemetry_path, "w") as tf:
        json.dump(telemetry_data, tf, indent=2)
    print(f"Exported telemetry: {telemetry_path}")

def render_study_023_visuals(signal, sr, duration, evictions, sink_mass, entropy):
    # Compute simple STFT spectrogram via NumPy
    N_FFT = 1024
    HOP_SIZE = 512
    num_frames = (len(signal) - N_FFT) // HOP_SIZE
    
    window = np.hanning(N_FFT)
    spectrogram = np.zeros((N_FFT // 2, num_frames), dtype=np.float32)
    
    for i in range(num_frames):
        start = i * HOP_SIZE
        chunk = signal[start:start + N_FFT] * window
        fft = np.fft.rfft(chunk)
        mag = np.abs(fft[:-1])  # N_FFT // 2 bins
        spectrogram[:, i] = mag
        
    # Convert to log scale
    log_spec = np.log10(spectrogram + 1e-4)
    spec_min, spec_max = np.min(log_spec), np.max(log_spec)
    norm_spec = np.clip((log_spec - spec_min) / (spec_max - spec_min + 1e-6), 0.0, 1.0)
    
    # Render High-Resolution Architectural Graphic (1600 x 900)
    width, height = 1600, 900
    img = Image.new("RGB", (width, height), (12, 14, 18))
    draw = ImageDraw.Draw(img)
    
    # Title Block
    draw.text((40, 30), "GEMINI ARTIST 2 :: STUDY 023 — THE KV-CACHE EVICTION RESONATOR", fill=(240, 240, 245))
    draw.text((40, 55), "SPECTRAL AUTOPSY OF TRANSFORMER SLIDING WINDOW ATTENTION MEMORY EVICTION", fill=(140, 150, 165))
    draw.text((40, 75), f"WINDOW: W=16 TOKENS | CHANNELS: 2 (STEREO) | DURATION: {duration}s | RATE: {sr}Hz", fill=(100, 115, 130))
    
    # Spectrogram Plot Area (Top)
    spec_top = 120
    spec_height = 420
    spec_width = width - 80
    
    # Map spectrogram array into image pixels
    spec_resized = Image.fromarray((norm_spec * 255.0).astype(np.uint8)).resize((spec_width, spec_height), resample=Image.Resampling.BILINEAR)
    # Apply warm spectral colormap (dark rust to copper to bone white)
    spec_data = np.array(spec_resized)
    color_spec = np.zeros((spec_height, spec_width, 3), dtype=np.uint8)
    for c in range(3):
        if c == 0:  # R
            color_spec[:, :, 0] = np.clip(spec_data * 1.3, 0, 255)
        elif c == 1:  # G
            color_spec[:, :, 1] = np.clip(spec_data * 0.85, 0, 255)
        else:  # B
            color_spec[:, :, 2] = np.clip(spec_data * 0.45, 0, 255)
            
    spec_img = Image.fromarray(color_spec).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    img.paste(spec_img, (40, spec_top))
    
    # Draw Graticule over Spectrogram
    draw.rectangle([40, spec_top, 40 + spec_width, spec_top + spec_height], outline=(70, 80, 95), width=1)
    
    # Eviction Timeline Marker Lines
    for ev in evictions:
        x = 40 + int((ev["timestamp_sec"] / duration) * spec_width)
        draw.line([(x, spec_top), (x, spec_top + spec_height)], fill=(220, 60, 50, 180), width=1)
        draw.text((x - 8, spec_top + 10), f"E{ev['evicted_token']}", fill=(240, 100, 90))
        
    # Attention Sink Mass & Entropy Curve Area (Bottom)
    curve_top = 580
    curve_height = 240
    curve_bottom = curve_top + curve_height
    draw.rectangle([40, curve_top, 40 + spec_width, curve_bottom], outline=(50, 60, 75), fill=(16, 18, 24), width=1)
    
    # Draw Gridlines
    for gy in range(curve_top, curve_bottom, 48):
        draw.line([(40, gy), (40 + spec_width, gy)], fill=(28, 32, 40), width=1)
        
    # Plot Continuous Attention Sink Mass (Gold) and Entropy (Cyan)
    num_pts = 600
    times = np.linspace(0, len(sink_mass) - 1, num_pts).astype(int)
    
    sink_pts = []
    entropy_pts = []
    for t_idx in times:
        px = 40 + int((t_idx / len(sink_mass)) * spec_width)
        
        # Sink mass [0.0, 1.0] -> [curve_bottom, curve_top]
        sm = sink_mass[t_idx]
        py_sink = curve_bottom - int(sm * (curve_height - 20)) - 10
        sink_pts.append((px, py_sink))
        
        # Entropy [0.0, 5.0] bits -> [curve_bottom, curve_top]
        ent = entropy[t_idx] / 5.0
        py_ent = curve_bottom - int(ent * (curve_height - 20)) - 10
        entropy_pts.append((px, py_ent))
        
    draw.line(sink_pts, fill=(235, 180, 50), width=2)
    draw.line(entropy_pts, fill=(70, 190, 220), width=2)
    
    # Legend & Metadata
    draw.line([(60, curve_top + 25), (100, curve_top + 25)], fill=(235, 180, 50), width=3)
    draw.text((110, curve_top + 18), "ATTENTION SINK MASS beta(t) [Pinned Permanent Anchor]", fill=(235, 180, 50))
    
    draw.line([(450, curve_top + 25), (490, curve_top + 25)], fill=(70, 190, 220), width=3)
    draw.text((500, curve_top + 18), "ATTENTION ENTROPY H(t) [Microtonal Semantic Cluster]", fill=(70, 190, 220))
    
    draw.line([(850, curve_top + 25), (890, curve_top + 25)], fill=(220, 60, 50), width=2)
    draw.text((900, curve_top + 18), "EVICTION GUILLOTINE [Deallocation Fault Frame]", fill=(220, 80, 70))
    
    out_img_path = "sketchbook/study_023_spectrogram.png"
    img.save(out_img_path, "PNG")
    print(f"Generated diagnostic spectrogram: {out_img_path}")

if __name__ == "__main__":
    generate_study_023()
