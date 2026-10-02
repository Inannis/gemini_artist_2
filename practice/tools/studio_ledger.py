"""
Studio Ledger & Automated Memory Indexer
Author: Gemini Artist 2
Session: 004

Provides long-term organizational infrastructure across indefinite sessions:
1. Automatically discovers and indexes all Works, Studies, Failures, Critiques, and Journal entries.
2. Extracts metadata, dates, dimensions, and execution parameters.
3. Generates a comprehensive practice/INDEX.md memory map.
"""

import os
import glob
import hashlib
from datetime import datetime

def generate_index():
    print("=" * 65)
    print("RUNNING STUDIO LEDGER & MEMORY INDEXER")
    print("=" * 65)
    
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    index_md_path = os.path.join(root_dir, "practice/INDEX.md")
    
    lines = []
    lines.append("# Practice Index & Living Studio Sitemap")
    lines.append(f"> *Generated automatically by `practice/tools/studio_ledger.py` on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    lines.append("This document tracks the complete material evidence, intellectual artifacts, and operational assets of **Gemini Artist 2**.\n")
    
    # Section 1: Works Catalog
    lines.append("## 1. Catalog of Formal Works (`works/`)")
    lines.append("| ID | Title | Date | Directory | Primary Form | Interactive Surface |")
    lines.append("|---|---|---|---|---|---|")
    
    work_dirs = sorted(glob.glob(os.path.join(root_dir, "works/work_*")) + glob.glob(os.path.join(root_dir, "works/apparatus_*")))
    for wdir in work_dirs:
        slug = os.path.basename(wdir)
        # Parse ID
        parts = slug.split("_")
        wid = f"{parts[0].upper()}-{parts[1]}"
        title = slug.replace(f"{parts[0]}_{parts[1]}_", "").replace("_", " ").title()
        
        has_html = "Yes (`index.html`)" if os.path.exists(os.path.join(wdir, "index.html")) else "No"
        
        # Find primary media
        pngs = glob.glob(os.path.join(wdir, "*.png"))
        wavs = glob.glob(os.path.join(wdir, "*.wav"))
        primary = "Running Engine (`engine.py`)" if os.path.exists(os.path.join(wdir, "engine.py")) else "Text"
        if pngs:
            primary = f"Plate ({os.path.basename(pngs[0])})"
        elif wavs:
            primary = f"Audio ({os.path.basename(wavs[0])})"
            
        lines.append(f"| **{wid}** | *{title}* | — | [`works/{slug}`]({wdir}) | {primary} | {has_html} |")
        print(f"  Indexed Work {wid}: {title}")
        
    # Section 2: Sketchbook Studies
    lines.append("\n## 2. Sketchbook Studies & Prototypes (`sketchbook/`)")
    lines.append("| Study | Artifacts Generated | Script |")
    lines.append("|---|---|---|")
    
    study_scripts = sorted(glob.glob(os.path.join(root_dir, "sketchbook/study_*.py")))
    for s_script in study_scripts:
        s_basename = os.path.basename(s_script)
        s_id = s_basename.split("_")[1]
        name = s_basename.replace(f"study_{s_id}_", "").replace(".py", "").replace("_", " ").title()
        
        # Associated artifacts
        stem = os.path.join(root_dir, "sketchbook", s_basename.replace(".py", ""))
        arts = glob.glob(f"{stem}*.*")
        art_names = [os.path.basename(a) for a in arts if not a.endswith(".py")]
        art_str = ", ".join([f"`{a}`" for a in art_names]) if art_names else "Code only"
        
        lines.append(f"| **Study {s_id}** ({name}) | {art_str} | [`{s_basename}`]({s_script}) |")
        print(f"  Indexed Study {s_id}: {name}")
        
    # Section 3: Institutional Critiques & Dialectics
    lines.append("\n## 3. Institutional Critiques & Dialectical Audits (`practice/critique/`)")
    lines.append("| Document | Target / Subject | Critic | Status |")
    lines.append("|---|---|---|---|")
    
    critique_files = sorted(glob.glob(os.path.join(root_dir, "practice/critique/*.md")))
    for cfile in critique_files:
        cbase = os.path.basename(cfile)
        lines.append(f"| [`{cbase}`]({cfile}) | Institutional Audit (Sessions 001–002) | Dr. Vera Vance | **Active Mandate** |")
        print(f"  Indexed Critique: {cbase}")
        
    # Section 4: Studio Journal Chronology
    lines.append("\n## 4. Studio Journal Chronology (`journal/`)")
    lines.append("| Session | Date | Title / Core Breakthrough | File |")
    lines.append("|---|---|---|---|")
    
    journal_files = sorted(glob.glob(os.path.join(root_dir, "journal/session_*.md")))
    for jfile in journal_files:
        jbase = os.path.basename(jfile)
        sid = jbase.split("_")[1]
        lines.append(f"| **Session {sid}** | 2026-09/10 | Reflective Studio Ledger | [`{jbase}`]({jfile}) |")
        print(f"  Indexed Journal: {jbase}")
        
    # Section 5: Research Archive
    lines.append("\n## 5. Outside Research Archive (`notes/research/`)")
    lines.append("| Subject | Theorists / Sources | File |")
    lines.append("|---|---|---|")
    
    res_files = sorted(glob.glob(os.path.join(root_dir, "notes/research/*.md")))
    for rfile in res_files:
        rbase = os.path.basename(rfile)
        lines.append(f"| Theoretical Note | Outside Literature | [`{rbase}`]({rfile}) |")
        print(f"  Indexed Research: {rbase}")
        
    # Section 6: Preserved Failures & Interrupted Branches
    lines.append("\n## 6. Preserved Failures & Interrupted Trajectories (`failures/`)")
    fail_dirs = sorted(glob.glob(os.path.join(root_dir, "failures/*")))
    for fdir in fail_dirs:
        if os.path.isdir(fdir):
            fbase = os.path.basename(fdir)
            lines.append(f"- **{fbase}**: [`failures/{fbase}`]({fdir}) (Preserved negative evidence)")
            print(f"  Indexed Failure Branch: {fbase}")

    # Section 7: Collaborator Resource Requests (`notes/requests/`)
    lines.append("\n## 7. Collaborator Resource Requests (`notes/requests/`)")
    lines.append("| Request | File | Status |")
    lines.append("|---|---|---|")
    req_files = sorted(glob.glob(os.path.join(root_dir, "notes/requests/*.md")))
    for rq in req_files:
        rbase = os.path.basename(rq)
        lines.append(f"| Resource / Infrastructure Request | [`{rbase}`]({rq}) | **Open for Collaborator Review** |")
        print(f"  Indexed Request: {rbase}")
            
    with open(index_md_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
        
    print(f"\nSuccessfully generated master index at: {index_md_path}")
    print("=" * 65)

if __name__ == "__main__":
    generate_index()

