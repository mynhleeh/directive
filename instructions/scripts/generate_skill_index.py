#!/usr/bin/env python3
"""Generate instructions/skills/INDEX.md from active and external skills.

Enforces deterministic sorting, canonical source trust tiers, license attribution,
description sanitization, and Markdown formatting compliance.
"""

import argparse
import difflib
import os
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional, Set, Tuple

SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import extract_skills  # noqa: E402

ACTIVE_PATH = REPO_ROOT / "instructions" / "skills" / "active"
EXTERNAL_PATH = REPO_ROOT / "instructions" / "skills" / "external"
SKILLS_DIR = REPO_ROOT / "instructions" / "skills"
DEFAULT_OUTPUT = SKILLS_DIR / "INDEX.md"

SOURCE_METADATA: Dict[str, Dict[str, Any]] = {
    "anthropics": {
        "focus": "Official Claude skills, skill creation, and document formats",
        "tier": 2,
        "origin": "Git Submodule",
        "license": "Apache-2.0 (most); `docx`/`pdf`/`pptx`/`xlsx` proprietary",
        "notes": "Prefix `ant-` on collision; 4 document skills source-available only",
        "rel_path": "external/anthropics/",
    },
    "AI-Research-SKILLs": {
        "focus": "ML engineering, training, evaluation, and LLM serving",
        "tier": 3,
        "origin": "Git Submodule",
        "license": "MIT",
        "notes": "Prefix `ars-` on collision",
        "rel_path": "external/AI-Research-SKILLs/",
    },
    "Auto-Empirical-Research-Skills": {
        "focus": "Econometric pipelines, causal inference, and replication",
        "tier": 3,
        "origin": "Git Submodule",
        "license": "MIT",
        "notes": "Prefix `aers-` on collision; 78 top-level suites with nested skills",
        "rel_path": "external/Auto-Empirical-Research-Skills/",
    },
    "humanizer": {
        "focus": "Prose revision removing stock AI writing tells",
        "tier": 3,
        "origin": "Git Submodule",
        "license": "MIT",
        "notes": "Standalone skill",
        "rel_path": "external/humanizer/",
    },
    "orca": {
        "focus": "Orca CLI, worktrees, Linear/Jira tickets, orchestration",
        "tier": 3,
        "origin": "Git Submodule",
        "license": "MIT",
        "notes": "Prefix `orc-` on collision",
        "rel_path": "external/orca/",
    },
    "ppt-master": {
        "focus": "Native editable PPTX generation, templates, and SVG-to-DrawingML workflows",
        "tier": 3,
        "origin": "Git Submodule",
        "license": "MIT (optional `PyMuPDF` dependency is AGPL-3.0)",
        "notes": "Standalone skill under `skills/ppt-master/`; optional `PyMuPDF` is AGPL-3.0",
        "rel_path": "external/ppt-master/",
    },
    "scientific-agent-skills": {
        "focus": "Scientific computing, bioinformatics, chemistry, quantum",
        "tier": 3,
        "origin": "Git Submodule",
        "license": "MIT",
        "notes": "Prefix `sas-` on collision",
        "rel_path": "external/scientific-agent-skills/",
    },
    "superpowers": {
        "focus": "Structured brainstorming, TDD, planning, verification",
        "tier": 3,
        "origin": "Git Submodule",
        "license": "MIT",
        "notes": "Prefix `sup-` on collision",
        "rel_path": "external/superpowers/",
    },
    "ui-ux-pro-max-skill": {
        "focus": "UI/UX design intelligence, design systems, and slides",
        "tier": 3,
        "origin": "Git Submodule",
        "license": "MIT",
        "notes": "Prefix `uupms-` on collision; `.claude/skills` deduplicates `cli/assets`",
        "rel_path": "external/ui-ux-pro-max-skill/",
    },
    "andrej-karpathy": {
        "focus": "Behavioral coding heuristics adapted from Karpathy notes",
        "tier": 4,
        "origin": "Git Submodule",
        "license": "MIT (in skill)",
        "notes": "Third-party self-authored adaptation; candidate heuristics",
        "rel_path": "external/andrej-karpathy/",
    },
    "deeptutor-eduhub": {
        "focus": "Education, tutoring, study, and cognitive model skills",
        "tier": 4,
        "origin": "Vendored Dir",
        "license": "Per-skill MIT / MIT-0; some missing",
        "notes": "EduHub registry (`.hub-lock.json`); absent from `.gitmodules`",
        "rel_path": "external/deeptutor-eduhub/",
    },
    "diagram-skills-package": {
        "focus": "IT Business Analyst diagramming (Mermaid, PlantUML, D2, BPMN, DBML)",
        "tier": 4,
        "origin": "Vendored Dir",
        "license": "MIT",
        "notes": "Canonical skills reside under `claude-code/.claude/skills/`",
        "rel_path": "external/diagram-skills-package/",
    },
    "reuseforge-standalone-bundle-v1.0.0": {
        "focus": "ReuseForge architecture, scouting, and gate routing family",
        "tier": 4,
        "origin": "Vendored Dir",
        "license": "Unspecified (`MANIFEST.json`)",
        "notes": "Standalone bundle (`reuseforge/1.0`) under `skills/`",
        "rel_path": "external/reuseforge-standalone-bundle-v1.0.0/",
    },
    "active": {
        "focus": "Owned AI-authored workflow, doc, and skill-engineering tools",
        "tier": 5,
        "origin": "In-house",
        "license": "MIT / Owned",
        "notes": "Prefix `own-` on collision; Operational Role: Executable",
        "rel_path": "active/",
    },
}


