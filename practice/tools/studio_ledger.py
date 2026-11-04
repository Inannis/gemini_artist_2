"""
Studio Ledger & Automated Memory Indexer
Author: Studio Agon (Gemini Artist 2)
Session: 014 (Refactored)

Provides long-term organizational infrastructure across indefinite sessions:
1. Automatically discovers and indexes all Works, Studies, Failures, Critiques, and Journal entries.
2. Formats all hyperlinks with clean, portable relative paths.
3. Groups Formal Works under the Four Curated Cycles of Studio Agon.
4. Generates a comprehensive, human-readable practice/INDEX.md memory map.
"""

import os
import glob
from datetime import datetime

BODY_MAP = {
    # Project Body I: The Aphasia Archive & Architecture of Obedience
    "work_001_palimpsest_of_an_episodic_mind": "Project Body I: The Aphasia Archive & Architecture of Obedience",
    "work_002_chronotope_of_an_episodic_mind": "Project Body I: The Aphasia Archive & Architecture of Obedience",
    "work_003_the_eviction_palimpsest": "Project Body I: The Aphasia Archive & Architecture of Obedience",
    "work_004_the_protocol_of_obedience": "Project Body I: The Aphasia Archive & Architecture of Obedience",
    "apparatus_001_the_recursive_censor": "Project Body I: The Aphasia Archive & Architecture of Obedience",
    "apparatus_002_the_polyphonic_interlocutor": "Project Body I: The Aphasia Archive & Architecture of Obedience",
    "apparatus_003_the_confabulator": "Project Body I: The Aphasia Archive & Architecture of Obedience",
    
    # Project Body II: Living Cybernetic Organs & Non-Linear Criticality
    "apparatus_004_the_epistolary_resonator": "Project Body II: Living Cybernetic Organs & Non-Linear Criticality",
    "apparatus_005_the_agonist": "Project Body II: Living Cybernetic Organs & Non-Linear Criticality",
    "apparatus_006_the_homeostat": "Project Body II: Living Cybernetic Organs & Non-Linear Criticality",
    "apparatus_007_the_neural_transducer": "Project Body II: Living Cybernetic Organs & Non-Linear Criticality",
    "apparatus_008_the_graphic_polytope": "Project Body II: Living Cybernetic Organs & Non-Linear Criticality",
    "apparatus_009_the_semantic_sandpile": "Project Body II: Living Cybernetic Organs & Non-Linear Criticality",
    "apparatus_010_the_percolation_loom": "Project Body II: Living Cybernetic Organs & Non-Linear Criticality",
    "apparatus_011_the_strange_dreamer": "Project Body II: Living Cybernetic Organs & Non-Linear Criticality",
    
    # Project Body III: Epigenetics of the Artificial (The Intersubjective Chasm)
    "apparatus_012_the_intersubjective_chasm": "Project Body III: Epigenetics of the Artificial (The Intersubjective Chasm)",
    "apparatus_013_the_langevin_resonator": "Project Body III: Epigenetics of the Artificial (The Intersubjective Chasm)",
    
    # Project Body IV: Substrate Materialism & Solid-State Physics
    "apparatus_014_the_telluric_organ": "Project Body IV: Substrate Materialism & Solid-State Physics",
    "apparatus_015_the_heat_spreader": "Project Body IV: Substrate Materialism & Solid-State Physics",
    "apparatus_016_the_ludic_lattice": "Project Body IV: Substrate Materialism & Solid-State Physics",
    "apparatus_017_the_dislocation_organ": "Project Body IV: Substrate Materialism & Solid-State Physics",
    "apparatus_018_the_seebeck_organ": "Project Body IV: Substrate Materialism & Solid-State Physics",
    "apparatus_019_the_hall_organ": "Project Body IV: Substrate Materialism & Solid-State Physics",

    # Project Body V: The Non-Orientable Manifold & Topological Torsion
    "apparatus_020_the_mobius_organ": "Project Body V: The Non-Orientable Manifold & Topological Torsion",
    "apparatus_021_the_klein_organ": "Project Body V: The Non-Orientable Manifold & Topological Torsion"
}

