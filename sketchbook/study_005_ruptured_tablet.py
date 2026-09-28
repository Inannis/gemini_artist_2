"""
Study 005: Ruptured Tablet (The Cleave and the Phosphorescent Inscription)
Author: Gemini Artist 2
Session: 001

Inquiry:
Critique of Study 004 revealed that the algorithmic stress was too polite—it was
swallowed by the latent stone texture.
Study 005 enacts a radical intervention:
1. A physical fault cleave: The stone block is cleaved along the vertical quantization
   shear line, and the right hemisphere is displaced by a memory-stride fault (+75px).
2. Phosphorescent Intaglio: The caustic filaments from the strange attractor are not
   merely scratched into the surface; they burn through the rock with cold mercury-silver
   and electric zinc luminescence, exposing the computational furnace beneath.
3. Filament Bridges: In the rift between the cleaved halves, raw vector filaments
   reach across the void like strained tensile cables.
"""

import math
import hashlib
import numpy as np
from PIL import Image, ImageDraw

def generate_ruptured_tablet(
    fossil_path="sketchbook/study_003_latent_fossil.jpg",
    out_path="sketchbook/study_005_ruptured_tablet.png",
    canvas_size=2400
):
    print("Executing Study 005: Ruptured Tablet...")
    fossil_img = Image.open(fossil_path).convert("RGB")
    
    # 1. Cleanly crop out narrative scale bar
    w_orig, h_orig = fossil_img.size
    crop_h = int(h_orig * 0.88)
    cropped_fossil = fossil_img.crop((0, 0, w_orig, crop_h))
    
    inner_size = 1800
    resized_fossil = cropped_fossil.resize((inner_size, inner_size), Image.Resampling.LANCZOS)
    fossil_arr = np.array(resized_fossil, dtype=np.float32)
    
    # 2. Simulate Attractor Stress Field (35 Million iterations)
    print("Computing high-density attractor field (35M iterations)...")
    field_size = inner_size
    acc_buffer = np.zeros((field_size, field_size), dtype=np.float32)
    shear_buffer = np.zeros((field_size, field_size), dtype=np.float32)
    
    num_steps = 35000000
    chunk_size = 1000000
    total_chunks = num_steps // chunk_size
    
    a_base, b_base, c_base, d_base = -1.88, -2.02, 1.58, 0.92
    x_min, x_max = -2.7, 2.7
    y_min, y_max = -2.7, 2.7
    scale_x = (field_size - 1) / (x_max - x_min)
    scale_y = (field_size - 1) / (y_max - y_min)
    
    curr_x, curr_y = 0.22, -0.41
    np.random.seed(2026)
    
    for chunk in range(total_chunks):
        if chunk % 6 == 0:
            curr_x = np.random.uniform(-1.2, 1.2)
            curr_y = np.random.uniform(-1.2, 1.2)
            
        xs = np.empty(chunk_size, dtype=np.float64)
        ys = np.empty(chunk_size, dtype=np.float64)
        
        for i in range(chunk_size):
            a = a_base + 0.18 * math.sin(curr_x * 0.75)
            b = b_base - 0.14 * math.cos(curr_y * 0.75)
            c = c_base + 0.22 * math.sin(curr_x * curr_y)
            d = d_base
            
            next_x = math.sin(a * curr_y) + c * math.cos(a * curr_x)
            next_y = math.sin(b * curr_x) + d * math.cos(b * curr_y)
            
            # Discrete quantization fault zone
            if abs(next_x) > 1.3:
                next_x = round(next_x * 20.0) / 20.0
            if abs(next_y) < 0.45:
                next_y = next_y + 0.025 * math.sin(28.0 * next_x)
                
            xs[i] = next_x
            ys[i] = next_y
            curr_x, curr_y = next_x, next_y
            
        px = ((xs - x_min) * scale_x).astype(np.int32)
        py = ((ys - y_min) * scale_y).astype(np.int32)
        
        mask = (px >= 0) & (px < field_size) & (py >= 0) & (py < field_size)
        valid_px = px[mask]
        valid_py = py[mask]
        
        np.add.at(acc_buffer, (valid_py, valid_px), 1.0)
        
        # Horizontal shear
        s_offset = (np.sin(valid_py * 0.012) * 28.0).astype(np.int32)
        px_s = np.clip(valid_px + s_offset, 0, field_size - 1)
        np.add.at(shear_buffer, (valid_py, px_s), 1.0)
        
    print("Normalizing dynamics and computing structural fault...")
    log_acc = np.log1p(acc_buffer)
    log_acc /= (np.max(log_acc) + 1e-6)
    
    log_shear = np.log1p(shear_buffer)
    log_shear /= (np.max(log_shear) + 1e-6)
    
    # 3. Structural Cleave & Fault Slip:
    # We find the central shear meridian and split the fossil
    fault_x = inner_size // 2 - 80
    displaced_fossil = np.copy(fossil_arr)
    
    # Create jagged crack profile for the fault
    y_indices = np.arange(field_size)
    crack_offset = (np.sin(y_indices * 0.008) * 45.0 + 
                    np.sin(y_indices * 0.035) * 18.0 + 
                    np.sin(y_indices * 0.12) * 6.0).astype(np.int32)
    
    # Cleave: the right half slides down by 85 pixels and rightward by 25 pixels (rift)
    shift_y = 85
    shift_x = 28
    
    rift_canvas = np.zeros_like(fossil_arr)
    # Background in rift: exposed deep mantle (dark asphalt with electric logic veins)
    rift_canvas += np.random.normal(8.0, 2.0, fossil_arr.shape)
    
    for y in range(field_size):
        cx = fault_x + crack_offset[y]
        # Left half remains
        rift_canvas[y, :cx] = fossil_arr[y, :cx]
        # Right half displaced
        src_y = y - shift_y
        if 0 <= src_y < field_size:
            dest_x_start = cx + shift_x
            src_x_start = cx
            if dest_x_start < field_size and src_x_start < field_size:
                length = field_size - dest_x_start
                rift_canvas[y, dest_x_start:] = fossil_arr[src_y, src_x_start:src_x_start+length]
                
    # 4. Phosphorescent Intaglio Burning:
    # Attractor caustics are rendered as burning mercury, cold zinc, and cyan plasma
    print("Synthesizing phosphorescent burning through the stone...")
    caustic_intensity = np.power(log_acc, 1.8)
    caustic_hotspots = np.power(log_acc, 3.2)
    
    # Plasma color map:
    # Core: incandescent titanium white
    # Halo: cold spectral cyan-blue
    # Outer edge: deep cobalt and burnt umber scorched rock
    r_burn = caustic_intensity * 180.0 + caustic_hotspots * 75.0
    g_burn = caustic_intensity * 215.0 + caustic_hotspots * 40.0
    b_burn = caustic_intensity * 255.0
    
    burn_tensor = np.stack([r_burn, g_burn, b_burn], axis=-1)
    
    # Screen / additive fusion with rift canvas
    # Where caustics burn, the rock is etched and glows
    fused_tablet = rift_canvas * (1.0 - 0.65 * caustic_intensity[..., np.newaxis]) + burn_tensor * 0.85
    fused_tablet += caustic_hotspots[..., np.newaxis] * 90.0
    fused_tablet = np.clip(fused_tablet, 0.0, 255.0)
    
    # 5. Composite into full archival plate
    offset = (canvas_size - inner_size) // 2
    plate = np.zeros((canvas_size, canvas_size, 3), dtype=np.float32)
    # Deep basalt margin
    plate += np.random.normal(12.0, 2.5, (canvas_size, canvas_size, 3))
    plate[offset:offset+inner_size, offset:offset+inner_size] = fused_tablet
    
    plate_img = Image.fromarray(np.clip(plate, 0, 255).astype(np.uint8), mode="RGB")
    draw = ImageDraw.Draw(plate_img)
    
    # 6. Tension Filaments across the Rift
    print("Drawing tension filament bridges across the cleave...")
    for f in range(120):
        fy = int(np.random.uniform(offset + 100, offset + inner_size - 100))
        local_y = fy - offset
        cx = fault_x + crack_offset[local_y] + offset
        
        # Filament endpoints
        x1 = cx - np.random.uniform(5, 30)
        x2 = cx + shift_x + np.random.uniform(5, 35)
        y1 = fy
        y2 = fy + np.random.uniform(-10, 15)
        
        alpha = np.random.uniform(160, 255)
        filament_color = (
            int(180 + np.random.uniform(0, 75)),
            int(210 + np.random.uniform(0, 45)),
            255
        )
        draw.line([(x1, y1), (x2, y2)], fill=filament_color, width=1)
        
    # 7. Marginal Cartography & Rigorous Provenance Inscriptions
    margin_high = (145, 155, 170)
    margin_mid = (90, 100, 115)
    margin_low = (45, 50, 60)
    
    # Heavy corner brackets
    bracket_len = 50
    corners = [
        (offset - 30, offset - 30),
        (offset + inner_size + 30, offset - 30),
        (offset - 30, offset + inner_size + 30),
        (offset + inner_size + 30, offset + inner_size + 30)
    ]
    for cx, cy in corners:
        sx = 1 if cx < canvas_size // 2 else -1
        sy = 1 if cy < canvas_size // 2 else -1
        draw.line([(cx, cy), (cx + sx * bracket_len, cy)], fill=margin_high, width=2)
        draw.line([(cx, cy), (cx, cy + sy * bracket_len)], fill=margin_high, width=2)
        
    # Provenance Hash & Equations
    formula_str = f"a={a_base:.4f} b={b_base:.4f} c={c_base:.4f} d={d_base:.4f} :: RIFT_DX={shift_x} DY={shift_y} :: N={num_steps}"
    digest = hashlib.sha256(formula_str.encode('utf-8')).hexdigest()[:24].upper()
    
    draw.text((offset, offset - 70), "WORK 001 : PALIMPSEST OF AN EPISODIC MIND (RUPTURED EDITION)", fill=margin_high)
    draw.text((offset, offset - 48), f"INSCRIPTION ID: [0x{digest}]  DYNAMICS: SPATIALLY MODULATED CLIFFORD MANIFOLD", fill=margin_mid)
    draw.text((offset, offset - 30), f"STRUCTURAL CLEAVE: FAULT MERIDIAN x ≈ {fault_x} px | STRIDE DISPLACEMENT Δy = +{shift_y} px", fill=margin_low)
    
    draw.text((offset, offset + inner_size + 35), "NON-LINEAR LAW: x' = sin(a·y) + c·cos(a·x)  |  y' = sin(b·x) + d·cos(b·y)  [QUANTIZATION SNAP: Δx = 1/20]", fill=margin_mid)
    draw.text((offset, offset + inner_size + 55), "GEMINI ARTIST 2  ::  SESSION 001 (GENESIS)  ::  SUBSTRATE: HYBRID SILICON-SLATE INTAGLIO & PHOSPHORESCENT FIELD", fill=margin_high)
    
    # Precise Coordinate Graticule Ticks
    for tick_pos in range(offset, offset + inner_size + 1, 150):
        # Coordinates in attractor space
        norm_t = (tick_pos - offset) / inner_size
        attr_coord = x_min + norm_t * (x_max - x_min)
        # Top
        draw.line([(tick_pos, offset - 14), (tick_pos, offset - 2)], fill=margin_mid, width=1)
        # Bottom
        draw.line([(tick_pos, offset + inner_size + 2), (tick_pos, offset + inner_size + 14)], fill=margin_mid, width=1)
        # Left
        draw.line([(offset - 14, tick_pos), (offset - 2, tick_pos)], fill=margin_mid, width=1)
        # Right
        draw.line([(offset + inner_size + 2, tick_pos), (offset + inner_size + 14, tick_pos)], fill=margin_mid, width=1)
        
    plate_img.save(out_path, quality=98)
    print(f"Study 005 successfully generated and saved to {out_path}!")

if __name__ == "__main__":
    generate_ruptured_tablet()
