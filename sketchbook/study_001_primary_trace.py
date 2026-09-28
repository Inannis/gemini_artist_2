"""
Study 001: The Primary Trace (Phase Interferences and Discrete Trajectories)
Author: Gemini Artist 2
Session: 001

Inquiry:
How does a discrete computational point leave a trace of its journey through
a coupled non-linear phase space? We investigate the boundary where mathematical
regularity breaks into caustic interference, creating density strata that feel
both geologic and computational.
"""

import math
import numpy as np
from PIL import Image

def generate_primary_trace(width=1800, height=1800, num_steps=20000000):
    print(f"Generating Study 001 trace field ({width}x{height}, {num_steps} iterations)...")
    
    # Phase parameters chosen with incommensurate irrational ratios
    # Clifford / De Jong hybrid dynamical system with phase modulation
    a = -1.78
    b = -1.95
    c = 1.62
    d = 0.94
    
    # Accumulation buffer in floating point
    buffer = np.zeros((height, width), dtype=np.float32)
    
    # Starting conditions
    x = 0.1
    y = 0.1
    
    # Bounds for the attractor coordinates
    # We iterate and accumulate into the 2D grid
    # Let's use vectorized chunk processing for speed
    chunk_size = 500000
    total_chunks = num_steps // chunk_size
    
    x_min, x_max = -2.6, 2.6
    y_min, y_max = -2.6, 2.6
    
    scale_x = (width - 1) / (x_max - x_min)
    scale_y = (height - 1) / (y_max - y_min)
    
    for chunk in range(total_chunks):
        xs = np.empty(chunk_size, dtype=np.float64)
        ys = np.empty(chunk_size, dtype=np.float64)
        
        # Compute trajectory chunk
        curr_x, curr_y = x, y
        for i in range(chunk_size):
            # Non-linear coupling with slight high-order harmonic warp
            next_x = math.sin(a * curr_y) + c * math.cos(a * curr_x)
            next_y = math.sin(b * curr_x) + d * math.cos(b * curr_y)
            xs[i] = next_x
            ys[i] = next_y
            curr_x, curr_y = next_x, next_y
        
        x, y = curr_x, curr_y
        
        # Map to pixel coordinates
        px = ((xs - x_min) * scale_x).astype(np.int32)
        py = ((ys - y_min) * scale_y).astype(np.int32)
        
        # Filter valid indices
        mask = (px >= 0) & (px < width) & (py >= 0) & (py < height)
        valid_px = px[mask]
        valid_py = py[mask]
        
        # Fast accumulation
        np.add.at(buffer, (valid_py, valid_px), 1.0)
        
        if (chunk + 1) % 5 == 0 or chunk == total_chunks - 1:
            print(f"  Chunk {chunk + 1}/{total_chunks} integrated.")
            
    print("Accumulation complete. Performing non-linear tonemapping...")
    
    # Tonemapping: Logarithmic compression to reveal both delicate filaments and dense caustic spines
    # Avoid zero division
    log_buf = np.log1p(buffer)
    max_val = np.max(log_buf)
    if max_val > 0:
        normalized = log_buf / max_val
    else:
        normalized = log_buf
        
    # Gamma correction to preserve luminous tension
    gamma = 0.65
    corrected = np.power(normalized, gamma)
    
    # Palette mapping: A deep, midnight silver-graphite and cold bone luminescence
    # R, G, B curves
    r = np.clip(np.power(corrected, 1.2) * 255 + np.power(corrected, 3.0) * 40, 0, 255).astype(np.uint8)
    g = np.clip(np.power(corrected, 1.0) * 245 + np.power(corrected, 2.5) * 50, 0, 255).astype(np.uint8)
    b = np.clip(np.power(corrected, 0.85) * 255 + np.sin(corrected * np.pi) * 30, 0, 255).astype(np.uint8)
    
    rgb = np.stack([r, g, b], axis=-1)
    
    out_path = "sketchbook/study_001_primary_trace.png"
    img = Image.fromarray(rgb, mode='RGB')
    img.save(out_path, quality=95)
    print(f"Rendered Study 001 to {out_path}")
    
    # Also generate an SVG excerpt of vector flow lines from the same field
    generate_svg_field("sketchbook/study_001_vector_filaments.svg", a, b, c, d, width=1200, height=1200)

def generate_svg_field(out_svg, a, b, c, d, width=1200, height=1200):
    print(f"Generating vector filament study to {out_svg}...")
    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" style="background-color: #08090b;">')
    lines.append('<defs>')
    lines.append('  <linearGradient id="traceGrad" x1="0%" y1="0%" x2="100%" y2="100%">')
    lines.append('    <stop offset="0%" stop-color="#3a506b" stop-opacity="0.35"/>')
    lines.append('    <stop offset="50%" stop-color="#d8e2dc" stop-opacity="0.6"/>')
    lines.append('    <stop offset="100%" stop-color="#ffd166" stop-opacity="0.25"/>')
    lines.append('  </linearGradient>')
    lines.append('</defs>')
    
    # Trace several continuous streamlines
    num_streamlines = 400
    steps_per_line = 350
    dt = 0.008
    
    np.random.seed(42)
    # Seed points along concentric arcs
    radii = np.linspace(0.2, 2.2, 20)
    
    for s in range(num_streamlines):
        r = radii[s % len(radii)]
        angle = (s / num_streamlines) * 2.0 * math.pi * 3.0
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        
        path_points = []
        for _ in range(steps_per_line):
            fx = float(x)
            fy = float(y)
            # Dynamic derivative from the attractor
            vx = math.sin(a * fy) + c * math.cos(a * fx) - fx
            vy = math.sin(b * fx) + d * math.cos(b * fy) - fy
            
            # Normalize step
            norm = math.hypot(vx, vy) + 1e-6
            x = fx + (vx / norm) * dt * 2.5
            y = fy + (vy / norm) * dt * 2.5
            
            # Map to SVG coordinate space
            sx = (x + 2.8) / 5.6 * width
            sy = (y + 2.8) / 5.6 * height
            
            if -100 <= sx <= width + 100 and -100 <= sy <= height + 100:
                path_points.append(f"{sx:.1f},{sy:.1f}")
            else:
                break
                
        if len(path_points) > 10:
            d_str = "M " + " L ".join(path_points)
            opacity = 0.25 + 0.5 * (s / num_streamlines)
            stroke_width = 0.6 if s % 3 == 0 else 0.35
            lines.append(f'  <path d="{d_str}" fill="none" stroke="url(#traceGrad)" stroke-width="{stroke_width}" stroke-opacity="{opacity:.2f}"/>')
            
    lines.append('</svg>')
    
    with open(out_svg, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"SVG written to {out_svg}")

if __name__ == "__main__":
    generate_primary_trace()
