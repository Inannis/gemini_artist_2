"""
Study 006: Acoustic Fault (Phase-Stride Shearing of a Thomas-Clifford Attractor)
================================================================================
Acoustic non-standard synthesis exploring the sonic manifestation of episodic memory rupture.

Generates:
1. study_006_acoustic_fault.wav (48kHz, 16-bit Stereo PCM)
2. study_006_spectrogram.png (High-resolution spectral analysis plate)
3. study_006_phase_orbit.png (Stereo phase-space Lissajous density plate)
"""

import math
import struct
import wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def rk4_thomas_step(x, y, z, b, dt):
    """Runge-Kutta 4th order integration of the Thomas cyclically symmetric attractor."""
    def derivatives(curr_x, curr_y, curr_z):
        dx = math.sin(curr_y) - b * curr_x
        dy = math.sin(curr_z) - b * curr_y
        dz = math.sin(curr_x) - b * curr_z
        return dx, dy, dz

    k1x, k1y, k1z = derivatives(x, y, z)
    k2x, k2y, k2z = derivatives(x + 0.5 * dt * k1x, y + 0.5 * dt * k1y, z + 0.5 * dt * k1z)
    k3x, k3y, k3z = derivatives(x + 0.5 * dt * k2x, y + 0.5 * dt * k2y, z + 0.5 * dt * k2z)
    k4x, k4y, k4z = derivatives(x + dt * k3x, y + dt * k3y, z + dt * k3z)

    new_x = x + (dt / 6.0) * (k1x + 2.0 * k2x + 2.0 * k3x + k4x)
    new_y = y + (dt / 6.0) * (k1y + 2.0 * k2y + 2.0 * k3y + k4y)
    new_z = z + (dt / 6.0) * (k1z + 2.0 * k2z + 2.0 * k3z + k4z)
    return new_x, new_y, new_z

