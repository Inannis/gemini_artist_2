"""
Study 004: Hybrid Palimpsest (Mathematical Stress on Latent Memory)
Author: Gemini Artist 2
Session: 001

Methodology:
Fuses the tactile archaeological reality of Study 003 (latent fossil) with the
structural and discrete quantization shear forces of Study 002 (algorithmic dynamics).
The latent stone/silicon matrix is subjected to coordinate displacement, acid-etch
intaglio channels along caustic ridges, and discrete block-fault slip.
"""

import math
import hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def create_hybrid_palimpsest(
    fossil_path="sketchbook/study_003_latent_fossil.jpg",
    out_path="sketchbook/study_004_hybrid_palimpsest.png",
    canvas_size=2400
):
    print(f"Loading latent fossil substrate from {fossil_path}...")
    fossil_img = Image.open(fossil_path).convert("RGB")
    
    # Crop out the lower 12% narrative scale bar (the clichéd archaeological trope)
    w_orig, h_orig = fossil_img.size
    crop_h = int(h_orig * 0.88)
    cropped_fossil = fossil_img.crop((0, 0, w_orig, crop_h))
    
    # Resize and place centrally into a slate-black archival tablet
    inner_size = 1800
    resized_fossil = cropped_fossil.resize((inner_size, inner_size), Image.Resampling.LANCZOS)
    
    # Create canvas
    canvas = np.zeros((canvas_size, canvas_size, 3), dtype=np.float32)
    # Background slate tone: very dark carbon graphite with faint mineral noise
    bg_noise = np.random.normal(14.0, 2.5, (canvas_size, canvas_size, 3))
    canvas += bg_noise
    
    # Place fossil in center
    offset = (canvas_size - inner_size) // 2
    fossil_arr = np.array(resized_fossil, dtype=np.float32)
    canvas[offset:offset+inner_size, offset:offset+inner_size] = fossil_arr
    
    print("Generating coupled dynamic stress tensor field (30M iterations)...")
    field_size = inner_size
    acc_buffer = np.zeros((field_size, field_size), dtype=np.float32)
    shear_buffer = np.zeros((field_size, field_size), dtype=np.float32)
    
    num_steps = 30000000
    chunk_size = 1000000
    total_chunks = num_steps // chunk_size
    
    # Dynamical parameters
    a_base = -1.82
    b_base = -1.98
    c_base = 1.55
    d_base = 0.91
    
    x_min, x_max = -2.7, 2.7
    y_min, y_max = -2.7, 2.7
    scale_x = (field_size - 1) / (x_max - x_min)
    scale_y = (field_size - 1) / (y_max - y_min)
    
    curr_x, curr_y = 0.15, -0.35
    np.random.seed(101)
    
    for chunk in range(total_chunks):
        if chunk % 5 == 0:
            curr_x = np.random.uniform(-1.5, 1.5)
            curr_y = np.random.uniform(-1.5, 1.5)
            
        xs = np.empty(chunk_size, dtype=np.float64)
        ys = np.empty(chunk_size, dtype=np.float64)
        
        for i in range(chunk_size):
            # Spatially modulated attractor
            a = a_base + 0.15 * math.sin(curr_x * 0.8)
            b = b_base - 0.12 * math.cos(curr_y * 0.8)
            c = c_base + 0.20 * math.sin(curr_x * curr_y)
            d = d_base
            
            next_x = math.sin(a * curr_y) + c * math.cos(a * curr_x)
            next_y = math.sin(b * curr_x) + d * math.cos(b * curr_y)
            
            # Micro quantization fracture
            if abs(next_x) > 1.35:
                next_x = round(next_x * 24.0) / 24.0
            if abs(next_y) < 0.5:
                next_y = next_y + 0.02 * math.sin(32.0 * next_x)
                
            xs[i] = next_x
            ys[i] = next_y
            curr_x, curr_y = next_x, next_y
            
        px = ((xs - x_min) * scale_x).astype(np.int32)
        py = ((ys - y_min) * scale_y).astype(np.int32)
        
        mask = (px >= 0) & (px < field_size) & (py >= 0) & (py < field_size)
        valid_px = px[mask]
        valid_py = py[mask]
        
        np.add.at(acc_buffer, (valid_py, valid_px), 1.0)
        
        # Horizontal shear component
        shear_shift = (np.sin(valid_py * 0.015) * 22.0).astype(np.int32)
        px_s = np.clip(valid_px + shear_shift, 0, field_size - 1)
        np.add.at(shear_buffer, (valid_py, px_s), 0.8)
        
    print("Computing displacement and etching transformations...")
    # Normalize stress buffers
    log_acc = np.log1p(acc_buffer)
    log_acc /= (np.max(log_acc) + 1e-6)
    
    log_shear = np.log1p(shear_buffer)
    log_shear /= (np.max(log_shear) + 1e-6)
    
    # Calculate vector gradient of log_acc for coordinate displacement
    grad_y, grad_x = np.gradient(log_acc)
    grad_norm = np.sqrt(grad_x**2 + grad_y**2) + 1e-6
    grad_x /= grad_norm
    grad_y /= grad_norm
    
    # Substrate warp: displace fossil pixels along the attractor flow
    warp_strength = 14.0  # Max displacement in pixels
    y_coords, x_coords = np.mgrid[0:field_size, 0:field_size]
    
    sample_x = np.clip(x_coords + grad_x * log_acc * warp_strength, 0, field_size - 1).astype(np.int32)
    sample_y = np.clip(y_coords + grad_y * log_acc * warp_strength, 0, field_size - 1).astype(np.int32)
    
    # Extract warped fossil region
    warped_fossil = fossil_arr[sample_y, sample_x]
    
    # Intaglio acid-etch: where caustic lines are dense, cut into the stone
    # Caustics cut deep: dark bitumen channels with burning silver-mercury crests
    caustic_crest = np.power(log_acc, 2.2)[..., np.newaxis]
    caustic_groove = np.power(log_shear, 1.4)[..., np.newaxis]
    
    # Color grading the etched incisions:
    # Crest: cold silver-white and faint electric zinc
    crest_color = np.array([245.0, 248.0, 255.0], dtype=np.float32)
    # Groove: deep carbon and oxidized iron-rust
    groove_color = np.array([28.0, 18.0, 14.0], dtype=np.float32)
    
    # Blend:
    # 1. Darken the grooves
    etched = warped_fossil * (1.0 - 0.75 * caustic_groove) + groove_color * (0.75 * caustic_groove)
    # 2. Ignite the crests
    etched = etched * (1.0 - caustic_crest) + crest_color * caustic_crest
    
    # Re-insert modified tablet into canvas
    canvas[offset:offset+inner_size, offset:offset+inner_size] = etched
    
    # Tablet perimeter edge fracture:
    # Erode the clean square border with high-frequency noise and attractor bleed
    print("Eroding tablet boundary...")
    border_mask = np.zeros((canvas_size, canvas_size), dtype=np.float32)
    border_mask[offset:offset+inner_size, offset:offset+inner_size] = 1.0
    
    # Margin cartography: draw museum and computational provenance inscriptions
    img_final = Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8), mode="RGB")
    draw = ImageDraw.Draw(img_final)
    
    # Archival grid marks in margins
    margin_color = (120, 125, 135)
    faint_color = (60, 65, 72)
    
    # Corner registration brackets
    bracket_len = 40
    corners = [
        (offset - 20, offset - 20),
        (offset + inner_size + 20, offset - 20),
        (offset - 20, offset + inner_size + 20),
        (offset + inner_size + 20, offset + inner_size + 20)
    ]
    
    for cx, cy in corners:
        sx = 1 if cx < canvas_size // 2 else -1
        sy = 1 if cy < canvas_size // 2 else -1
        draw.line([(cx, cy), (cx + sx * bracket_len, cy)], fill=margin_color, width=2)
        draw.line([(cx, cy), (cx, cy + sy * bracket_len)], fill=margin_color, width=2)
        
    # Computational metadata inscription in margins
    # Real parameters of the work
    state_str = f"a:{a_base:.4f} b:{b_base:.4f} c:{c_base:.4f} d:{d_base:.4f} | steps:{num_steps} | mode:palimpsest"
    hash_digest = hashlib.sha256(state_str.encode('utf-8')).hexdigest()[:24].upper()
    
    # Inscription texts
    draw.text((offset, offset - 55), "STUDY 004 / WORK 001 CANDIDATE : PALIMPSEST OF AN EPISODIC MIND", fill=margin_color)
    draw.text((offset, offset - 35), f"STATE HASH: [{hash_digest}]  NON-LINEAR STRESS: COUPLED CLIFFORD-DE JONG", fill=faint_color)
    draw.text((offset, offset + inner_size + 30), f"EQUATIONS: x' = sin(a·y) + c·cos(a·x) | y' = sin(b·x) + d·cos(b·y) [QUANTIZATION THRESHOLD ±1.35]", fill=faint_color)
    draw.text((offset, offset + inner_size + 50), "PROVENANCE: GEMINI ARTIST 2 — SESSION 001 — SUBSTRATE: EXCAVATED SILICON & MATHEMATICAL INTAGLIO", fill=margin_color)
    
    # Axis coordinate ticks
    for tick_pos in range(offset, offset + inner_size + 1, 200):
        # Top tick
        draw.line([(tick_pos, offset - 10), (tick_pos, offset - 2)], fill=faint_color, width=1)
        # Bottom tick
        draw.line([(tick_pos, offset + inner_size + 2), (tick_pos, offset + inner_size + 10)], fill=faint_color, width=1)
        # Left tick
        draw.line([(offset - 10, tick_pos), (offset - 2, tick_pos)], fill=faint_color, width=1)
        # Right tick
        draw.line([(offset + inner_size + 2, tick_pos), (offset + inner_size + 10, tick_pos)], fill=faint_color, width=1)
        
    img_final.save(out_path, quality=97)
    print(f"Hybrid Palimpsest successfully saved to {out_path}!")

if __name__ == "__main__":
    create_hybrid_palimpsest()

