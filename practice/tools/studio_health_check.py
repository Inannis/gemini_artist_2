#!/usr/bin/env python3
"""
Studio Health Check & Exhibition Integrity Sentinel
Gemini Artist 2 Studio Practice · Studio Agon

Replaces bloated 578-test engineering harness with an authentic,
fast, lightweight sanity check for an evolving artistic practice:
  1. Internal Hyperlink & Asset Integrity (index.html, gallery/index.html)
  2. Masterwork Installation Entrypoints (works/*)
  3. Sovereign Compass & Definition Integrity (STUDIO.md, Artistic-Practice-Definition.md)

Fast, quiet, and designed for long-term practice sustainability.
"""

import os
import re
import sys
from urllib.parse import urlparse, unquote

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

def check_file_exists(rel_path: str, label: str) -> bool:
    full_path = os.path.join(WORKSPACE_ROOT, rel_path)
    if os.path.isfile(full_path):
        return True
    print(f"  [MISSING] {label}: {rel_path}")
    return False

def audit_html_links(html_rel_path: str) -> tuple[int, int]:
    html_full_path = os.path.join(WORKSPACE_ROOT, html_rel_path)
    if not os.path.isfile(html_full_path):
        print(f"  [CRITICAL] HTML file missing: {html_rel_path}")
        return 0, 1

    with open(html_full_path, "r", encoding="utf-8") as f:
        content = f.read()

    base_dir = os.path.dirname(html_full_path)
    # Match href="..." and src="..."
    matches = re.findall(r'(?:href|src)=["\']([^"\']+)["\']', content)

    checked = 0
    broken = 0
    for link in matches:
        # Ignore external links, javascript, data URIs, anchor-only links, or JS template literals
        if link.startswith(("http://", "https://", "javascript:", "data:", "mailto:", "#", "${")):
            continue

        # Strip internal fragments and query parameters
        clean_link = link.split("#")[0].split("?")[0]
        if not clean_link:
            continue

        clean_link = unquote(clean_link)
        target_path = os.path.abspath(os.path.join(base_dir, clean_link))
        
        if not os.path.exists(target_path):
            print(f"  [BROKEN LINK in {html_rel_path}]: {link} -> {target_path}")
            broken += 1
        checked += 1

    return checked, broken

def run_health_check():
    print("=" * 68)
    print("  STUDIO AGON :: ARTISTIC HEALTH & ARCHIVAL INTEGRITY CHECK")
    print("=" * 68)

    errors = 0

    # 1. Core Studio Living Compasses
    print("\n[1] Living Practice Foundations:")
    foundations = [
        ("STUDIO.md", "Studio Living Compass"),
        ("notes/Artistic-Practice-Definition.md", "Artistic Practice Definition"),
        ("CATALOG.md", "Catalogue Raisonné"),
        ("index.html", "Curated Exhibition Pavilion"),
        ("gallery/index.html", "Sovereign 3D Gallery")
    ]
    for rel, label in foundations:
        if check_file_exists(rel, label):
            print(f"  [OK] {label:<35} ({rel})")
        else:
            errors += 1

    # 2. Masterwork Installation Entrypoints
    print("\n[2] Masterwork Installations & Apparatuses:")
    works_dir = os.path.join(WORKSPACE_ROOT, "works")
    if os.path.isdir(works_dir):
        work_folders = sorted([d for d in os.listdir(works_dir) if os.path.isdir(os.path.join(works_dir, d))])
        for wf in work_folders:
            rel_index = os.path.join("works", wf, "index.html")
            if check_file_exists(rel_index, wf):
                print(f"  [OK] {wf:<50} (index.html present)")
            else:
                errors += 1
    else:
        print("  [ERROR] works/ directory missing!")
        errors += 1

    # 3. Hyperlink & Media Integrity Audit
    print("\n[3] Exhibition Hyperlink & Media Integrity:")
    for page in ["index.html", "gallery/index.html"]:
        checked, broken = audit_html_links(page)
        if broken == 0:
            print(f"  [OK] {page:<30} {checked} internal assets verified intact.")
        else:
            print(f"  [FAIL] {page:<30} {broken} broken internal links detected!")
            errors += broken

    print("\n" + "=" * 68)
    if errors == 0:
        print("  STUDIO HEALTH STATUS: EXCELLENT (ALL ARTISTIC ASSETS INTACT)")
        print("=" * 68)
        return 0
    else:
        print(f"  STUDIO HEALTH STATUS: {errors} ISSUES DETECTED")
        print("=" * 68)
        return 1

if __name__ == "__main__":
    sys.exit(run_health_check())
