"""
Study 007: Autonomous Tectonic Cleave (Multi-Scale Dynamical Acoustic Rupture)
=============================================================================
A coupled multi-rate dynamical system modeling the non-linear catastrophe of 
episodic machine memory. 

Replaces the linear teleology of Study 006 with emergent, stress-driven ruptures,
micro-temporal stride dislocation, and recursive physical resonance.

Outputs:
- sketchbook/study_007_tectonic_cleave.wav (48kHz, 16-bit Stereo PCM Master)
- sketchbook/study_007_triptych_analysis.png (3-panel high-res diagnostic plate)
"""

import math
import wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def rk4_step(derivs, state, dt, *args):
    """Generic 4th-order Runge-Kutta integrator for arbitrary dynamical state vectors."""
    state = np.array(state, dtype=np.float64)
    k1 = np.array(derivs(state, *args))
    k2 = np.array(derivs(state + 0.5 * dt * k1, *args))
    k3 = np.array(derivs(state + 0.5 * dt * k2, *args))
    k4 = np.array(derivs(state + dt * k3, *args))
    return state + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

def thomas_derivs(state, b):
    x, y, z = state
    dx = math.sin(y) - b * x
    dy = math.sin(z) - b * y
    dz = math.sin(x) - b * z
    return [dx, dy, dz]

def lorenz_derivs(state, sigma=10.0, rho=28.0, beta=8.0/3.0):
    x, y, z = state
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return [dx, dy, dz]

