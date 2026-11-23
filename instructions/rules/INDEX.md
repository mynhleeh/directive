---
name: rules-index
description: "Index, authority hierarchy, and trust classification for workspace rules under instructions/rules/. Read to discover active governance invariants and operational constraints."
version: 1.2.0
tags: [rules, index, tiers, governance, constraints, standards]
metadata:
  author: "directive"
  scope: "All rule specifications under instructions/rules/"
---

# Rules Index

Catalog and authority classification for workspace rules under `instructions/rules/`. Canonical definitions of the 6-tier trust scale live in [README.md](../../README.md).

## Module Tier

All owned rules in this directory are in-house synthesized engineering and formatting standards classified under **Tier 5**.

## Rule Catalog

| Rule | Scope & Purpose | Precedence | Summary |
| --- | --- | --- | --- |
| [`clean-engineering-and-testing`](clean-engineering-and-testing.rule.md) | Code Quality & Testing | Priority 5 | Micro-unit inside-out delivery, zero-guesswork halting, precision arithmetic, edge-case test matrix |
| [`core-collaboration-charter`](core-collaboration-charter.rule.md) | Core Collaboration | Priority 2 & 3 | Single-unit incremental delivery, clarify gate, evidence-backed claims, four-link reasoning |
| [`file-folder-organization`](file-folder-organization.rule.md) | File & Folder Hygiene | Priority 4 | Strict MECE directory structure, intent taxonomy, dynamic lifecycle state splits, and naming conventions |
| [`knowledge-grounding-and-citation`](knowledge-grounding-and-citation.rule.md) | Knowledge Grounding | Priority 5 | Multi-tier grounding hierarchy, dynamic branch resolution, ingestion gate, and 3-channel citations |
| [`markdown-formatting-and-layout`](markdown-formatting-and-layout.rule.md) | Markdown Layout | Priority 4 | Content density, compact tables, zero thematic breaks, zero HTML entities, deterministic awk checks |
| [`software-architecture-and-modeling`](software-architecture-and-modeling.rule.md) | Software Architecture | Priority 5 | Separation of Requirements/OOA/OOD, Inside-Out dependencies, SOLID principles, and UML modeling |
| [`task-workflow-and-construction`](task-workflow-and-construction.rule.md) | Task Orchestration | Priority 6 | Six-phase pipeline, scaffold-first unit construction (FIFO/LIFO), risk classes, whole-scope sweeps |
| [`technical-writing-principles`](technical-writing-principles.rule.md) | Technical Writing | Priority 5 | Anti-AI writing principles, elimination of filler rhetoric, precise vocabulary, and factual calibration |

## Maintenance Rules

1. Register each new rule in `Rule Catalog` with its scope, precedence, and concise summary.
2. All rules in this directory are governed as Tier 5 assets. Never record tier metadata inside individual `*.rule.md` files or frontmatter.
3. Mirror active rule definitions to `.agents/rules/` and `.claude/rules/` when target workspace scaffolding is required.
