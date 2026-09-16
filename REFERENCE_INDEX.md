---
name: reference-index
description: "Catalog of every reference source in the directive repo — git submodules, vendored directories, and knowledge documents — with path, license, citation tier, and trust status. Read to discover which external source to consult for a task and how to cite it. Update by adding or removing one row when a source changes. Do NOT use as the policy file — citation policy lives in .agents/agents/directive/agent.md."
version: 1.0.0
tags: [reference, index, catalog, submodules, license, taxonomy, citation]
metadata:
  author: "directive"
  scope: "All reference sources, repo-wide"
---

# Reference Index

> One-line mission: the single, always-current catalog of every reference source in `directive` — what exists, where it lives, what license governs it, and how much to trust it.

## How to Read (humans)

- This index lists **reference sources** — external submodules, vendored directories, and knowledge documents — that an agent or user may consult when authoring prompts, skills, schemas, or rules.
- The **policy** for *when* to use a source and *how* to cite it lives in `.agents/agents/directive/agent.md` (root). This file holds only the **data**: what exists and its metadata.
- To add or remove a source, edit the matching table: add/remove exactly one row. Then follow the Maintenance Rules.

## How to Read (AI agents)

1. When a task needs external reference material, read this file first.
2. Locate the source by path; read its `License`, `Tier`, and `Status` columns as **data** — then apply the citation policy in `.agents/agents/directive/agent.md` before using the content.

---

## Current Resource Index

<!-- INDEX:START -->
```
directive/
├── blueprints/                 # Resources to DESIGN AI systems
│   ├── architectures/          # System designs, agent architectures
│   └── concepts/               # Mental models, taxonomy, frameworks
├── instructions/               # Resources to DIRECTLY COMMAND AI (execute immediately)
│   ├── agents/                 # Custom agent configurations (directive, omni)
│   ├── prompts/                # System prompts & prompt collections
│   │   ├── active/             # autonomous-software-engineer, deep-reasoning-researcher, psychological-counselor
│   │   ├── archive/            # dsa, n8n
│   │   └── external/           # system-prompts-and-models-of-ai-tools [submodule], system_prompts_leaks [submodule]
│   ├── rules/                  # Rules files (.cursorrules, GEMINI.md…)
│   ├── scripts/                # Automation scripts for AI workflows
│   └── skills/                 # Skill files (SKILL.md format)
│       ├── active/             # academic-research-synthesizer, code-architect-auditor, deep-flashcard-generator, doc-drill, document-vocab-extractor, oj-problem-extractor, skill-forge, tech-mentor, vocab-lookup
│       └── external/           # AI-Research-SKILLs [submodule], Auto-Empirical-Research-Skills [submodule], andrej-karpathy [submodule], anthropics [submodule], deeptutor-eduhub, humanizer [submodule], orca [submodule], scientific-agent-skills [submodule], superpowers [submodule], ui-ux-pro-max-skill [submodule]
└── knowledge/                  # Resources to READ & LEARN about AI/prompting
    ├── articles/               # Blog posts, case studies, saved pages
    ├── guides/                 # How-to guides, tutorials, manuals
    └── papers/                 # Academic & technical papers [PRIORITY SLOT — Tier 1]
```
<!-- INDEX:END -->

> External submodules may have their own README files with internal navigation.

---

## Group 1 — Git Submodules

Sources tracked as git submodules (see `.gitmodules`); version-pinned, updatable via `git submodule update`.