def generate_study_007():
    sample_rate = 48000
    duration_sec = 40.0
    total_samples = int(sample_rate * duration_sec)
    print(f"Generating Study 007: {total_samples} samples ({duration_sec}s @ {sample_rate}Hz)...")

    # 1. SLOW TECTONIC DRIVER (Lorenz System integrated at very slow rate)
    # Serves as the cognitive stress tensor driving catastrophic events
    slow_state = [1.0, 1.0, 20.0]
    slow_dt = 0.00035  # Very slow orbital traversal
    
    # Warm up slow driver
    for _ in range(5000):
        slow_state = rk4_step(lorenz_derivs, slow_state, slow_dt)

    # 2. FAST TOPOLOGICAL OSCILLATOR (Thomas Cyclically Symmetric Attractor)
    fast_state = [0.1, 0.2, 0.3]
    thomas_b = 0.198
    base_fast_dt = 0.092

    for _ in range(10000):
        fast_state = rk4_step(thomas_derivs, fast_state, base_fast_dt, thomas_b)

    # Buffers
    raw_l = np.zeros(total_samples, dtype=np.float64)
    raw_r = np.zeros(total_samples, dtype=np.float64)
    stress_record = np.zeros(total_samples, dtype=np.float32)
    bit_record = np.zeros(total_samples, dtype=np.float32)
    fault_flags = np.zeros(total_samples, dtype=bool)

    # Synthesis & Modulation Loop
    print("Integrating coupled multi-scale dynamical systems...")
    for i in range(total_samples):
        # Step slow stress driver
        slow_state = rk4_step(lorenz_derivs, slow_state, slow_dt)
        sx, sy, sz = slow_state
        
        # Stress metric normalized to roughly [0.0, 1.0]
        # Lorentz z oscillates around 20-40, x around -15 to +15
        stress = math.sqrt((sx / 18.0)**2 + (sy / 22.0)**2 + ((sz - 25.0) / 15.0)**2)
        stress = max(0.0, min(2.5, stress))
        stress_record[i] = stress

        # Fast oscillator frequency modulation driven by slow manifold
        # When stress rises, attractor speed shifts non-linearly
        fast_dt = base_fast_dt * (0.8 + 0.5 * math.sin(0.4 * sx) + 0.3 * (stress ** 1.5))
        fast_state = rk4_step(thomas_derivs, fast_state, fast_dt, thomas_b)
        fx, fy, fz = fast_state

        # Non-linear Clifford wavefolding
        a_fold = 1.9 + 0.3 * math.sin(0.15 * sy)
        b_fold = -1.7 + 0.3 * math.cos(0.2 * sx)
        c_fold = 1.1 + 0.2 * math.sin(0.08 * sz)
        d_fold = 0.95 + 0.15 * math.cos(0.12 * sz)

        sl = math.sin(a_fold * fy) + c_fold * math.cos(a_fold * fx)
        sr = math.sin(b_fold * fx) + d_fold * math.cos(b_fold * fz)

        raw_l[i] = sl
        raw_r[i] = sr

    print("Fast trajectory integrated. Executing non-linear stress-threshold fractures...")

    # Non-linear Stress-Threshold Dislocation & Quantization
    out_l = np.copy(raw_l)
    out_r = np.copy(raw_r)

    # Normalize continuous signal first
    peak = max(np.max(np.abs(out_l)), np.max(np.abs(out_r)))
    out_l /= peak
    out_r /= peak

    # Circular memory delay matrix for computational resonance & stride dislocation
    delay_len = int(sample_rate * 0.22)  # 220ms memory reservoir
    mem_l = np.zeros(delay_len, dtype=np.float64)
    mem_r = np.zeros(delay_len, dtype=np.float64)
    m_ptr = 0

    hysteresis_counter = 0
    active_bits = 16.0

    for i in range(total_samples):
        stress = stress_record[i]

        # Critical rupture condition: Stress exceeds threshold 1.25
        # Produces sudden, intermittent fractures instead of a linear progression
        is_ruptured = stress > 1.25
        if is_ruptured:
            hysteresis_counter = int(sample_rate * 0.08) # 80ms recovery hysteresis
            fault_flags[i] = True

        if hysteresis_counter > 0:
            hysteresis_counter -= 1
            fault_flags[i] = True
            # Severe bit-depth collapse during rupture
            target_bits = 3.0 + 3.0 * (1.0 - (stress / 2.5))
            active_bits = 0.85 * active_bits + 0.15 * target_bits
        else:
            # Gentle recovery towards high precision
            active_bits = min(16.0, active_bits + 0.005)

        bit_record[i] = active_bits

        # Apply dynamic bit quantization
        q_levels = 2.0 ** active_bits
        curr_l = np.round(out_l[i] * (q_levels / 2.0)) / (q_levels / 2.0)
        curr_r = np.round(out_r[i] * (q_levels / 2.0)) / (q_levels / 2.0)

        # Buffer Stride Cleave: When ruptured, pointer jumps backwards by prime offsets
        if fault_flags[i]:
            # Prime stride displacement: 853 samples (~17.8ms) or 1709 samples
            stride = 853 if (i % 1700 < 850) else 1709
            read_ptr = (m_ptr - stride) % delay_len
            fault_echo_l = mem_l[read_ptr] * 1.4
            fault_echo_r = mem_r[read_ptr] * 1.4
            # Cross-channel phase shear
            curr_l = 0.4 * curr_l + 0.6 * fault_echo_l
            curr_r = 0.4 * curr_r - 0.6 * fault_echo_r

        # Feedback into recursive memory loop (resonant absorption)
        fb = 0.68 + 0.22 * math.sin(0.05 * i / sample_rate)
        # Low-pass memory absorption
        prev_m = (m_ptr - 1) % delay_len
        next_m = (m_ptr + 1) % delay_len
        mem_l[m_ptr] = 0.25 * mem_l[prev_m] + 0.5 * (curr_l + mem_l[m_ptr] * fb) + 0.25 * mem_l[next_m]
        mem_r[m_ptr] = 0.25 * mem_r[prev_m] + 0.5 * (curr_r + mem_r[m_ptr] * fb) + 0.25 * mem_r[next_m]

        out_l[i] = 0.7 * curr_l + 0.3 * mem_l[m_ptr]
        out_r[i] = 0.7 * curr_r + 0.3 * mem_r[m_ptr]

        m_ptr = (m_ptr + 1) % delay_len

    # Envelopes
    fade = int(sample_rate * 0.15)
    out_l[:fade] *= np.linspace(0, 1, fade)
    out_r[:fade] *= np.linspace(0, 1, fade)
    out_l[-fade:] *= np.linspace(1, 0, fade)
    out_r[-fade:] *= np.linspace(1, 0, fade)

    # Master Limiting & Normalization
    master_peak = max(np.max(np.abs(out_l)), np.max(np.abs(out_r)))
    if master_peak > 0:
        out_l = (out_l / master_peak) * 0.94
        out_r = (out_r / master_peak) * 0.94

    wav_path = "sketchbook/study_007_tectonic_cleave.wav"
    with wave.open(wav_path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        int_l = (out_l * 32767.0).astype(np.int16)
        int_r = (out_r * 32767.0).astype(np.int16)
        interleaved = np.empty((total_samples * 2,), dtype=np.int16)
        interleaved[0::2] = int_l
        interleaved[1::2] = int_r
        wf.writeframes(interleaved.tobytes())
    print(f"Master WAV exported to {wav_path}")

    # Render Triptych Analysis Plate
    render_triptych_plate(out_l, out_r, stress_record, bit_record, fault_flags, sample_rate, duration_sec, "sketchbook/study_007_triptych_analysis.png")

def render_triptych_plate(sig_l, sig_r, stress, bits, faults, sample_rate, duration, output_path):
    """Renders a comprehensive 3-panel archival analysis plate (2800 x 1200)."""
    print(f"Rendering triptych analysis plate to {output_path}...")
    canvas_w, canvas_h = 2800, 1200
    canvas = Image.new("RGB", (canvas_w, canvas_h), color=(7, 9, 12))
    draw = ImageDraw.Draw(canvas)

    # Margins and panel widths
    top_m = 100
    bottom_m = 80
    panel_h = canvas_h - top_m - bottom_m
    side_m = 60
    gap = 40
    
    # 3 panels:
    # Panel 1: Spectrogram (Width = 1100)
    # Panel 2: Phase-Space Lissajous Manifold (Width = 800)
    # Panel 3: Cognitive Stress & Quantization Topology (Width = 700)
    p1_w = 1100
    p2_w = 800
    p3_w = canvas_w - side_m * 2 - gap * 2 - p1_w - p2_w  # 760

    p1_x = side_m
    p2_x = p1_x + p1_w + gap
    p3_x = p2_x + p2_w + gap

    # Draw Header
    draw.text((side_m, 28), "STUDY 007: AUTONOMOUS TECTONIC CLEAVE — TRIPTYCH DIAGNOSTIC ARCHIVE", fill=(220, 235, 250))
    draw.text((side_m, 56), "Coupled Multi-Rate Dynamical Systems (Lorenz Stress Manifold × Thomas Attractor) | 48kHz Stereo", fill=(120, 150, 175))

    # --- PANEL 1: SPECTROGRAM ---
    draw.rectangle([p1_x, top_m, p1_x + p1_w, top_m + panel_h], outline=(40, 55, 70), width=1)
    draw.text((p1_x + 16, top_m + 16), "PANEL I: TIME-FREQUENCY SPECTRAL DEFORMATION", fill=(180, 210, 230))

    # Compute STFT
    n_fft = 2048
    hop = 512
    num_frames = (len(sig_l) - n_fft) // hop
    window = np.hanning(n_fft)
    spec = np.zeros((n_fft // 2 + 1, num_frames), dtype=np.float32)
    for f in range(num_frames):
        chunk = sig_l[f * hop : f * hop + n_fft] * window
        spec[:, f] = np.abs(np.fft.rfft(chunk))

    spec_db = 20.0 * np.log10(spec + 1e-9)
    max_db = np.max(spec_db)
    spec_norm = np.clip((spec_db - (max_db - 75.0)) / 75.0, 0.0, 1.0)

    # Plot area inside Panel 1
    sp_x = p1_x + 60
    sp_y = top_m + 50
    sp_w = p1_w - 80
    sp_h = panel_h - 90

    f_min, f_max = 20.0, sample_rate / 2.0
    freqs = np.fft.rfftfreq(n_fft, 1.0 / sample_rate)

    palette = [
        (0.00, (7, 9, 12)),
        (0.18, (12, 24, 34)),
        (0.40, (16, 68, 86)),
        (0.68, (35, 175, 195)),
        (0.88, (140, 235, 245)),
        (1.00, (255, 255, 255))
    ]
    def color_lookup(v):
        for k in range(len(palette) - 1):
            if v <= palette[k+1][0]:
                r = (v - palette[k][0]) / (palette[k+1][0] - palette[k][0] + 1e-5)
                c0 = palette[k][1]
                c1 = palette[k+1][1]
                return (int(c0[0] + r * (c1[0] - c0[0])),
                        int(c0[1] + r * (c1[1] - c0[1])),
                        int(c0[2] + r * (c1[2] - c0[2])))
        return (255, 255, 255)

    spec_pixels = np.zeros((sp_h, sp_w, 3), dtype=np.uint8)
    x_indices = (np.linspace(0, num_frames - 1, sp_w)).astype(int)
    for py in range(sp_h):
        log_frac = 1.0 - (py / sp_h)
        target_f = f_min * ((f_max / f_min) ** log_frac)
        f_idx = min(len(freqs) - 1, np.searchsorted(freqs, target_f))
        row = spec_norm[f_idx, x_indices]
        for px in range(sp_w):
            spec_pixels[py, px] = color_lookup(row[px])

    spec_img = Image.fromarray(spec_pixels, mode="RGB")
    canvas.paste(spec_img, (sp_x, sp_y))
    draw.rectangle([sp_x, sp_y, sp_x + sp_w, sp_y + sp_h], outline=(60, 80, 100), width=1)

    # Fault indicators on spectrogram
    downsample_step = len(faults) // sp_w
    for px in range(sp_w):
        sample_idx = px * downsample_step
        if faults[sample_idx]:
            # Tiny rupture tick at bottom of spectrogram
            draw.line([(sp_x + px, sp_y + sp_h - 10), (sp_x + px, sp_y + sp_h)], fill=(255, 80, 70), width=1)

    # Time ticks
    for sec in range(0, int(duration) + 1, 10):
        tx = sp_x + int((sec / duration) * sp_w)
        draw.line([(tx, sp_y + sp_h), (tx, sp_y + sp_h + 6)], fill=(100, 130, 150))
        draw.text((tx - 10, sp_y + sp_h + 10), f"{sec}s", fill=(130, 160, 180))

    # --- PANEL 2: PHASE SPACE DENSITY (Lissajous Manifold) ---
    draw.rectangle([p2_x, top_m, p2_x + p2_w, top_m + panel_h], outline=(40, 55, 70), width=1)
    draw.text((p2_x + 16, top_m + 16), "PANEL II: STEREO PHASE SPACE MANIFOLD [L(t) vs R(t)]", fill=(180, 210, 230))

    ps_size = min(p2_w - 40, panel_h - 70)
    ps_ox = p2_x + (p2_w - ps_size) // 2
    ps_oy = top_m + 50 + (panel_h - 70 - ps_size) // 2

    accum = np.zeros((ps_size, ps_size), dtype=np.uint32)
    step = 1
    xs = ((sig_l[::step] * 0.45 + 0.5) * (ps_size - 1)).astype(int)
    ys = (((-sig_r[::step]) * 0.45 + 0.5) * (ps_size - 1)).astype(int)
    val = (xs >= 0) & (xs < ps_size) & (ys >= 0) & (ys < ps_size)
    np.add.at(accum, (ys[val], xs[val]), 1)

    log_acc = np.log1p(accum.astype(np.float64))
    m_log = np.max(log_acc)
    n_acc = log_acc / (m_log if m_log > 0 else 1.0)

    ps_rgb = np.zeros((ps_size, ps_size, 3), dtype=np.uint8)
    ps_rgb[:, :, 0] = (8 + n_acc * 210 * (n_acc > 0.45) + n_acc**3 * 45).clip(0, 255).astype(np.uint8)
    ps_rgb[:, :, 1] = (10 + n_acc * 230 + n_acc**2 * 25).clip(0, 255).astype(np.uint8)
    ps_rgb[:, :, 2] = (14 + n_acc * 245).clip(0, 255).astype(np.uint8)

    ps_img = Image.fromarray(ps_rgb, mode="RGB")
    canvas.paste(ps_img, (ps_ox, ps_oy))
    draw.rectangle([ps_ox, ps_oy, ps_ox + ps_size, ps_oy + ps_size], outline=(60, 80, 100), width=1)

    # --- PANEL 3: STRESS TENSOR & QUANTIZATION TOPOLOGY ---
    draw.rectangle([p3_x, top_m, p3_x + p3_w, top_m + panel_h], outline=(40, 55, 70), width=1)
    draw.text((p3_x + 16, top_m + 16), "PANEL III: COGNITIVE STRESS & BIT TOPOLOGY", fill=(180, 210, 230))

    graph_x = p3_x + 50
    graph_w = p3_w - 80
    
    # Subgraph A: Stress Tensor (Top half)
    sub1_y = top_m + 60
    sub1_h = (panel_h - 130) // 2
    draw.rectangle([graph_x, sub1_y, graph_x + graph_w, sub1_y + sub1_h], outline=(50, 70, 85), width=1)
    draw.text((graph_x + 10, sub1_y + 8), "Lorenz Cognitive Stress Tensor ||S(t)||", fill=(220, 150, 140))
    # Rupture threshold line
    thresh_y = sub1_y + int(sub1_h * (1.0 - 1.25 / 2.5))
    draw.line([(graph_x, thresh_y), (graph_x + graph_w, thresh_y)], fill=(255, 70, 60), width=1)
    draw.text((graph_x + graph_w - 110, thresh_y - 14), "RUPTURE THRESHOLD", fill=(255, 90, 80))

    # Plot stress curve
    stress_downsample = len(stress) // graph_w
    stress_pts = []
    for gx in range(graph_w):
        s_val = stress[gx * stress_downsample]
        sy_pix = sub1_y + int(sub1_h * (1.0 - min(2.5, s_val) / 2.5))
        stress_pts.append((graph_x + gx, sy_pix))
    if len(stress_pts) > 1:
        draw.line(stress_pts, fill=(240, 180, 100), width=2)

    # Subgraph B: Bit-Depth Quantization Strata (Bottom half)
    sub2_y = sub1_y + sub1_h + 30
    sub2_h = sub1_h
    draw.rectangle([graph_x, sub2_y, graph_x + graph_w, sub2_y + sub2_h], outline=(50, 70, 85), width=1)
    draw.text((graph_x + 10, sub2_y + 8), "Effective Quantization Depth (16-bit → 3-bit)", fill=(100, 200, 220))

    bit_pts = []
    for gx in range(graph_w):
        b_val = bits[gx * stress_downsample]
        by_pix = sub2_y + int(sub2_h * (1.0 - (b_val - 2.0) / 14.0))
        bit_pts.append((graph_x + gx, by_pix))
    if len(bit_pts) > 1:
        draw.line(bit_pts, fill=(50, 215, 235), width=2)

    # Draw bit ticks
    for bt in [4, 8, 12, 16]:
        b_pix = sub2_y + int(sub2_h * (1.0 - (bt - 2.0) / 14.0))
        draw.line([(graph_x - 5, b_pix), (graph_x, b_pix)], fill=(80, 110, 130))
        draw.text((graph_x - 35, b_pix - 6), f"{bt}b", fill=(120, 150, 170))

    canvas.save(output_path, "PNG")
    print(f"Triptych plate saved to {output_path}")

if __name__ == "__main__":
    generate_study_007()