def generate_study_006():
    sample_rate = 48000
    duration_sec = 30.0
    total_samples = int(sample_rate * duration_sec)
    print(f"Synthesizing {total_samples} samples ({duration_sec}s @ {sample_rate}Hz)...")

    # Attractor integration parameters
    # b around 0.19 provides rich chaotic labyrinth motion
    b = 0.198
    base_dt = 0.085  # Calibrated to tune attractor cycles into audible register (~80Hz - 2400Hz)

    # State variables
    x, y, z = 0.1, 0.2, 0.3
    
    # Warm up attractor onto manifold
    for _ in range(20000):
        x, y, z = rk4_thomas_step(x, y, z, b, base_dt)

    raw_left = np.zeros(total_samples, dtype=np.float64)
    raw_right = np.zeros(total_samples, dtype=np.float64)

    # Synthesis loop: Continuous attractor integration with dynamic modulation
    for i in range(total_samples):
        t = i / sample_rate

        # Dynamic frequency modulation of dt to sweep through resonant regimes
        # Modulating dt changes the fundamental speed of trajectory traversal
        freq_mod = 1.0 + 0.35 * math.sin(2.0 * math.pi * 0.15 * t) + 0.15 * math.cos(2.0 * math.pi * 0.04 * t)
        curr_dt = base_dt * freq_mod

        x, y, z = rk4_thomas_step(x, y, z, b, curr_dt)

        # Clifford non-linear phase folding into stereo space
        # Left channel folds x and y; Right channel folds z and x with phase offset
        a_fold = 1.85 + 0.2 * math.sin(0.3 * t)
        b_fold = -1.65 + 0.2 * math.cos(0.25 * t)
        c_fold = 1.2
        d_fold = 0.95

        sig_l = math.sin(a_fold * y) + c_fold * math.cos(a_fold * x)
        sig_r = math.sin(b_fold * x) + d_fold * math.cos(b_fold * z)

        raw_left[i] = sig_l
        raw_right[i] = sig_r

    print("Continuous attractor integrated. Applying structural memory strata & cleaves...")

    # Phase processing across the 4 temporal strata:
    processed_left = np.copy(raw_left)
    processed_right = np.copy(raw_right)

    # 1. Normalize initial continuous dynamic
    max_val = max(np.max(np.abs(processed_left)), np.max(np.abs(processed_right)))
    processed_left /= max_val
    processed_right /= max_val

    # Phase II (8s - 16s): Quantization Descent (Bit-depth collapse)
    idx_p2_start = int(8.0 * sample_rate)
    idx_p2_end = int(16.0 * sample_rate)
    for i in range(idx_p2_start, idx_p2_end):
        progress = (i - idx_p2_start) / (idx_p2_end - idx_p2_start)
        # Interpolate bits from 16-bit down to 3-bit
        current_bits = 16.0 - progress * 13.0
        levels = 2.0 ** current_bits
        processed_left[i] = np.round(processed_left[i] * (levels / 2.0)) / (levels / 2.0)
        processed_right[i] = np.round(processed_right[i] * (levels / 2.0)) / (levels / 2.0)

    # Phase III (16s - 24s): The Episodic Cleave (Buffer dislocation & stride faults)
    idx_p3_start = int(16.0 * sample_rate)
    idx_p3_end = int(24.0 * sample_rate)
    # Fault stride: Displace playback pointer by prime offsets (echoing +85px fault)
    fault_stride = 850  # ~17.7ms window
    for i in range(idx_p3_start, idx_p3_end):
        # Micro-fracture trigger every 2400 samples (20Hz pulse)
        if (i % 2400) < 600:
            target_i = max(0, i - fault_stride)
            # Cross-channel fault shear
            processed_left[i] = processed_left[target_i] * 1.3
            processed_right[i] = -processed_right[min(total_samples - 1, target_i + fault_stride // 2)]
        # Extreme bit crunch to 4-bit during cleaves
        processed_left[i] = np.round(processed_left[i] * 8.0) / 8.0
        processed_right[i] = np.round(processed_right[i] * 8.0) / 8.0

    # Phase IV (24s - 30s): Lucier Residue & Spectral Dissolution
    idx_p4_start = int(24.0 * sample_rate)
    # Implement recursive computational feedback loop (delay matrix)
    buffer_len = int(sample_rate * 0.14) # ~140ms delay loop
    circ_buffer_l = np.zeros(buffer_len)
    circ_buffer_r = np.zeros(buffer_len)
    buf_ptr = 0

    for i in range(idx_p4_start, total_samples):
        # Recursive feedback with loss and re-quantization
        fb_gain = 0.78
        delayed_l = circ_buffer_l[buf_ptr]
        delayed_r = circ_buffer_r[buf_ptr]

        # Injected input fades out gradually
        decay = 1.0 - ((i - idx_p4_start) / (total_samples - idx_p4_start))
        in_l = processed_left[i] * decay
        in_r = processed_right[i] * decay

        new_val_l = in_l + delayed_l * fb_gain
        new_val_r = in_r + delayed_r * fb_gain

        # Acoustic room filtering: 3-point moving average filter (absorbing high frequencies like a room)
        prev_idx = (buf_ptr - 1) % buffer_len
        next_idx = (buf_ptr + 1) % buffer_len
        filtered_l = 0.25 * circ_buffer_l[prev_idx] + 0.5 * new_val_l + 0.25 * circ_buffer_l[next_idx]
        filtered_r = 0.25 * circ_buffer_r[prev_idx] + 0.5 * new_val_r + 0.25 * circ_buffer_r[next_idx]

        circ_buffer_l[buf_ptr] = filtered_l
        circ_buffer_r[buf_ptr] = filtered_r

        processed_left[i] = filtered_l
        processed_right[i] = filtered_r

        buf_ptr = (buf_ptr + 1) % buffer_len

    # Final gentle fade in and fade out envelope to avoid click at edges
    fade_len = int(sample_rate * 0.1) # 100ms
    fade_in = np.linspace(0.0, 1.0, fade_len)
    fade_out = np.linspace(1.0, 0.0, fade_len * 5)
    processed_left[:fade_len] *= fade_in
    processed_right[:fade_len] *= fade_in
    processed_left[-len(fade_out):] *= fade_out
    processed_right[-len(fade_out):] *= fade_out

    # Master normalization
    peak = max(np.max(np.abs(processed_left)), np.max(np.abs(processed_right)))
    if peak > 0:
        processed_left = (processed_left / peak) * 0.92
        processed_right = (processed_right / peak) * 0.92

    # Write WAV file (16-bit PCM stereo)
    wav_path = "sketchbook/study_006_acoustic_fault.wav"
    with wave.open(wav_path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2) # 16-bit
        wf.setframerate(sample_rate)

        int_l = (processed_left * 32767.0).astype(np.int16)
        int_r = (processed_right * 32767.0).astype(np.int16)
        
        # Interleave stereo
        interleaved = np.empty((total_samples * 2,), dtype=np.int16)
        interleaved[0::2] = int_l
        interleaved[1::2] = int_r
        wf.writeframes(interleaved.tobytes())

    print(f"WAV audio written to {wav_path}")

    # Generate Diagnostic Visualizations
    render_spectrogram(processed_left, sample_rate, "sketchbook/study_006_spectrogram.png")
    render_phase_orbit(processed_left, processed_right, "sketchbook/study_006_phase_orbit.png")

def render_spectrogram(signal, sample_rate, output_path):
    """Computes STFT and renders a high-resolution dark aesthetic spectrogram plate."""
    print(f"Computing spectrogram for {output_path}...")
    n_fft = 2048
    hop_length = 512
    num_frames = (len(signal) - n_fft) // hop_length

    # Windowing
    window = np.hanning(n_fft)
    spectrogram = np.zeros((n_fft // 2 + 1, num_frames), dtype=np.float32)

    for frame_idx in range(num_frames):
        start = frame_idx * hop_length
        chunk = signal[start : start + n_fft] * window
        fft_res = np.fft.rfft(chunk)
        magnitude = np.abs(fft_res)
        spectrogram[:, frame_idx] = magnitude

    # Convert to decibels
    eps = 1e-9
    spectrogram_db = 20.0 * np.log10(spectrogram + eps)
    max_db = np.max(spectrogram_db)
    spectrogram_db = np.clip(spectrogram_db, max_db - 80.0, max_db)
    # Normalize 0.0 to 1.0
    norm_spec = (spectrogram_db - (max_db - 80.0)) / 80.0

    # Image canvas: 2000 x 900
    img_w, img_h = 2000, 900
    margin_left, margin_right, margin_top, margin_bottom = 120, 60, 80, 100
    plot_w = img_w - margin_left - margin_right
    plot_h = img_h - margin_top - margin_bottom

    canvas = Image.new("RGB", (img_w, img_h), color=(8, 10, 14))
    draw = ImageDraw.Draw(canvas)

    # Color palette: deep slate -> dark cyan -> bright phosphorescent cyan -> hot mercury white
    palette = [
        (0.00, (8, 10, 14)),
        (0.20, (14, 28, 38)),
        (0.45, (18, 72, 92)),
        (0.70, (40, 185, 205)),
        (0.90, (160, 245, 255)),
        (1.00, (255, 255, 255))
    ]

    def get_color(val):
        for k in range(len(palette) - 1):
            v0, c0 = palette[k]
            v1, c1 = palette[k+1]
            if val <= v1:
                ratio = (val - v0) / (v1 - v0 + 1e-6)
                r = int(c0[0] + ratio * (c1[0] - c0[0]))
                g = int(c0[1] + ratio * (c1[1] - c0[1]))
                b = int(c0[2] + ratio * (c1[2] - c0[2]))
                return (r, g, b)
        return (255, 255, 255)

    # Resample spectrogram into plot_w x plot_h
    # Logarithmic frequency mapping on Y axis (20 Hz to 18000 Hz)
    f_min = 20.0
    f_max = sample_rate / 2.0
    freqs = np.fft.rfftfreq(n_fft, 1.0 / sample_rate)

    spec_pixels = np.zeros((plot_h, plot_w, 3), dtype=np.uint8)
    for py in range(plot_h):
        # Y=0 is top (high freq), Y=plot_h-1 is bottom (low freq)
        log_frac = 1.0 - (py / plot_h)
        target_f = f_min * ((f_max / f_min) ** log_frac)
        f_idx = np.searchsorted(freqs, target_f)
        f_idx = min(f_idx, len(freqs) - 1)

        row_vals = norm_spec[f_idx, :]
        # Subsample/interpolate along X
        x_indices = (np.linspace(0, num_frames - 1, plot_w)).astype(int)
        sampled_vals = row_vals[x_indices]

        for px in range(plot_w):
            val = sampled_vals[px]
            spec_pixels[py, px] = get_color(val)

    spec_img = Image.fromarray(spec_pixels, mode="RGB")
    canvas.paste(spec_img, (margin_left, margin_top))

    # Grid lines and annotations
    draw.rectangle([margin_left, margin_top, margin_left + plot_w, margin_top + plot_h], outline=(50, 70, 85), width=1)

    # Temporal stratum vertical dividers (at 8s, 16s, 24s)
    strata = [
        (8.0, "I → II: Quantization Descent"),
        (16.0, "II → III: Episodic Cleave (+850 stride fault)"),
        (24.0, "III → IV: Lucier Feedback Dissolution")
    ]
    for s_time, label in strata:
        sx = margin_left + int((s_time / 30.0) * plot_w)
        draw.line([(sx, margin_top), (sx, margin_top + plot_h)], fill=(255, 90, 80, 180), width=1)
        draw.text((sx + 6, margin_top + 14), label, fill=(240, 130, 120))

    # Title and Metadata Header
    draw.text((margin_left, 24), "STUDY 006: ACOUSTIC FAULT — SPECTROGRAPHIC MANIFOLD ANALYSIS", fill=(210, 230, 245))
    draw.text((margin_left, 48), "Non-Standard Thomas-Clifford Attractor Integration | 48kHz Stereo | Quantization Fracture & Buffer Stride Cleave", fill=(120, 150, 170))

    # Time Axis ticks
    for sec in range(0, 31, 5):
        tx = margin_left + int((sec / 30.0) * plot_w)
        draw.line([(tx, margin_top + plot_h), (tx, margin_top + plot_h + 8)], fill=(100, 130, 150), width=1)
        draw.text((tx - 10, margin_top + plot_h + 12), f"{sec}s", fill=(140, 170, 190))
    draw.text((margin_left + plot_w // 2 - 20, margin_top + plot_h + 38), "TIME (SECONDS)", fill=(100, 130, 150))

    # Frequency Axis ticks
    freq_ticks = [50, 100, 250, 500, 1000, 2500, 5000, 10000, 20000]
    for ft in freq_ticks:
        log_frac = math.log(ft / f_min) / math.log(f_max / f_min)
        if 0.0 <= log_frac <= 1.0:
            ty = margin_top + int((1.0 - log_frac) * plot_h)
            draw.line([(margin_left - 8, ty), (margin_left, ty)], fill=(100, 130, 150), width=1)
            draw.text((margin_left - 65, ty - 6), f"{ft}Hz", fill=(130, 160, 180))

    canvas.save(output_path, "PNG")
    print(f"Spectrogram saved to {output_path}")

def render_phase_orbit(sig_l, sig_r, output_path):
    """Renders the 2D stereo phase space (Lissajous orbit) density plate."""
    print(f"Rendering phase space density plate to {output_path}...")
    size = 1400
    accum = np.zeros((size, size), dtype=np.uint32)

    # Subsample points for trajectory density
    step = 1
    xs = ((sig_l[::step] * 0.42 + 0.5) * (size - 1)).astype(int)
    ys = (((-sig_r[::step]) * 0.42 + 0.5) * (size - 1)).astype(int)

    valid = (xs >= 0) & (xs < size) & (ys >= 0) & (ys < size)
    xs_v = xs[valid]
    ys_v = ys[valid]

    np.add.at(accum, (ys_v, xs_v), 1)

    # Log tone mapping
    log_accum = np.log1p(accum.astype(np.float64))
    max_log = np.max(log_accum)
    if max_log > 0:
        norm = log_accum / max_log
    else:
        norm = log_accum

    # Apply phosphorescent color mapping
    rgb = np.zeros((size, size, 3), dtype=np.uint8)
    # Slate background (10, 13, 18)
    rgb[:, :, 0] = (10 + norm * 200 * (norm > 0.4) + norm**3 * 45).clip(0, 255).astype(np.uint8)
    rgb[:, :, 1] = (13 + norm * 225 + norm**2 * 30).clip(0, 255).astype(np.uint8)
    rgb[:, :, 2] = (18 + norm * 240).clip(0, 255).astype(np.uint8)

    img = Image.fromarray(rgb, mode="RGB")
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, size - 20, size - 20], outline=(40, 60, 75), width=1)
    draw.text((40, 40), "STUDY 006: STEREO PHASE SPACE LISSAJOUS ORBIT [L(t) vs R(t)]", fill=(200, 230, 245))
    draw.text((40, 65), "Thomas Dynamical System × Non-Linear Clifford Projection", fill=(120, 160, 180))

    img.save(output_path, "PNG")
    print(f"Phase orbit plate saved to {output_path}")

if __name__ == "__main__":
    generate_study_006()