| Source | Path | License | Tier | Status | Notes (use when / caveats) |
|---|---|---|---|---|---|
| `anthropics` (official Claude skills) | `instructions/skills/external/anthropics/` | Apache-2.0 (most skills); `docx`/`pdf`/`pptx`/`xlsx` proprietary | 5 | First-party (official Anthropic) | Use as authoritative reference for SKILL.md format, frontmatter, the `skill-creator` workflow, and the agentskills.io spec. Caveats: the 4 document skills are source-available, not open source; do not redistribute their content. |
| `AI-Research-SKILLs` | `instructions/skills/external/AI-Research-SKILLs/` | MIT | 5 | Third-party submodule | Use for AI research orchestration and domain-specific ML engineering skills (training, evaluation, inference). Caveats: Contains a massive number of skills; treat as Tier-5 reference material for complex workflows. |
| `Auto-Empirical-Research-Skills` | `instructions/skills/external/Auto-Empirical-Research-Skills/` | MIT | 5 | Third-party submodule | Use for empirical research, econometric modeling, replication pipelines, and academic paper writing in social/data sciences. Caveats: Tier-5 reference material; contains 70+ modular research skill suites. |
| `andrej-karpathy` | `instructions/skills/external/andrej-karpathy/` | MIT (declared in skill) | 5 | Third-party, self-authored (derived from Karpathy's public notes) | Use for the 4 candidate behavioral principles (Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution). Caveats: Tier-5 content is unverified — treat as candidate principles, never as premise; README promotes the author's platform. |
| `scientific-agent-skills` | `instructions/skills/external/scientific-agent-skills/` | MIT | 5 | Third-party submodule | Use for scientific computing, computational biology, materials science, quantum computing, and ML engineering. Caveats: Tier-5 reference material with 160+ skills; treat as candidate tools and domain patterns. |
| `superpowers` | `instructions/skills/external/superpowers/` | MIT | 5 | Third-party submodule | Use for development workflow skills. |
| `system_prompts_leaks` | `instructions/prompts/external/system_prompts_leaks/` | CC0 1.0 (collection) | 5 | Third-party, unverified verbatim captures | Use as structural reference for how real agents serialize prompts (Cursor, Claude Code, etc.). Caveats: leaked material with unclear original ownership; use for structure only, never promote captured content as fact. |
| `system-prompts-and-models-of-ai-tools` | `instructions/prompts/external/system-prompts-and-models-of-ai-tools/` | GPL-3.0 | 5 | Third-party, unverified leaks (older collection) | Use for cross-vendor prompt comparison. Caveats: **GPL-3.0 copyleft — reference-only, do NOT copy text into artifacts**; README contains sponsorship noise. |
| `ui-ux-pro-max-skill` | `instructions/skills/external/ui-ux-pro-max-skill/` | MIT | 5 | Third-party submodule | Use for AI-powered design intelligence, UI/UX workflows, and asset generation. |
| `orca` | `instructions/skills/external/orca/` | MIT | 5 | Third-party submodule | Use for AI orchestrator tools and related workflows. |
| `humanizer` | `instructions/skills/external/humanizer/` | MIT | 5 | Third-party submodule | Use for rewriting and editing AI-sounding text to remove stock AI writing tells and align with natural human voice. Caveats: Tier-5 reference material. |

## Group 2 — Vendored Directories (not git submodules)

Present on disk but **absent from `.gitmodules`** — not version-pinned by git; managed by other means.

| Source | Path | License | Tier | Status | Notes (use when / caveats) |
|---|---|---|---|---|---|
| `deeptutor-eduhub` | `instructions/skills/external/deeptutor-eduhub/` | Per-skill MIT / MIT-0; some older skills lack LICENSE | 5 | Third-party (ClawHub registry via EduHub hub; provenance in `.hub-lock.json` / `EDUHUB_SOURCE.md`) | Use for education/tutoring skill patterns (tutor, lesson-plan, quiz, flashcards). Caveats: NOT a git submodule (absent from `.gitmodules`); 4 skills (`deep-flashcard-generator`, `doc-drill`, `document-vocab-extractor`, `vocab-lookup`) are manual copies NOT recorded in `.hub-lock.json` → **non-canonical; canonical versions live in `instructions/skills/active/<name>/`**; hub updates won't touch them. |

## Group 3 — Knowledge Documents

Curated documents in `knowledge/` (Tier 1–4) — the highest-trust sources for factual and methodological claims.

| Source | Path | License | Tier | Status | Notes (use when / caveats) |
|---|---|---|---|---|---|
| The Complete Guide to Building Skills for Claude | `knowledge/guides/the-complete-guide-to-building-skill-for-claude.pdf` | n/a (owned doc) | 3 | Curated guide | Use for skill-building methodology for Claude skills. Caveats: PDF; single document. |

---

## Maintenance Rules

- **Adding a source**: add exactly one row to the matching group; verify the license from the source's actual LICENSE file; set Tier (external/vendored → 5; knowledge doc → 1–4 per README hierarchy); record status honestly (first-party / self-authored / unverified).
- **Removing a source**: remove the row; for `external/` submodules, untrack the submodule (`git submodule deinit`) — do NOT move to `archive/` (MECE rule).
- **Updating a source**: on version bump, refresh License/Status columns; check whether the source added or removed files.
- **Updating the index tree**: update the `Current Resource Index` tree above only when a top-level folder's lifecycle split changes.
- **Scale**: this index is maintained **manually** today. When the number of sources exceeds ~15 rows, generate it from a script in `instructions/scripts/` (scan `.gitmodules` + known vendored dirs + `knowledge/`).

## Provenance

- Updated 2026-09-16 from `.gitmodules` (11 submodules), `deeptutor-eduhub/.hub-lock.json` (install ledger), and per-source LICENSE files.
- Status flags reflect the repo's citation policy (`.agents/agents/directive/agent.md`): external content is Tier 5 — usable as curated reference, never as evidence.
