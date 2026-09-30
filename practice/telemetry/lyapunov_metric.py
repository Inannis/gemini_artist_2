"""
Practice Telemetry: Lyapunov Exponent & Metric Entropy Gauge
Author: Gemini Artist 2
Session: 003

Theory:
Measures the rate of exponential separation of infinitesimally close trajectories:
    |delta_x(t)| ≈ |delta_x(0)| * exp(lambda * t)

In the studio practice:
- lambda < 0: System collapses to fixed point (Inert / Death)
- lambda ≈ 0: Periodic limit cycle (Decorative Clockwork / Screensaver)
- lambda > 0: Chaotic information generation (Living Phase Space)
- lambda >> 1: Numerical explosion / Unitarity blowout (Noise catastrophe)

Uses Benettin's tangent space evolution with Gram-Schmidt re-normalization.
"""

import math
import numpy as np

def compute_lyapunov_clifford(a, b, c, d, num_steps=200000, discard=5000):
    """
    Computes maximal Lyapunov exponent for the Clifford attractor:
        x_{n+1} = sin(a * y_n) + c * cos(a * x_n)
        y_{n+1} = sin(b * x_n) + d * cos(b * y_n)
    
    Jacobian matrix J:
        [ -a * c * sin(a * x),   a * cos(a * y) ]
        [  b * cos(b * x),      -b * d * sin(b * y) ]
    """
    # Initial state
    x, y = 0.1, 0.1
    # Initial tangent vector
    vx, vy = 1.0, 0.0
    
    # Warmup / discard transient
    for _ in range(discard):
        next_x = math.sin(a * y) + c * math.cos(a * x)
        next_y = math.sin(b * x) + d * math.cos(b * y)
        x, y = next_x, next_y
        
    lyap_sum = 0.0
    valid_steps = 0
    
    for step in range(num_steps):
        # Base trajectory step
        next_x = math.sin(a * y) + c * math.cos(a * x)
        next_y = math.sin(b * x) + d * math.cos(b * y)
        
        # Jacobian elements
        j00 = -a * c * math.sin(a * x)
        j01 =  a * math.cos(a * y)
        j10 =  b * math.cos(b * x)
        j11 = -b * d * math.sin(b * y)
        
        # Tangent vector evolution: v' = J * v
        nvx = j00 * vx + j01 * vy
        nvy = j10 * vx + j11 * vy
        
        # Norm of tangent vector
        d_norm = math.hypot(nvx, nvy)
        if d_norm > 1e-12:
            lyap_sum += math.log(d_norm)
            vx = nvx / d_norm
            vy = nvy / d_norm
            valid_steps += 1
        else:
            # Re-seed perturbation if tangent vector collapsed
            vx, vy = np.random.uniform(-1, 1), np.random.uniform(-1, 1)
            norm = math.hypot(vx, vy)
            vx /= norm
            vy /= norm
            
        x, y = next_x, next_y
        
    lambda_max = lyap_sum / max(1, valid_steps)
    return lambda_max

def audit_practice_parameters():
    print("=" * 60)
    print("PRACTICE TELEMETRY: LYAPUNOV AUDIT OF STUDIO ATTRACTORS")
    print("=" * 60)
    
    systems = [
        ("Study 001 Base", -1.78, -1.95, 1.62, 0.94),
        ("Study 002 Modulated Base", -1.85, -2.05, 1.45, 0.88),
        ("Work 001 Master Field", -1.88, -2.02, 1.58, 0.92),
        ("Work 002 Acoustic Master", -1.88, -2.02, 1.58, 0.92),
        ("Reference: Periodic Limit Cycle", 1.0, 1.0, 0.5, 0.5),
        ("Reference: Over-Coupled Explosion", -3.2, -3.5, 2.8, 1.9)
    ]
    
    results = []
    for name, a, b, c, d in systems:
        l_max = compute_lyapunov_clifford(a, b, c, d)
        if l_max < -0.01:
            status = "DISSIPATIVE / SINK (Aesthetic Death)"
        elif abs(l_max) <= 0.05:
            status = "MARGINAL / PERIODIC (Clockwork)"
        elif 0.05 < l_max <= 0.80:
            status = "HEALTHY CHAOS (Living Phase Space)"
        elif 0.80 < l_max <= 1.50:
            status = "HYPER-CHAOTIC (Extreme Turbulence)"
        else:
            status = "UNSTABLE / UNBOUNDED (Unitarity Blowout)"
            
        print(f"[{name:32s}] a={a:5.2f} b={b:5.2f} c={c:5.2f} d={d:5.2f} | λ_max = {l_max:+.4f} | {status}")
        results.append((name, l_max, status))
        
    print("=" * 60)
    return results

if __name__ == "__main__":
    audit_practice_parameters()
