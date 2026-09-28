"""
Study 002: Corrupted Strata (Substrate Fracture, Quantization Drift, and Spatially Modulated Dynamics)
Author: Gemini Artist 2
Session: 001

Inquiry:
To overcome the centered, decorative trap of Study 001, Study 002 subjects the
field to spatially varying phase parameters, discrete coordinate quantization
faults, and anisotropic memory shearing. The image must occupy the full frame
with the density of an excavated geological/digital tablet.
"""

import math
import numpy as np
from PIL import Image

def generate_corrupted_strata(width=2000, height=2000, num_steps=25000000):
    print(f"Executing Study 002: Corrupted Strata ({width}x{height}, {num_steps} iterations)...")
    
    # Accumulation buffers
    # buffer_fine: records continuous flow filaments
    # buffer_shear: records discrete coordinate fault slip
    buffer_fine = np.zeros((height, width), dtype=np.float32)
    buffer_shear = np.zeros((height, width), dtype=np.float32)
    
    # Spatially modulated attractor parameters:
    # Instead of constant a, b, c, d, they vary across the domain
    # creating distinct dynamical regimes across the surface.
    
    chunk_size = 500000
    total_chunks = num_steps // chunk_size
    
    # We use multiple trajectories seeded in an asymmetric perimeter lattice
    num_seeds = 16
    seed_xs = np.linspace(-2.2, 2.2, 4)
    seed_ys = np.linspace(-2.2, 2.2, 4)
    seeds = [(x, y) for x in seed_xs for y in seed_ys]
    
    x_min, x_max = -2.8, 2.8
    y_min, y_max = -2.8, 2.8
    
    scale_x = (width - 1) / (x_max - x_min)
    scale_y = (height - 1) / (y_max - y_min)
    
    curr_x, curr_y = 0.25, -0.45
    
    for chunk in range(total_chunks):
        # Periodically re-seed or inject disturbance
        if chunk % 8 == 0:
            s_idx = (chunk // 8) % len(seeds)
            curr_x, curr_y = seeds[s_idx]
            curr_x += np.random.uniform(-0.05, 0.05)
            curr_y += np.random.uniform(-0.05, 0.05)
            
        xs = np.empty(chunk_size, dtype=np.float64)
        ys = np.empty(chunk_size, dtype=np.float64)
        
        # We run the dynamical update with spatial parameter modulation
        for i in range(chunk_size):
            # Spatially modulated parameters
            # Modulate according to position to shatter global symmetry
            pos_factor = math.sin(0.7 * curr_x + 0.3 * curr_y)
            a = -1.85 + 0.35 * pos_factor
            b = -2.05 - 0.25 * math.cos(0.5 * curr_y)
            c = 1.45 + 0.40 * math.sin(curr_x * curr_y)
            d = 0.88 + 0.20 * math.cos(curr_x)
            
            # Non-linear phase equation
            next_x = math.sin(a * curr_y) + c * math.cos(a * curr_x)
            next_y = math.sin(b * curr_x) + d * math.cos(b * curr_y)
            
            # Introduce non-linear fold / threshold fracture
            # If the trajectory crosses certain bands, apply a micro-quantization
            if abs(next_x) > 1.4:
                # Quantization shear: snap to stepped grid levels
                next_x = round(next_x * 32.0) / 32.0
            if abs(next_y) < 0.6:
                next_y = next_y + 0.015 * math.sin(40.0 * next_x)
                
            xs[i] = next_x
            ys[i] = next_y
            curr_x, curr_y = next_x, next_y
            
        # Map to pixel coordinates
        px = ((xs - x_min) * scale_x).astype(np.int32)
        py = ((ys - y_min) * scale_y).astype(np.int32)
        
        mask = (px >= 0) & (px < width) & (py >= 0) & (py < height)
        valid_px = px[mask]
        valid_py = py[mask]
        
        # Accumulate into fine buffer
        np.add.at(buffer_fine, (valid_py, valid_px), 1.0)
        
        # Produce discrete shear traces on high-curvature points
        # Every 4th step, accumulate with a horizontal dislocation
        if chunk % 2 == 0:
            shear_offset = (np.sin(valid_py * 0.02) * 18.0).astype(np.int32)
            px_sheared = np.clip(valid_px + shear_offset, 0, width - 1)
            np.add.at(buffer_shear, (valid_py, px_sheared), 0.75)
            
        if (chunk + 1) % 10 == 0 or chunk == total_chunks - 1:
            print(f"  Integrated {chunk + 1}/{total_chunks} chunks...")
            
    print("Accumulation complete. Synthesizing stratigraphic layers...")
    
    # Combine buffers with weighted tension
    # Non-linear compression
    log_fine = np.log1p(buffer_fine)
    log_fine /= (np.max(log_fine) + 1e-6)
    
    log_shear = np.log1p(buffer_shear)
    log_shear /= (np.max(log_shear) + 1e-6)
    
    # Layer 1: Base strata
    # Contrast curve
    layer_base = np.power(log_fine, 0.75)
    
    # Layer 2: Fault lines and dislocations
    layer_fault = np.power(log_shear, 1.1)
    
    # Layer 3: Substrate digital interference / scanlines
    # Generate horizontal micro-striations and vertical memory artifacts
    y_coords, x_coords = np.mgrid[0:height, 0:width]
    scanlines = 0.035 * np.sin(y_coords * 0.85) + 0.02 * np.cos(x_coords * 0.4 + y_coords * 0.2)
    # Memory blocks / stride dropouts
    block_noise = ((x_coords // 128 + y_coords // 64) % 7 == 0).astype(np.float32) * 0.025
    
    composite = layer_base * 0.75 + layer_fault * 0.35 + scanlines + block_noise
    composite = np.clip(composite, 0.0, 1.0)
    
    # High-pass micro-relief filter to give physical lithographic tooth
    print("Applying structural relief tooth...")
    # Shift-difference gradient for tactile edges
    grad_x = np.diff(composite, axis=1, prepend=composite[:, :1])
    grad_y = np.diff(composite, axis=0, prepend=composite[:1, :])
    relief = np.sqrt(grad_x**2 + grad_y**2)
    relief /= (np.max(relief) + 1e-6)
    
    final_field = composite * 0.88 + relief * 0.22
    final_field = np.clip(final_field, 0.0, 1.0)
    
    # Mineral Palette Construction:
    # Deep iron-black, oxidized slate, wet bitumen, raw titanium white with faint sulfur ochre in the mid-tones
    # R: rich midtones with warm amber-ochre inflection in the fractures
    r = np.clip(
        np.power(final_field, 1.35) * 230 + 
        np.power(final_field, 2.5) * 45 + 
        np.sin(final_field * np.pi) * 35 * (layer_fault), 
        0, 255
    ).astype(np.uint8)
    
    # G: mineral slate and oxidized zinc
    g = np.clip(
        np.power(final_field, 1.15) * 235 + 
        np.power(final_field, 3.0) * 30 + 
        layer_fault * 15, 
        0, 255
    ).astype(np.uint8)
    
    # B: cold graphite, deep twilight undertone
    b = np.clip(
        np.power(final_field, 0.95) * 245 + 
        np.cos(final_field * np.pi * 0.5) * 18, 
        0, 255
    ).astype(np.uint8)
    
    # Add subtle grain noise to prevent digital flatness
    grain = np.random.normal(0, 3.0, (height, width))
    r = np.clip(r.astype(np.float32) + grain, 0, 255).astype(np.uint8)
    g = np.clip(g.astype(np.float32) + grain, 0, 255).astype(np.uint8)
    b = np.clip(b.astype(np.float32) + grain, 0, 255).astype(np.uint8)
    
    rgb = np.stack([r, g, b], axis=-1)
    
    out_path = "sketchbook/study_002_corrupted_strata.png"
    img = Image.fromarray(rgb, mode='RGB')
    img.save(out_path, quality=96)
    print(f"Study 002 successfully rendered and saved to {out_path}!")

if __name__ == "__main__":
    generate_corrupted_strata()

