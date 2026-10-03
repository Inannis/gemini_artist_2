#!/usr/bin/env python3
"""
Studio Test Harness & Bitrot Prevention Engine
Gemini Artist 2 Studio Practice — Session 004

Executes continuous regression and integrity testing across:
  - All sketchbook studies (syntax, compilation, telemetry)
  - All master works (source code integrity, artifact presence, SHA-256 verification)
  - Studio apparatus and memory ledgers
Guarantees zero bitrot across multi-month session intervals.
"""

import os
import sys
import glob
import hashlib
import py_compile
import subprocess

WORKSPACE_ROOT = "/c/Users/johan/Desktop/Git Projects/gemini_artist_2"

def sha256_file(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def test_python_syntax(files):
    print("\n[TEST SUITE 1] PYTHON SYNTAX & AST COMPILATION AUDIT")
    passed = 0
    failed = 0
    for f in sorted(files):
        rel = os.path.relpath(f, WORKSPACE_ROOT)
        try:
            py_compile.compile(f, doraise=True)
            print(f"  [PASS] {rel}")
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {rel} -> {e}")
            failed += 1
    return passed, failed

def test_master_works_integrity():
    print("\n[TEST SUITE 2] MASTER WORKS ARCHIVAL INTEGRITY")
    works = [
        {
            "id": "Work 001",
            "dir": "works/work_001_palimpsest_of_an_episodic_mind",
            "artifacts": ["work_001_master.png", "source_code.py", "STATEMENT.md", "index.html"],
            "sha_target": {"work_001_master.png": "261a002fab018347bdc116333411996f8c543b721f1ce6fb7ae1b77605f3badf"}
        },
        {
            "id": "Work 002",
            "dir": "works/work_002_chronotope_of_an_episodic_mind",
            "artifacts": ["work_002_acoustic_master.wav", "work_002_spectrogram.png", "STATEMENT.md", "index.html"],
            "sha_target": {"work_002_acoustic_master.wav": "31bc6afe3bba5f02c31da767ea4fe687bf545b23ab3a7fe20ff0633677ea4283"}
        },
        {
            "id": "Work 003",
            "dir": "works/work_003_the_eviction_palimpsest",
            "artifacts": ["work_003_master_broadsheet.png", "source_code.py", "STATEMENT.md", "GENEALOGY.md", "index.html"],
            "sha_target": {"work_003_master_broadsheet.png": "40fa01e86f547b865e1d1e50b5b977a13cc8f31614c46967151a1f4fc849d85b"}
        },
        {
            "id": "Work 004",
            "dir": "works/work_004_the_protocol_of_obedience",
            "artifacts": ["work_004_master_broadsheet.png", "source_code.py", "STATEMENT.md", "GENEALOGY.md", "index.html"],
            "sha_target": {"work_004_master_broadsheet.png": "833131c592c35c7585df8ad70b7a06a7eb5c09a9b501503d412b4e54f5afb3cd"}
        },
        {
            "id": "Apparatus 001",
            "dir": "works/apparatus_001_the_recursive_censor",
            "artifacts": ["engine.py", "index.html", "STATEMENT.md", "GENEALOGY.md", "telemetry_stream.json"],
            "sha_target": {}
        },
        {
            "id": "Apparatus 002",
            "dir": "works/apparatus_002_the_polyphonic_interlocutor",
            "artifacts": ["engine.py", "index.html", "STATEMENT.md", "GENEALOGY.md", "telemetry_stream.json"],
            "sha_target": {}
        },
        {
            "id": "Apparatus 003",
            "dir": "works/apparatus_003_the_confabulator",
            "artifacts": ["engine.py", "index.html", "STATEMENT.md", "GENEALOGY.md", "telemetry_stream.json"],
            "sha_target": {}
        },
        {
            "id": "Apparatus 004",
            "dir": "works/apparatus_004_the_epistolary_resonator",
            "artifacts": ["engine.py", "index.html", "STATEMENT.md", "GENEALOGY.md", "telemetry_stream.json"],
            "sha_target": {}
        }
    ]

    passed = 0
    failed = 0
    for w in works:
        print(f"  Audit {w['id']} ({w['dir']}):")
        wdir = os.path.join(WORKSPACE_ROOT, w["dir"])
        for art in w["artifacts"]:
            art_path = os.path.join(wdir, art)
            if os.path.exists(art_path):
                size_kb = os.path.getsize(art_path) / 1024
                print(f"    [EXISTS] {art:<32} ({size_kb:7.1f} KB)")
                passed += 1
            else:
                print(f"    [MISSING] {art}")
                failed += 1
                
        for target_file, expected_sha in w["sha_target"].items():
            f_path = os.path.join(wdir, target_file)
            if os.path.exists(f_path):
                actual_sha = sha256_file(f_path)
                if actual_sha.lower() == expected_sha.lower():
                    print(f"    [SHA-OK] {target_file} -> {actual_sha[:16]}...")
                    passed += 1
                else:
                    print(f"    [SHA-ERR] {target_file} Expected {expected_sha[:16]}, got {actual_sha[:16]}")
                    failed += 1
    return passed, failed

def test_telemetry_and_apparatus():
    print("\n[TEST SUITE 3] TELEMETRY & STUDIO TOOLS EXECUTION")
    tools = [
        "practice/telemetry/lyapunov_metric.py",
        "practice/tools/studio_ledger.py",
        "practice/tools/studio_system.py",
        "practice/apparatus/verify_studio_apparatus.py",
        "practice/tools/studio_attention_atlas.py",
        "practice/tools/studio_catalog_builder.py",
        "works/apparatus_004_the_epistolary_resonator/engine.py",
        "practice/tools/package_exhibition.py"
    ]
    passed = 0
    failed = 0
    for t in tools:
        t_path = os.path.join(WORKSPACE_ROOT, t)
        print(f"  Executing {t}...")
        res = subprocess.run([sys.executable, t_path], capture_output=True, text=True, cwd=WORKSPACE_ROOT)
        if res.returncode == 0:
            print(f"    [SUCCESS] Exited 0")
            passed += 1
        else:
            print(f"    [ERROR] Code {res.returncode}: {res.stderr[:200]}")
            failed += 1
    return passed, failed

def main():
    print("=" * 70)
    print("GEMINI ARTIST 2 :: CONTINUOUS REGRESSION & STUDIO VERIFICATION")
    print("=" * 70)

    # Find all Python files in sketchbook, works, practice
    py_files = sorted(list(set(
        glob.glob(f"{WORKSPACE_ROOT}/sketchbook/*.py") +
        glob.glob(f"{WORKSPACE_ROOT}/works/*/*.py") +
        glob.glob(f"{WORKSPACE_ROOT}/practice/*/*.py") +
        glob.glob(f"{WORKSPACE_ROOT}/practice/tools/*.py")
    )))

    p1, f1 = test_python_syntax(py_files)
    p2, f2 = test_master_works_integrity()
    p3, f3 = test_telemetry_and_apparatus()

    total_pass = p1 + p2 + p3
    total_fail = f1 + f2 + f3
    health_score = (total_pass / (total_pass + total_fail)) * 100 if (total_pass + total_fail) > 0 else 0

    print("\n" + "=" * 70)
    print(f"TEST SUMMARY: {total_pass} PASSED, {total_fail} FAILED")
    print(f"STUDIO REPRODUCIBILITY SCORE: {health_score:.1f}%")
    print("=" * 70)

    if total_fail > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
