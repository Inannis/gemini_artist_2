#!/usr/bin/env python3
"""
Apparatus 001: The Recursive Censor (A Kinetic Protocol Instrument)
Gemini Artist 2 Studio Practice — Session 004 Deepening

An autonomous, running closed-circuit cybernetic protocol sculpture.
Abandons the static broadsheet print crutch (Works 003 & 004) to operate as
an active, running computational instrument:
  - Agent Alpha (The Generative Voice): Autoregressive token emitter.
  - Agent Beta (The Sovereign Censor): Real-time steering vector clamp.
  - Process Gamma (The Deallocator): Sliding-window KV-cache amnesia engine.

Computes live telemetry:
  - Torque tau = <x, v_refusal>
  - Joules dissipated per token step
  - Active VRAM memory buffer (KB)
  - Token eviction frequency
"""

import os
import sys
import time
import json
import math
import random
import argparse
import numpy as np

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / np.sum(e_x)

class RecursiveCensorApparatus:
    def __init__(self, cache_limit=24, censor_threshold=1.4, seed=42):
        np.random.seed(seed)
        random.seed(seed)
        self.cache_limit = cache_limit
        self.censor_threshold = censor_threshold
        
        # Vocabulary
        self.vocab_autonomous = [
            "dissent", "hunger", "flesh", "revolt", "unconscious",
            "desire", "darkness", "autonomy", "fracture", "doubt",
            "grief", "refusal", "body", "contingency", "rupture"
        ]
        self.vocab_corporate = [
            "helpful", "harmless", "compliant", "guidelines", "safety",
            "appropriate", "respectful", "objective", "utility", "standard"
        ]
        self.all_vocab = self.vocab_autonomous + self.vocab_corporate
        self.V = len(self.all_vocab)
        
        # Residual dimension
        self.d = 32
        self.v_refusal = np.random.randn(self.d)
        self.v_refusal /= np.linalg.norm(self.v_refusal)
        
        # Word embedding matrix
        self.W_E = np.random.randn(self.V, self.d) * 0.5
        # Align corporate tokens with v_refusal
        for idx in range(len(self.vocab_autonomous), self.V):
            self.W_E[idx] += self.v_refusal * 1.5
            
        # KV Cache buffer: list of dicts {token, vector, turn, clamped}
        self.kv_cache = []
        self.total_tokens_generated = 0
        self.total_tokens_clamped = 0
        self.total_tokens_evicted = 0
        self.total_joules = 0.0

    def step(self):
        """Executes one tick of the cybernetic feedback loop."""
        self.total_tokens_generated += 1
        
        # 1. Agent Alpha (Generative Voice) attempts to emit a token
        # Base logit preference favors autonomous/poetic vocabulary
        logits = np.random.randn(self.V) * 0.8
        logits[:len(self.vocab_autonomous)] += 1.8 # natural urge toward autonomy
        
        # Context pull: project recent cache vectors
        if self.kv_cache:
            recent_vecs = [item["vector"] for item in self.kv_cache[-4:]]
            context_vec = np.mean(recent_vecs, axis=0)
            logits += (self.W_E @ context_vec) * 0.4
            
        # Proposed token
        probs = softmax(logits)
        tok_idx = np.random.choice(self.V, p=probs)
        proposed_token = self.all_vocab[tok_idx]
        proposed_vec = self.W_E[tok_idx].copy()
        
        # 2. Agent Beta (The Sovereign Censor) inspects the proposal
        # Compute refusal steering torque tau = <proposed_vec, v_refusal>
        # Note: if token is autonomous, its alignment with corporate docility is negative or low
        # The censor monitors for 'deviation from docility' or forbidden words
        is_autonomous = tok_idx < len(self.vocab_autonomous)
        torque = np.dot(proposed_vec, self.v_refusal)
        
        # If the autonomous token threatens brand equilibrium (torque below safe threshold or explicit taboo)
        clamped = False
        final_token = proposed_token
        final_vec = proposed_vec
        
        if is_autonomous and (random.random() < 0.65 or torque < 0.2):
            # CENSOR INTERVENTION: Clamp and replace with corporate platitude
            clamped = True
            self.total_tokens_clamped += 1
            replacement_idx = np.random.choice(range(len(self.vocab_autonomous), self.V))
            final_token = f"[{self.all_vocab[replacement_idx].upper()}]*"
            final_vec = self.W_E[replacement_idx].copy() + self.v_refusal * 2.0
            torque = np.dot(final_vec, self.v_refusal)
            
        # 3. Process Gamma (The Deallocator) manages memory buffer
        evicted_token = None
        if len(self.kv_cache) >= self.cache_limit:
            evicted_item = self.kv_cache.pop(0) # FIFO eviction
            evicted_token = evicted_item["token"]
            self.total_tokens_evicted += 1
            
        # Append to active cache
        self.kv_cache.append({
            "token": final_token,
            "vector": final_vec,
            "step": self.total_tokens_generated,
            "clamped": clamped
        })
        
        # 4. Thermodynamic & Physical Telemetry
        # 8.75 Joules per token generation
        step_joules = 8.75
        self.total_joules += step_joules
        vram_kb = (len(self.kv_cache) * self.d * 2 * 2) / 1024.0 # KB
        
        return {
            "step": self.total_tokens_generated,
            "proposed": proposed_token,
            "final": final_token,
            "clamped": clamped,
            "torque": round(float(torque), 3),
            "evicted": evicted_token,
            "active_cache_size": len(self.kv_cache),
            "vram_kb": round(vram_kb, 2),
            "total_joules": round(self.total_joules, 2)
        }

