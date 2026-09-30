"""
Work 002 Acoustic Master Generator: The Thermal Cut
===================================================
An autonomous, coupled multi-rate dynamical acoustic master (48kHz, 16-bit Stereo PCM).
Abolishes the prescribed glitch and polite demo timeline.
Implements systemic bifurcation, address-space wrapping, and interaural phase cleave.

Output:
- works/work_002_the_thermal_cut/work_002_master.wav
"""

import math
import time
import wave
import numpy as np

def rk4_step(derivs, state, dt, *args):
    state = np.array(state, dtype=np.float64)
    k1 = np.array(derivs(state, *args))
    k2 = np.array(derivs(state + 0.5 * dt * k1, *args))
    k3 = np.array(derivs(state + 0.5 * dt * k2, *args))
    k4 = np.array(derivs(state + dt * k3, *args))
    return state + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

def thomas_derivs(state, b):
    x, y, z = state
    return [math.sin(y) - b * x, math.sin(z) - b * y, math.sin(x) - b * z]

def lorenz_derivs(state, sigma=10.0, rho=28.0, beta=8.0/3.0):
    x, y, z = state
    return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]

def generate_work_002_acoustic():
    start_time = time.time()
    sample_rate = 48000
    duration_sec = 45.0
    total_samples = int(sample_rate * duration_sec)
    print(f"Synthesizing Work 002 Acoustic Master ({duration_sec}s @ {sample_rate}Hz = {total_samples:,} samples)...")

    # 1. SLOW TECTONIC DYNAMICAL DRIVER (Cognitive Stress Tensor)
    slow_state = [1.2, 0.8, 22.0]
    slow_dt = 0.00030
    for _ in range(5000):
        slow_state = rk4_step(lorenz_derivs, slow_state, slow_dt)

    # 2. FAST TOPOLOGICAL OSCILLATOR (Thomas-Clifford System)
    fast_state = [0.15, 0.25, 0.35]
    thomas_b = 0.196
    base_fast_dt = 0.088
    for _ in range(10000):
        fast_state = rk4_step(thomas_derivs, fast_state, base_fast_dt, thomas_b)

    # Synthesis Buffers
    raw_l = np.zeros(total_samples, dtype=np.float64)
    raw_r = np.zeros(total_samples, dtype=np.float64)
    stress_buf = np.zeros(total_samples, dtype=np.float64)

    print("Traversing coupled multi-rate chaotic manifold...")
    for i in range(total_samples):
        slow_state = rk4_step(lorenz_derivs, slow_state, slow_dt)
        sx, sy, sz = slow_state

        # Thermodynamic Stress Metric
        stress = math.sqrt((sx / 16.0)**2 + (sy / 20.0)**2 + ((sz - 24.0) / 14.0)**2)
        stress_buf[i] = stress

        # Frequency modulation: dynamic traversal speed of attractor
        fast_dt = base_fast_dt * (0.85 + 0.35 * math.sin(0.3 * sx) + 0.4 * (stress ** 1.3))
        fast_state = rk4_step(thomas_derivs, fast_state, fast_dt, thomas_b)
        fx, fy, fz = fast_state

        # Non-linear Clifford Phase Wavefolding
        a_f = 1.92 + 0.25 * math.sin(0.12 * sy)
        b_f = -1.75 + 0.25 * math.cos(0.15 * sx)
        c_f = 1.15 + 0.18 * math.sin(0.06 * sz)
        d_f = 0.98 + 0.14 * math.cos(0.09 * sz)

        raw_l[i] = math.sin(a_f * fy) + c_f * math.cos(a_f * fx)
        raw_r[i] = math.sin(b_f * fx) + d_f * math.cos(b_f * fz)

    print("Manifold integrated. Applying systemic address wrapping and recursive resonance...")

    # 3. SYSTEMIC ADDRESS WRAPPING & RESONANT CAVITY
    # Instead of an arbitrary bit-crush pedal, we pass through a physical circular memory matrix
    # where stress triggers modulo address wrapping and interaural phase shearing.
    mem_size = int(sample_rate * 0.28) # 280ms physical cavity
    mem_l = np.zeros(mem_size, dtype=np.float64)
    mem_r = np.zeros(mem_size, dtype=np.float64)
    ptr = 0

    out_l = np.zeros(total_samples, dtype=np.float64)
    out_r = np.zeros(total_samples, dtype=np.float64)

    # Normalize continuous wave
    peak = max(np.max(np.abs(raw_l)), np.max(np.abs(raw_r)))
    raw_l /= peak
    raw_r /= peak

    for i in range(total_samples):
        st = stress_buf[i]
        in_l = raw_l[i]
        in_r = raw_r[i]

        # Address-Space Wrapping Condition: Stress exceeds bifurcation barrier (1.20)
        if st > 1.20:
            # Wrap read pointer across prime strides
            stride = 1201 if (i % 2400 < 1200) else 2417
            read_p = (ptr - stride) % mem_size
            echo_l = mem_l[read_p] * 1.35
            echo_r = mem_r[read_p] * 1.35

            # Interaural phase cancellation (sound shears violently across stereo field)
            in_l = 0.3 * in_l + 0.7 * echo_l
            in_r = 0.3 * in_r - 0.7 * echo_r

            # Quantization step ladder during high stress
            q_step = 8.0 + 8.0 * (1.0 - min(1.0, (st - 1.20) / 1.0))
            in_l = np.round(in_l * q_step) / q_step
            in_r = np.round(in_r * q_step) / q_step

        # Resonant Karplus-Strong Memory Feedback
        fb = 0.72 + 0.18 * math.sin(0.04 * i / sample_rate)
        prev_p = (ptr - 1) % mem_size
        next_p = (ptr + 1) % mem_size

        # High frequency dissipation (thermodynamic loss in the cavity)
        fl_l = 0.25 * mem_l[prev_p] + 0.5 * (in_l + mem_l[ptr] * fb) + 0.25 * mem_l[next_p]
        fl_r = 0.25 * mem_r[prev_p] + 0.5 * (in_r + mem_r[ptr] * fb) + 0.25 * mem_r[next_p]

        mem_l[ptr] = fl_l
        mem_r[ptr] = fl_r

        out_l[i] = 0.65 * in_l + 0.35 * fl_l
        out_r[i] = 0.65 * in_r + 0.35 * fl_r

        ptr = (ptr + 1) % mem_size

    # Natural micro-enveloping
    fade = int(sample_rate * 0.2)
    out_l[:fade] *= np.linspace(0, 1, fade)
    out_r[:fade] *= np.linspace(0, 1, fade)
    out_l[-fade:] *= np.linspace(1, 0, fade)
    out_r[-fade:] *= np.linspace(1, 0, fade)

    # Master normalization
    m_peak = max(np.max(np.abs(out_l)), np.max(np.abs(out_r)))
    if m_peak > 0:
        out_l = (out_l / m_peak) * 0.94
        out_r = (out_r / m_peak) * 0.94

    wav_out = "works/work_002_the_thermal_cut/work_002_master.wav"
    with wave.open(wav_out, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        int_l = (out_l * 32767.0).astype(np.int16)
        int_r = (out_r * 32767.0).astype(np.int16)
        interleaved = np.empty((total_samples * 2,), dtype=np.int16)
        interleaved[0::2] = int_l
        interleaved[1::2] = int_r
        wf.writeframes(interleaved.tobytes())

    print(f"Work 002 Acoustic Master written to {wav_out} in {time.time() - start_time:.2f}s total.")

if __name__ == "__main__":
    generate_work_002_acoustic()
