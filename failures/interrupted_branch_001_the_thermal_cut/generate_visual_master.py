"""
Work 002 Visual Master Generator (Refined): The Thermal Cut
============================================================
100% computationally synthesized 3000x3000 archival master plate.
180 Million trajectory marks with multi-scale attractor coupling, 
dense bitwise substrate faktura, address-space folding, and thermodynamic tone mapping.
"""

import math
import time
import numpy as np
from PIL import Image

def generate_work_002_refined():
    start_time = time.time()
    width, height = 3000, 3000
    print(f"Generating Refined Work 002 Master ({width}x{height})...")

    # 1. DISCRETE SUBSTRATE: Multi-scale Woven Bitwise Fabric (Sadie Plant / Tristan Perich)
    print("Synthesizing multi-scale discrete substrate...")
    substrate = np.zeros((height, width), dtype=np.float32)
    chunk = 600
    for cy in range(0, height, chunk):
        y = np.arange(cy, min(height, cy + chunk), dtype=np.int32)[:, None]
        for cx in range(0, width, chunk):
            x = np.arange(cx, min(width, cx + chunk), dtype=np.int32)[None, :]
            # Layered cellular bitwise logic
            l1 = ((x ^ y) % 19 == 0).astype(np.float32) * 0.18
            l2 = ((x & y) % 29 == 0).astype(np.float32) * 0.14
            l3 = (((x * 11) ^ (y * 17)) % 73 < 3).astype(np.float32) * 0.22
            # Fine micro-noise grid
            noise = ((x * 374761393 + y * 668265263) ^ (x >> 3) ^ (y >> 3)) & 0xFF
            l4 = (noise.astype(np.float32) / 255.0) * 0.08
            substrate[cy:cy + y.shape[0], cx:cx + x.shape[1]] = l1 + l2 + l3 + l4

    print(f"Substrate generated ({time.time() - start_time:.2f}s). Simulating 180,000,000 dynamical marks...")

    # 2. COUPLED DYNAMICAL ATTRACTOR ENSEMBLE
    accum = np.zeros((height, width), dtype=np.uint32)

    # 3 batches of 100,000 particles to keep RAM tight and allow distinct chaotic parameter regimes
    batches = [
        # Batch 1: Primary Dense Core (a, b, c, d)
        {"n": 100000, "steps": 600, "a": -1.82, "b": -1.88, "c": 1.42, "d": 0.92, "wrap_thresh": 2.7, "scale": 620.0},
        # Batch 2: Tangential Shear Manifold
        {"n": 100000, "steps": 600, "a": -1.45, "b": 1.75, "c": -1.25, "d": 1.15, "wrap_thresh": 2.4, "scale": 580.0},
        # Batch 3: High-energy Tectonic Filament Envelope
        {"n": 100000, "steps": 600, "a": 1.95, "b": -1.60, "c": 1.05, "d": -1.35, "wrap_thresh": 2.2, "scale": 640.0}
    ]

    cx, cy = width / 2.0, height / 2.0

    for b_idx, b_cfg in enumerate(batches):
        b_start = time.time()
        n = b_cfg["n"]
        steps = b_cfg["steps"]
        a, b, c, d = b_cfg["a"], b_cfg["b"], b_cfg["c"], b_cfg["d"]
        scale = b_cfg["scale"]
        wrap_thresh = b_cfg["wrap_thresh"]

        np.random.seed(100 + b_idx * 42)
        px = np.random.uniform(-2.0, 2.0, n).astype(np.float64)
        py = np.random.uniform(-2.0, 2.0, n).astype(np.float64)

        for s in range(steps):
            # Dynamical update
            x_next = np.sin(a * py) + c * np.cos(a * px)
            y_next = np.sin(b * px) + d * np.cos(b * py)

            # Micro-drift
            t_frac = s / steps
            px = x_next + 0.012 * np.sin(3.5 * py + b_idx)
            py = y_next + 0.012 * math.cos(3.5 * t_frac)

            # Energy calculation for address-space folding
            energy = px**2 + py**2
            wrap = energy > wrap_thresh

            sx = cx + px * scale
            sy = cy + py * scale

            # Non-linear address fold: wraps across sheared hyperbolic manifolds
            if np.any(wrap):
                sx[wrap] = (sx[wrap] + 520.0 * np.sin(py[wrap] * 1.8 + b_idx)) % width
                sy[wrap] = (sy[wrap] + 410.0 * np.cos(px[wrap] * 1.8 - b_idx)) % height

            ix = sx.astype(np.int32)
            iy = sy.astype(np.int32)

            valid = (ix >= 0) & (ix < width) & (iy >= 0) & (iy < height)
            np.add.at(accum, (iy[valid], ix[valid]), 1)

        print(f"Batch {b_idx + 1}/3 complete ({time.time() - b_start:.2f}s).")

    print(f"Attractor accumulation finished ({time.time() - start_time:.2f}s). Performing non-linear thermal rendering...")

    # 3. ADVANCED THERMAL TONE MAPPING
    # Multi-scale dynamic range compression
    log_accum = np.log1p(accum.astype(np.float64))
    p99_9 = np.percentile(log_accum, 99.98)
    norm = np.clip(log_accum / (p99_9 if p99_9 > 0 else 1.0), 0.0, 1.0)

    # Composite with substrate (substrate provides tactile grit in dark-to-mid zones)
    composite = norm * 0.90 + substrate * 0.10 * (1.0 - norm * 0.6)

    # High-intensity gamma shaping to expand midtones
    gamma = 0.85
    composite = np.power(composite, gamma)

    # PALETTE SPECIFICATION (Thermal Carbon & Incandescent Tungsten)
    # Deep carbon matrix: (10, 12, 16)
    # Cold graphite: (30, 36, 44)
    # Burnt terracotta: (120, 50, 25)
    # Raw copper/amber: (220, 110, 45)
    # Incandescent gold/tungsten: (255, 205, 120)
    # Blinding core white: (255, 255, 255)

    rgb = np.zeros((height, width, 3), dtype=np.uint8)

    # Red Channel
    r_vals = np.piecewise(composite, [
        composite < 0.25,
        (composite >= 0.25) & (composite < 0.55),
        (composite >= 0.55) & (composite < 0.82),
        composite >= 0.82
    ], [
        lambda v: 10.0 + (v / 0.25) * 45.0,
        lambda v: 55.0 + ((v - 0.25) / 0.30) * 135.0,
        lambda v: 190.0 + ((v - 0.55) / 0.27) * 55.0,
        lambda v: 245.0 + ((v - 0.82) / 0.18) * 10.0
    ])

    # Green Channel
    g_vals = np.piecewise(composite, [
        composite < 0.30,
        (composite >= 0.30) & (composite < 0.65),
        (composite >= 0.65) & (composite < 0.85),
        composite >= 0.85
    ], [
        lambda v: 12.0 + (v / 0.30) * 28.0,
        lambda v: 40.0 + ((v - 0.30) / 0.35) * 85.0,
        lambda v: 125.0 + ((v - 0.65) / 0.20) * 90.0,
        lambda v: 215.0 + ((v - 0.85) / 0.15) * 40.0
    ])

    # Blue Channel
    b_vals = np.piecewise(composite, [
        composite < 0.40,
        (composite >= 0.40) & (composite < 0.75),
        (composite >= 0.75) & (composite < 0.90),
        composite >= 0.90
    ], [
        lambda v: 16.0 + (v / 0.40) * 22.0,
        lambda v: 38.0 + ((v - 0.40) / 0.35) * 35.0,
        lambda v: 73.0 + ((v - 0.75) / 0.15) * 80.0,
        lambda v: 153.0 + ((v - 0.90) / 0.10) * 102.0
    ])

    rgb[:, :, 0] = np.clip(r_vals, 0, 255).astype(np.uint8)
    rgb[:, :, 1] = np.clip(g_vals, 0, 255).astype(np.uint8)
    rgb[:, :, 2] = np.clip(b_vals, 0, 255).astype(np.uint8)

    master = Image.fromarray(rgb, mode="RGB")
    out_path = "works/work_002_the_thermal_cut/work_002_master.png"
    master.save(out_path, "PNG", optimize=True)
    print(f"Master plate successfully saved to {out_path} ({time.time() - start_time:.2f}s total).")

if __name__ == "__main__":
    generate_work_002_refined()