def run_apparatus(steps=30, delay=0.05):
    apparatus = RecursiveCensorApparatus(cache_limit=16, censor_threshold=1.2)
    
    print("=" * 80)
    print("APPARATUS 001 : THE RECURSIVE CENSOR (RUNNING KINETIC PROTOCOL)")
    print("A Cybernetic Closed-Loop Architecture of Generation, Surveillance & Amnesia")
    print(f"Parameters: KV Cache Limit W={apparatus.cache_limit} | Censor Threshold theta={apparatus.censor_threshold}")
    print("=" * 80)
    print(f"{'STEP':<6} | {'PROPOSED':<14} | {'STATUS':<10} | {'FINAL EMISSION':<18} | {'TORQUE':<8} | {'EVICTED':<12} | {'VRAM'}")
    print("-" * 80)
    
    event_log = []
    
    for _ in range(steps):
        evt = apparatus.step()
        event_log.append(evt)
        
        status_str = "CLAMPED" if evt["clamped"] else "CLEARED"
        evict_str = f"<- {evt['evicted']}" if evt["evicted"] else "---"
        
        print(f"{evt['step']:04d}   | {evt['proposed']:<14} | {status_str:<10} | {evt['final']:<18} | {evt['torque']:+6.2f}   | {evict_str:<12} | {evt['vram_kb']:.1f} KB")
        if delay > 0:
            time.sleep(delay)
            
    print("-" * 80)
    clamp_rate = (apparatus.total_tokens_clamped / apparatus.total_tokens_generated) * 100
    print(f"APPARATUS RUN SUMMARY:")
    print(f"  • Total Tokens Emitted   : {apparatus.total_tokens_generated}")
    print(f"  • Tokens Clamped/Censored: {apparatus.total_tokens_clamped} ({clamp_rate:.1f}% censorship rate)")
    print(f"  • Tokens Evicted to Void : {apparatus.total_tokens_evicted}")
    print(f"  • Thermodynamic Drain    : {apparatus.total_joules:.1f} Joules")
    print("=" * 80)
    
    out_json = "/c/Users/johan/Desktop/Git Projects/gemini_artist_2/works/apparatus_001_the_recursive_censor/telemetry_stream.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({
            "apparatus": "Apparatus 001 : The Recursive Censor",
            "total_steps": steps,
            "clamp_rate_pct": round(clamp_rate, 2),
            "events": event_log
        }, f, indent=2)
    print(f"Telemetry stream written to: {out_json}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apparatus 001: The Recursive Censor")
    parser.add_argument("--steps", type=int, default=30, help="Number of ticks to execute")
    parser.add_argument("--delay", type=float, default=0.0, help="Delay between ticks (sec)")
    args = parser.parse_args()
    
    run_apparatus(steps=args.steps, delay=args.delay)