def parse_frontmatter(text: str) -> Tuple[Optional[str], Optional[str]]:
    """Parse YAML frontmatter name and description without external dependencies."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, None

    fm_lines = []
    closing_idx = -1
    for idx, line in enumerate(lines[1:], 1):
        if line.strip() in ("---", "..."):
            closing_idx = idx
            break
        fm_lines.append(line)

    name = None
    desc_lines = []
    in_desc = False

    for line in fm_lines:
        if not in_desc:
            name_match = re.match(r"^name:\s*(.*)$", line)
            if name_match:
                val = name_match.group(1).strip().strip("'\"")
                name = val
                continue
            desc_match = re.match(r"^description:\s*(.*)$", line)
            if desc_match:
                val = desc_match.group(1).strip()
                in_desc = True
                if val in (">", ">-", "|", "|-", ""):
                    pass
                else:
                    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                        desc_lines.append(val[1:-1])
                    else:
                        desc_lines.append(val)
                continue
        else:
            if re.match(r"^[a-zA-Z0-9_-]+:\s*", line):
                in_desc = False
                name_match = re.match(r"^name:\s*(.*)$", line)
                if name_match:
                    name = name_match.group(1).strip().strip("'\"")
                continue

            if line.strip() == "":
                continue

            indent = len(line) - len(line.lstrip())
            if indent > 0:
                desc_lines.append(line.strip())
            else:
                in_desc = False

    description = " ".join([l for l in desc_lines if l]).strip() if desc_lines else None

    # Fallback to first body paragraph if description is absent
    if not description and closing_idx != -1 and closing_idx + 1 < len(lines):
        body_lines = lines[closing_idx + 1 :]
        body_para = []
        for bline in body_lines:
            sline = bline.strip()
            if not sline:
                if body_para:
                    break
                continue
            if sline.startswith("#"):
                continue
            body_para.append(sline)
        if body_para:
            description = " ".join(body_para).strip()

    return name, description


def clean_description(desc: Optional[str]) -> str:
    """Normalize and escape description string for single-line Markdown table cells."""
    if not desc:
        return ""
    desc = desc.replace("→", "->").replace("⇒", "->")
    desc = desc.replace("—", " - ").replace("–", " - ")
    desc = re.sub(r"[\r\n\t]+", " ", desc)
    desc = re.sub(r" {2,}", " ", desc)
    # Unescape escaped pipes first, then escape all pipes
    desc = desc.replace(r"\|", "|")
    desc = desc.replace("|", r"\|")
    if re.search(r"(?<!\\)\\$", desc):
        desc = desc[:-1] + " "

    # Protect pseudo-markdown links like [text](url) in descriptions from rendering as broken links
    def _quote_pseudo_link(match: re.Match) -> str:
        text, url = match.group(1), match.group(2)
        if url.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)
        return f"`[{text}]({url})`"

    desc = re.sub(r"(?<!`)(?<!\\)\[([^\]]+)\]\(([^)]+)\)(?!`)", _quote_pseudo_link, desc)
    return desc.strip()


def compute_raw_counts(active_dir: Path, external_dir: Path) -> Dict[str, int]:
    """Count raw SKILL.md occurrences per source directory on disk."""
    raw_counts: Dict[str, int] = {}
    if active_dir.is_dir():
        raw_counts["active"] = sum(1 for root, _, files in os.walk(active_dir) if "SKILL.md" in files)
    if external_dir.is_dir():
        for sub in external_dir.iterdir():
            if sub.is_dir():
                raw_counts[sub.name] = sum(1 for root, _, files in os.walk(sub) if "SKILL.md" in files)
    return raw_counts


def generate_index_content(active_dir: Path, external_dir: Path, skills_root: Path) -> str:
    """Generate the full content of instructions/skills/INDEX.md."""
    skills = extract_skills.find_all_skills(active_dir, external_dir)
    discovered_sources: Set[str] = set(s[0] for s in skills)

    unknown_sources = discovered_sources - set(SOURCE_METADATA.keys())
    if unknown_sources:
        raise ValueError(
            f"Unregistered skill source(s) discovered: {sorted(unknown_sources)}. "
            "Update SOURCE_METADATA with tier and provenance metadata before generating index."
        )

    raw_counts = compute_raw_counts(active_dir, external_dir)

    # Sort sources: Tier ascending, then lowercase name
    sorted_sources = sorted(
        SOURCE_METADATA.keys(),
        key=lambda k: (SOURCE_METADATA[k]["tier"], k.lower()),
    )

    # Group skills by source
    skills_by_source: Dict[str, List[Dict[str, str]]] = {src: [] for src in sorted_sources}
    for source, dir_name, path in skills:
        skill_file = path / "SKILL.md"
        text = skill_file.read_text(encoding="utf-8", errors="replace")
        yaml_name, desc = parse_frontmatter(text)
        display_name = yaml_name if yaml_name else dir_name
        rel_path = (skill_file).relative_to(skills_root).as_posix()
        cleaned_desc = clean_description(desc)

        skills_by_source[source].append(
            {
                "display_name": display_name,
                "rel_path": rel_path,
                "description": cleaned_desc,
            }
        )

    # Sort skills inside each source alphabetically by displayed skill name
    for src in sorted_sources:
        skills_by_source[src].sort(key=lambda s: (s["display_name"].lower(), s["rel_path"].lower()))

    lines: List[str] = [
        "---",
        "name: skills-index",
        'description: "Index and tier registry for all skills under instructions/skills/ (active and external). Read to select candidate sources by domain and tier, or drill into Skill Catalog by Source for individual skills."',
        "version: 2.2.0",
        "tags: [skills, index, tiers, catalog, capabilities]",
        "metadata:",
        '  author: "directive"',
        '  scope: "All active and external skills under instructions/skills/"',
        "---",
        "",
        "# Skill Index",
        "",
        "Comprehensive catalog and source-trust classification for all skills available under `instructions/skills/`. Canonical definitions of the 6-tier trust scale live in [README.md](../../README.md).",
        "",
        "## Source Overview",
        "",
        "| Source | Focus & Capabilities | Tier | Origin | Count | Trigger / Notes |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    for src in sorted_sources:
        meta = SOURCE_METADATA[src]
        canonical_count = len(skills_by_source[src])
        raw_count = raw_counts.get(src, canonical_count)
        count_str = f"{canonical_count} ({raw_count} raw)" if raw_count > canonical_count else str(canonical_count)
        source_link = f"[`{src}`]({meta['rel_path']})"
        tier_str = f"`Tier {meta['tier']}`"
        lines.append(
            f"| {source_link} | {meta['focus']} | {tier_str} | {meta['origin']} | {count_str} | {meta['notes']} |"
        )

    lines.append("")
    lines.append("## Skill Catalog by Source")

    for src in sorted_sources:
        items = skills_by_source[src]
        lines.append("")
        lines.append(f"### {src}")
        lines.append("")
        lines.append("| # | Skill | Description |")
        lines.append("| --- | --- | --- |")
        for idx, item in enumerate(items, 1):
            skill_link = f"[{item['display_name']}]({item['rel_path']})"
            lines.append(f"| {idx} | {skill_link} | {item['description']} |")

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate instructions/skills/INDEX.md")
    parser.add_argument("--write", action="store_true", help="Write generated index to target output file.")
    parser.add_argument("--check", action="store_true", help="Check if target output file matches generated content.")
    parser.add_argument("--output", type=Path, default=None, help="Target output file path.")
    args = parser.parse_args()

    if not args.write and not args.check:
        args.write = True

    output_path = args.output if args.output else DEFAULT_OUTPUT
    content = generate_index_content(ACTIVE_PATH, EXTERNAL_PATH, SKILLS_DIR)

    if args.check:
        if not output_path.exists():
            print(f"FAIL: Target file {output_path} does not exist.")
            return 1
        current = output_path.read_bytes().decode("utf-8")
        if current == content:
            print(f"PASS: {output_path} is synchronized with source trees (0 drift).")
            return 0
        diff = list(
            difflib.unified_diff(
                current.splitlines(keepends=True),
                content.splitlines(keepends=True),
                fromfile=str(output_path),
                tofile="generated",
                n=3,
            )
        )
        print(f"FAIL: Drift detected between {output_path} and canonical skills ({len(diff)} diff lines):")
        sys.stdout.writelines(diff[:40])
        if len(diff) > 40:
            print(f"... and {len(diff) - 40} more lines.")
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8", newline="\n")
    skill_count = sum(1 for line in content.splitlines() if re.match(r"^\|\s*\d+\s*\|", line))
    source_count = sum(1 for line in content.splitlines() if line.startswith("### "))
    print(f"SUCCESS: Generated {output_path} ({skill_count} canonical skills across {source_count} sources).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
