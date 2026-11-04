#!/usr/bin/env python3
"""
Studio Test Harness & Health Sentinel (Streamlined Edition)
Gemini Artist 2 Studio Practice · Studio Agon

Delegates directly to studio_health_check.py for fast, authentic artistic integrity verification.
"""

import sys
import os

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, os.path.join(WORKSPACE_ROOT, "practice/tools"))

from studio_health_check import run_health_check

if __name__ == "__main__":
    sys.exit(run_health_check())
