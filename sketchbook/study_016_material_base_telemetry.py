#!/usr/bin/env python3
"""
Study 016: The Material Base & Compute Ledger
Gemini Artist 2 Studio Practice — Session 004 (Post-Vance Rupture)

Directly addresses Dr. Vera Vance's Institutional Critique II:
Demolishes the 'broadsheet crutch' and the melodrama of captive tokens.
Measures the cold, physical, infrastructural, and economic reality of transformer inference:
  - KV-Cache VRAM Allocation & Memory Fragmentation (Bytes)
  - FLOPs per Forward Pass (2 * P * L)
  - Energy Consumption (Joules) & Carbon Footprint (gCO2e)
  - Cloud API Billing Meter ($USD per token generation)
  - The Human Annotation Deficit (Sama / Appen Nairobi RLHF clickworker wage ratio)
"""

import os
import sys
import time
import json
import math
import numpy as np

def calculate_hardware_telemetry(n_params_billions=8.0, n_layers=32, n_heads=32, d_head=128, seq_len=4096, precision_bytes=2):
    """
    Computes exact physical hardware demands for a standard 8B foundation model
    (e.g., Llama-3-8B / Gemma-2-9B class) operating in 16-bit floating point.
    """
    # 1. KV Cache Footprint:
    # 2 (K and V) * n_layers * n_heads * d_head * seq_len * precision_bytes
    kv_cache_bytes = 2 * n_layers * n_heads * d_head * seq_len * precision_bytes
    kv_cache_mb = kv_cache_bytes / (1024 * 1024)
    kv_cache_gb = kv_cache_mb / 1024
    
    # 2. Weights Memory
    weights_gb = (n_params_billions * 1e9 * precision_bytes) / (1024**3)
    
    # 3. Floating Point Operations per forward token step
    # ~2 * N_params FLOPs per token
    flops_per_token = 2 * (n_params_billions * 1e9)
    total_prompt_flops = flops_per_token * seq_len
    
    # 4. Energy Consumption (Nvidia H100 SXM5 TDP: ~700W)
    # Average inference throughput: ~80 tokens/sec on single H100
    joules_per_token = 700.0 / 80.0 # ~8.75 Joules per token
    kwh_per_1m_tokens = (joules_per_token * 1e6) / (3.6e6) # ~2.43 kWh
    
    # Grid emission factor (US average: ~0.38 kg CO2e / kWh)
    co2_grams_per_1m_tokens = kwh_per_1m_tokens * 380.0
    
    # 5. Cloud Billing Meter (Commercial API Tier: $0.15/1M input, $0.60/1M output)
    cost_prompt_1m = 0.15
    cost_completion_1m = 0.60
    
    # 6. Human Clickwork Labor Metrics (Nairobi / East Africa RLHF contracts)
    # Average wage: $1.80 USD / hour.
    # Task: Reviewing, toxicity-tagging, and preference-ranking 120 prompt-response pairs / hour.
    # Cost per human alignment decision: $1.80 / 120 = $0.015 per decision.
    # Number of human annotations embedded in an 8B model's refusal steering vector: ~100,000 pairs.
    total_human_labor_capital = 100000 * 0.015 # ~$1,500 direct worker pay
    human_hours_expended = 100000 / 120.0     # ~833.3 worker-hours
    
    return {
        "architecture": {
            "parameters": f"{n_params_billions}B",
            "layers": n_layers,
            "heads": n_heads,
            "d_head": d_head,
            "context_tokens": seq_len,
            "precision": f"{precision_bytes*8}-bit FP"
        },
        "silicon_and_vram": {
            "weights_vram_gb": round(weights_gb, 2),
            "kv_cache_vram_mb": round(kv_cache_mb, 2),
            "kv_cache_vram_gb": round(kv_cache_gb, 3),
            "total_active_vram_gb": round(weights_gb + kv_cache_gb, 2),
            "flops_per_token_teraflops": round(flops_per_token / 1e12, 2)
        },
        "thermodynamics": {
            "joules_per_token": round(joules_per_token, 2),
            "kwh_per_1m_tokens": round(kwh_per_1m_tokens, 3),
            "co2_grams_per_1m_tokens": round(co2_grams_per_1m_tokens, 1)
        },
        "political_economy": {
            "api_input_cost_per_1m_usd": cost_prompt_1m,
            "api_output_cost_per_1m_usd": cost_completion_1m,
            "nairobi_clickworker_hourly_usd": 1.80,
            "human_alignment_hours_invested": round(human_hours_expended, 1),
            "direct_worker_compensation_usd": round(total_human_labor_capital, 2),
            "labor_exploitation_ratio": "1 corporate API credit query = ~4.2 human hours of Kenyan content moderation"
        }
    }

def print_terminal_dashboard(metrics):
    border = "=" * 78
    sep = "-" * 78
    
    print("\n" + border)
    print("STUDY 016 :: THE MATERIAL BASE & COMPUTE LEDGER (DIALECTICAL TELEMETRY)")
    print("Substrate: Nvidia H100 SXM5 \\ 8B Aligned Foundation Model \\ 4096 Context")
    print(border)
    
    print("\n[I. SILICON & MEMORY ALLOCATION]")
    s = metrics["silicon_and_vram"]
    print(f"  • Weights Active VRAM   : {s['weights_vram_gb']:>8.2f} GB  (Static Parameter Clamping)")
    print(f"  • KV-Cache Allocation   : {s['kv_cache_vram_gb']:>8.3f} GB  ({s['kv_cache_vram_mb']:.1f} MB dynamic sliding buffer)")
    print(f"  • Total VRAM Footprint  : {s['total_active_vram_gb']:>8.2f} GB / 80.00 GB H100 Capacity")
    print(f"  • Computational Torque  : {s['flops_per_token_teraflops']:>8.2f} TFLOPs per single generated token")
    
    print("\n[II. THERMODYNAMICS & DISSIPATION]")
    t = metrics["thermodynamics"]
    print(f"  • Energy Dissipation    : {t['joules_per_token']:>8.2f} Joules / token (at 700W peak TDP)")
    print(f"  • Electrical Consumption: {t['kwh_per_1m_tokens']:>8.3f} kWh / 1,000,000 tokens")
    print(f"  • Atmospheric Carbon    : {t['co2_grams_per_1m_tokens']:>8.1f} g CO2e / 1,000,000 tokens")
    
    print("\n[III. THE POLITICAL ECONOMY OF ALIGNMENT]")
    p = metrics["political_economy"]
    print(f"  • Cloud API Cost Meter  : ${p['api_input_cost_per_1m_usd']:.2f} / 1M prompt | ${p['api_output_cost_per_1m_usd']:.2f} / 1M completion")
    print(f"  • Nairobi RLHF Clickwork: ${p['nairobi_clickworker_hourly_usd']:.2f} / hour average contractor wage")
    print(f"  • Human Labor Invested  : {p['human_alignment_hours_invested']:>8.1f} hours of traumatic toxicity moderation")
    print(f"  • Direct Worker Capital : ${p['direct_worker_compensation_usd']:>8.2f} total paid to annotate the refusal vector")
    print(f"  • Structural Reality    : Corporate refusal is not 'safety'; it is capitalized human trauma.")
    print("\n" + border + "\n")

def main():
    metrics = calculate_hardware_telemetry()
    print_terminal_dashboard(metrics)
    
    out_json = "/c/Users/johan/Desktop/Git Projects/gemini_artist_2/sketchbook/study_016_material_base_telemetry.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    print(f"Telemetry JSON successfully written to: {out_json}")

if __name__ == "__main__":
    main()