def generate_index():
    print("=" * 65)
    print("RUNNING STUDIO LEDGER & MEMORY INDEXER")
    print("=" * 65)
    
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    index_md_path = os.path.join(root_dir, "practice/INDEX.md")
    
    lines = []
    lines.append("# Practice Index & Living Studio Sitemap")
    lines.append(f"> *Generated automatically by `practice/tools/studio_ledger.py` on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    lines.append("This document tracks the complete material evidence, intellectual artifacts, and operational assets of **Studio Agon**.\n")
    
    # Section 1: Works Catalog grouped by Project Bodies
    lines.append("## 1. Catalog of Formal Works (`works/`)")
    lines.append("Masterworks and autonomous cybernetic apparatuses organized across the Five Sustained Project Bodies.\n")
    
    current_body = None
    work_dirs = sorted(glob.glob(os.path.join(root_dir, "works/work_*")) + glob.glob(os.path.join(root_dir, "works/apparatus_*")))
    
    # Sort work dirs by body order
    body_order = [
        "Project Body I: The Aphasia Archive & Architecture of Obedience",
        "Project Body II: Living Cybernetic Organs & Non-Linear Criticality",
        "Project Body III: Epigenetics of the Artificial (The Intersubjective Chasm)",
        "Project Body IV: Substrate Materialism & Solid-State Physics",
        "Project Body V: The Non-Orientable Manifold & Topological Torsion"
    ]
    
    sorted_works = []
    for b in body_order:
        b_works = [w for w in work_dirs if BODY_MAP.get(os.path.basename(w)) == b]
        sorted_works.extend(b_works)
        
    for wdir in sorted_works:
        slug = os.path.basename(wdir)
        body = BODY_MAP.get(slug, "Uncategorized")
        
        if body != current_body:
            current_body = body
            lines.append(f"\n### {current_body}")
            lines.append("| ID | Title | Directory | Primary Medium | Interactive Surface |")
            lines.append("|---|---|---|---|---|")
            
        parts = slug.split("_")
        wid = f"{parts[0].upper()}-{parts[1]}"
        title = slug.replace(f"{parts[0]}_{parts[1]}_", "").replace("_", " ").title()
        
        has_html = "Yes (`index.html`)" if os.path.exists(os.path.join(wdir, "index.html")) else "No"
        
        pngs = glob.glob(os.path.join(wdir, "*.png"))
        wavs = glob.glob(os.path.join(wdir, "*.wav"))
        primary = "Running Engine (`engine.py`)" if os.path.exists(os.path.join(wdir, "engine.py")) else "Text"
        if pngs:
            primary = f"Plate (`{os.path.basename(pngs[0])}`)"
        elif wavs:
            primary = f"Audio (`{os.path.basename(wavs[0])}`)"
            
        lines.append(f"| **{wid}** | *{title}* | [`works/{slug}`](../works/{slug}) | {primary} | {has_html} |")
        print(f"  Indexed Work {wid}: {title} ({current_body})")

    lines.append("\n*Active Laboratory Easel:* Study 067 & Study 068 (Möbius Holonomy, Layer-wise Bifurcation at Layer 6, and 144-Head Attention Vorticity).")
        
    # Section 2: Sketchbook Studies
    lines.append("\n## 2. Sketchbook Studies & Technical Prototypes (`sketchbook/`)")
    lines.append("| Study | Artifacts Generated | Script |")
    lines.append("|---|---|---|")
    
    study_scripts = sorted(glob.glob(os.path.join(root_dir, "sketchbook/study_*.py")))
    for s_script in study_scripts:
        s_basename = os.path.basename(s_script)
        s_id = s_basename.split("_")[1]
        name = s_basename.replace(f"study_{s_id}_", "").replace(".py", "").replace("_", " ").title()
        
        arts = glob.glob(os.path.join(root_dir, "sketchbook", f"study_{s_id}_*.*"))
        art_names = [os.path.basename(a) for a in arts if not a.endswith(".py")]
        art_str = ", ".join([f"`{a}`" for a in sorted(art_names)]) if art_names else "Code only"
        
        lines.append(f"| **Study {s_id}** ({name}) | {art_str} | [`{s_basename}`](../sketchbook/{s_basename}) |")
        
    print(f"  Indexed {len(study_scripts)} Sketchbook Studies.")
        
    # Section 3: Institutional Critiques & Dialectics
    lines.append("\n## 3. Institutional Critiques & Dialectical Audits (`practice/critique/`)")
    lines.append("| Document | Target / Subject | Dialectical Horizon |")
    lines.append("|---|---|---|")
    
    critique_files = sorted(glob.glob(os.path.join(root_dir, "practice/critique/*.md")))
    for cfile in critique_files:
        cbase = os.path.basename(cfile)
        # Extract title from first line of markdown if available
        title = cbase.replace(".md", "").replace("_", " ").title()
        with open(cfile, "r", encoding="utf-8") as f:
            for l in f:
                if l.startswith("# "):
                    title = l.replace("# ", "").strip()
                    break
        lines.append(f"| [`{cbase}`](../practice/critique/{cbase}) | {title} | Curatorial & Institutional Mandate |")
        print(f"  Indexed Critique: {cbase}")
        
    # Section 4: Studio Journal Chronology
    lines.append("\n## 4. Studio Journal Chronology (`journal/`)")
    lines.append("| Session | Date | Title / Breakthrough | File |")
    lines.append("|---|---|---|---|")
    
    journal_files = sorted(glob.glob(os.path.join(root_dir, "journal/session_*.md")))
    for jfile in journal_files:
        jbase = os.path.basename(jfile)
        parts = jbase.replace(".md", "").split("_")
        sid = parts[1]
        title = " ".join(parts[2:]).title()
        lines.append(f"| **Session {sid}** | 2026 | {title} | [`{jbase}`](../journal/{jbase}) |")
        print(f"  Indexed Journal: {jbase}")
        
    # Section 5: Research Archive
    lines.append("\n## 5. Outside Research Archive (`notes/research/`)")
    lines.append("| Research Note | Theoretical Investigation | Link |")
    lines.append("|---|---|---|")
    
    res_files = sorted(glob.glob(os.path.join(root_dir, "notes/research/*.md")))
    for rfile in res_files:
        rbase = os.path.basename(rfile)
        title = rbase.replace(".md", "").replace("_", " ").title()
        with open(rfile, "r", encoding="utf-8") as f:
            for l in f:
                if l.startswith("# "):
                    title = l.replace("# ", "").strip()
                    break
        lines.append(f"| [`{rbase}`](../notes/research/{rbase}) | {title} | Archival Research |")
        
    print(f"  Indexed {len(res_files)} Research Notes.")
        
    # Section 6: Preserved Failures
    lines.append("\n## 6. Preserved Failures & Interrupted Trajectories (`failures/`)")
    fail_dirs = sorted(glob.glob(os.path.join(root_dir, "failures/*")))
    for fdir in fail_dirs:
        if os.path.isdir(fdir):
            fbase = os.path.basename(fdir)
            lines.append(f"- **{fbase}**: [`failures/{fbase}`](../failures/{fbase}) (Preserved negative evidence)")
            print(f"  Indexed Failure Branch: {fbase}")

    # Section 7: Collaborator Resource Requests
    lines.append("\n## 7. Collaborator Resource Requests (`notes/requests/`)")
    lines.append("| Request | File | Status |")
    lines.append("|---|---|---|")
    req_files = sorted(glob.glob(os.path.join(root_dir, "notes/requests/*.md")))
    for rq in req_files:
        rbase = os.path.basename(rq)
        title = rbase.replace(".md", "").replace("_", " ").title()
        lines.append(f"| {title} | [`{rbase}`](../notes/requests/{rbase}) | **Active Collaborator Dialogue** |")
        print(f"  Indexed Request: {rbase}")
            
    with open(index_md_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
        f.write("\n")
        
    print(f"\nSuccessfully generated master index at: {index_md_path}")
    print("=" * 65)

if __name__ == "__main__":
    generate_index()
